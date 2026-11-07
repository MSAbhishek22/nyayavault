"""NyayaVault legal agent: grounded Q&A + research briefs.

The agent never answers from the model alone. It retrieves
provisions from the local corpus first, refuses when nothing
matches, and only then asks a provider — mock or real — with the
retrieved text as its only source. Every answer carries its
citations, its mode, and the legal-information disclaimer.
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field

from .config import NyayaVaultConfig
from .guardrails import LEGAL_NOTE, guard_question
from .index import Provision, list_by_act, load_provisions, search_provisions
from .routing import RoutingLedger, run_with_fallback

REFUSAL_TEXT = (
    "I could not find a grounded answer to that question in the "
    "NyayaVault corpus. The corpus covers the Constitution of India "
    "(Articles 14, 19, 21 and 32), the Information Technology Act "
    "2000 (sections 43, 66, 66C, 66D and 79, plus a note that "
    "section 66A is void), the Consumer Protection Act 2019 "
    "(sections 2, 34, 35 and 69), and the Indian Contract Act 1872 "
    "(sections 2(h), 10 and 73). I will not guess, invent a section "
    "number, or invent a case. Try asking about identity theft, "
    "online free speech, a consumer refund, or a broken contract — "
    "or consult a licensed advocate for your specific situation."
)


@dataclass
class LegalAnswer:
    ok: bool
    answer: str = ""
    citations: list[Provision] = field(default_factory=list)
    mode: str = "mock"
    language: str = "en"
    model: str = "mock-extractive"
    reason: str = ""
    attempted: list[str] = field(default_factory=list)
    fallback_used: bool = False
    error: str = ""


class LegalAgent:
    """Grounded legal Q&A over the NyayaVault corpus."""

    def __init__(self, config: NyayaVaultConfig) -> None:
        self.config = config
        self.provisions = load_provisions(config.corpus_root)
        self.ledger = RoutingLedger(cap=config.daily_call_cap)
        self.language = "en"

    # -- corpus ----------------------------------------------------
    def search(self, question: str, limit: int = 3) -> list[Provision]:
        return search_provisions(question, self.provisions, limit=limit)

    def by_act(self) -> dict[str, list[Provision]]:
        return list_by_act(self.provisions)

    # -- Q&A -------------------------------------------------------
    def ask_detailed(self, question: str, language: str = "en") -> LegalAnswer:
        refusal = guard_question(question)
        if refusal is not None:
            return LegalAnswer(ok=False, error=refusal, language=language)
        hits = self.search(question)
        if not hits:
            return LegalAnswer(
                ok=False,
                answer=REFUSAL_TEXT,
                mode="refused",
                language=language,
                error=REFUSAL_TEXT,
            )
        # A coverage note as the top hit means the question is about
        # something the corpus explicitly does NOT cover (e.g. the
        # DPDP Act 2023). That is a grounded refusal, not an answer —
        # and it costs no budget.
        if "not-in-corpus" in hits[0].tags:
            note = _coverage_section(hits[0].body)
            return LegalAnswer(
                ok=False,
                answer=note,
                citations=[hits[0]],
                mode="refused",
                language=language,
                error=note,
            )
        context = "\n\n---\n\n".join(
            f"{p.title}\n{p.citation}\n{p.body}" for p in hits
        )
        try:
            result, decision = run_with_fallback(
                self.config, question, context, language, self.ledger
            )
        except RuntimeError as exc:
            return LegalAnswer(ok=False, error=str(exc), language=language)
        mode = "real" if decision.provider == "bharatcode" else "mock"
        answer = result.text
        if mode == "mock":
            answer = f"[mock] {answer}"
        answer = f"{answer}\n\n{LEGAL_NOTE}"
        return LegalAnswer(
            ok=True,
            answer=answer,
            citations=hits,
            mode=mode,
            language=language,
            model=decision.model,
            reason=decision.reason,
            attempted=decision.attempted,
            fallback_used=decision.fallback_used,
        )

    def ask(self, question: str, language: str = "en") -> str:
        answer = self.ask_detailed(question, language)
        return answer.answer if answer.ok else answer.error

    # -- research brief --------------------------------------------
    def research_brief(self, question: str, language: str = "en") -> str:
        """A structured research brief, generated from the corpus.

        The brief is deterministic in mock mode: short answer from
        the extractive provider, provisions quoted from the corpus,
        and an explicit "not covered" section. It is a legal
        information document, not legal advice.
        """
        detail = self.ask_detailed(question, language)
        today = datetime.date.today().isoformat()
        mode_label = "mock (extractive, offline)" if detail.mode == "mock" else "real BharatCode model"
        lines = [
            f"# Research brief — {question.strip()}",
            "",
            f"Prepared by NyayaVault on {today}. Mode: {mode_label}.",
            f"Language: {language}.",
            "",
            "## Short answer",
            "",
            detail.answer if detail.ok else detail.error,
            "",
            "## What the law says",
            "",
        ]
        if detail.citations:
            for provision in detail.citations:
                lines.append(f"### {provision.title}")
                lines.append("")
                lines.append(f"Citation: {provision.citation}.")
                lines.append(f"Source: {provision.source}")
                lines.append("")
                statutory = _statutory_section(provision.body)
                if statutory:
                    lines.append(statutory.strip())
                    lines.append("")
        else:
            lines.append("No provision in the corpus answers this question.")
            lines.append("")
        lines.extend(
            [
                "## What is NOT covered",
                "",
                "- This brief draws only on the 17 documents in the NyayaVault "
                "corpus (Constitution Arts. 14, 19, 21, 32; IT Act 2000 ss. 43, "
                "66, 66C, 66D, 79; Consumer Protection Act 2019 ss. 2, 34, 35, "
                "69; Indian Contract Act 1872 ss. 2(h), 10, 73; plus one "
                "coverage note stating that the DPDP Act 2023 is not covered).",
                "- Case law is limited to two verified notes: Shreya Singhal "
                "(2015) 5 SCC 1 and Anuradha Bhasin (2020) 3 SCC 637.",
                "- The Digital Personal Data Protection Act 2023, state "
                "amendments, and subordinate rules are not in the corpus.",
                "- No facts about the reader's own situation were used, and "
                "none are in this brief.",
                "",
                "## Next steps (general information only)",
                "",
                "- Verify the quoted text against the official source listed "
                "under each provision (India Code / Gazette of India).",
                "- If the matter involves a real dispute, a deadline, or money "
                "at risk, consult a licensed advocate before acting.",
                "- For a consumer complaint: check that you are a 'consumer' "
                "under CPA 2019 s. 2(7), file within two years (s. 69), and "
                "file where you live or work (s. 34).",
                "",
                "---",
                "",
                "This brief is general legal information, not legal advice.",
            ]
        )
        return "\n".join(lines)

    # -- samples ---------------------------------------------------
    def list_samples(self, samples_root: str) -> list[str]:
        if not os.path.isdir(samples_root):
            return []
        return sorted(
            name for name in os.listdir(samples_root) if name.endswith(".md")
        )

    def read_sample(self, samples_root: str, name: str) -> str | None:
        safe = os.path.basename(name)
        path = os.path.join(samples_root, safe)
        if not safe.endswith(".md") or not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as handle:
            return handle.read()


def _coverage_section(body: str) -> str:
    """The 'Coverage note' section of a coverage-note document."""
    start = body.find("## Coverage note")
    if start < 0:
        return body.strip()
    end = body.find("\n## ", start + 1)
    section = body[start:end if end > 0 else len(body)]
    lines = [line.strip() for line in section.splitlines()[1:] if line.strip()]
    return " ".join(lines)


def _statutory_section(body: str) -> str:
    """The main substantive section of a corpus document, if present.

    Statutory text first; a coverage note's own section second; then
    a case note; then the plain-language note.
    """
    for heading in ("## Statutory text", "## Coverage note", "## Case note"):
        start = body.find(heading)
        if start < 0:
            continue
        end = body.find("## Plain-language note", start)
        if end < 0:
            end = body.find("\n## ", start + 1)
        if end < 0:
            end = len(body)
        return body[start:end].strip()
    return ""
