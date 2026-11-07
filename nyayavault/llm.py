"""NyayaVault providers: a deterministic mock and the real BharatCode API.

Both providers share one interface: ``ask(question, context, language)``
returns a ``Result``. The mock never calls the network and never
pretends to be a model — its answers are extractive (the first long
sentence after a marker) and are always labelled ``[mock]``. The real
provider calls the BharatCode model API with a key from the
environment only; without a key the app never reaches this code.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .config import NyayaVaultConfig

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass
class ProviderResult:
    text: str
    model: str
    provider: str  # "mock" or "bharatcode"


def extractive_answer(question: str, context: str) -> str:
    """Deterministic extractive answer from retrieved context.

    Takes the first substantive sentence (60+ characters) from the
    first provision's Statutory text section, falling back to the
    Plain-language note, then the Case note. Bold markers are
    stripped. Legal abbreviations ("v.", "s.", "ss.", "No.", "Rs.")
    are protected so a sentence is never cut mid-citation. Never
    invents anything — it only returns words already in the corpus.
    """
    text = context.strip()
    if not text:
        return ""
    protected = {" v. ": " v\u0000 ", " s. ": " s\u0000 ", " ss. ": " ss\u0000 ",
                 " No. ": " No\u0000 ", " Rs. ": " Rs\u0000 "}
    for heading in ("## Statutory text", "## Plain-language note", "## Case note"):
        start = text.find(heading)
        if start < 0:
            continue
        end = text.find("\n## ", start + 1)
        section = text[start:end if end > 0 else len(text)]
        lines = [
            line.lstrip("> ").replace("**", "").strip()
            for line in section.splitlines()[1:]
        ]
        body = " ".join(line for line in lines if line)
        for abbr, placeholder in protected.items():
            body = body.replace(abbr, placeholder)
        for sentence in SENTENCE_END.split(body):
            sentence = sentence.replace("\u0000", ".").strip()
            if len(sentence) >= 60:
                return sentence
    return ""


class MockProvider:
    """Offline extractive provider. No network, no key, no pretence."""

    def __init__(self) -> None:
        self.model = "mock-extractive"

    def ask(self, question: str, context: str, language: str = "en") -> ProviderResult:
        answer = extractive_answer(question, context)
        if not answer:
            answer = "The corpus has no provision that answers this question."
        return ProviderResult(text=answer, model=self.model, provider="mock")


class BharatCodeProvider:
    """Real provider: BharatCode model API (key from env only)."""

    def __init__(self, config: NyayaVaultConfig) -> None:
        self.config = config
        self.model = config.model

    def ask(self, question: str, context: str, language: str = "en") -> ProviderResult:
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are NyayaVault, a legal research assistant. "
                        "Answer ONLY from the provisions below. Cite the Act "
                        "and section for every claim. If the provisions do not "
                        "answer the question, say so plainly and refuse. "
                        "Never invent a case, a section number, or a judgment. "
                        "This is general legal information, not legal advice."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Language: {language}\n\n"
                        f"Provisions:\n{context}\n\n"
                        f"Question: {question}"
                    ),
                },
            ],
        }
        request = urllib.request.Request(
            f"{self.config.base_url}/api/model/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"BharatCode API error: HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"BharatCode API unreachable: {exc}") from exc
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("BharatCode API returned no answer")
        text = (choices[0].get("message") or {}).get("content", "").strip()
        if not text:
            raise RuntimeError("BharatCode API returned an empty answer")
        return ProviderResult(text=text, model=self.config.model, provider="bharatcode")
