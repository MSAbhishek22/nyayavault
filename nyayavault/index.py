"""NyayaVault legal-corpus index: load, search, and open provisions.

The corpus is a folder of Markdown files, one per provision, each
with a ``# Title`` heading and header lines ``Act:``, ``Section:``
and ``Source:``. Search is a deterministic keyword scorer — title
and tag matches count most — so the same question always retrieves
the same provisions.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

TOKEN_RE = re.compile(r"[a-z0-9]+")
TAG_RE = re.compile(r"#([a-z0-9][a-z0-9_-]*)")
ACT_RE = re.compile(r"^Act:\s*(.+)$", re.MULTILINE)
SECTION_RE = re.compile(r"^Section:\s*(.+)$", re.MULTILINE)
SOURCE_RE = re.compile(r"^Source:\s*(.+)$", re.MULTILINE)

# Words that appear in nearly every legal document and carry no
# retrieval signal (e.g. "act" is in every header, "what" in every
# question). Filtering them keeps a generic question from matching
# the whole corpus.
STOPWORDS = frozenset({
    "what", "who", "when", "where", "why", "how", "which", "whose",
    "does", "do", "did", "is", "are", "was", "were", "be", "been",
    "the", "a", "an", "and", "or", "if", "can", "could", "should",
    "would", "may", "might", "must", "shall", "will",
    "i", "my", "me", "we", "you", "he", "she", "it", "its", "they",
    "in", "on", "of", "to", "for", "with", "by", "about", "from",
    "at", "as", "into", "under", "over", "than", "then",
    "say", "says", "said", "tell", "happens", "happen",
    "act", "section", "law", "legal", "india", "indian",
    "used", "use", "using", "corpus", "general", "advice",
    "verify", "information", "note", "summary",
})

# A hit must score at least 2: one body-only word match is not enough
# to claim a grounded answer. This is what makes an out-of-corpus
# question (e.g. about the DPDP Act 2023) refuse instead of answering
# from a stray word.
MIN_SCORE = 2


@dataclass
class Provision:
    """One verified legal document from the corpus."""

    title: str
    act: str
    section: str
    source: str
    rel: str
    tags: list[str]
    body: str

    @property
    def short_act(self) -> str:
        """Act name without the parenthetical Act number."""
        return self.act.split(" (", 1)[0].strip()

    @property
    def short_section(self) -> str:
        """Section label without the parenthetical chapter note.

        Case notes keep their full label — the year and citation
        (e.g. (2020) 3 SCC 637) are part of the reference.
        """
        if self.section.startswith("Case note"):
            return self.section
        return self.section.split(" (", 1)[0].strip()

    @property
    def citation(self) -> str:
        """Short citation: 'IT Act 2000, Section 66C' style."""
        return f"{self.short_act}, {self.short_section}"


def load_provisions(corpus_root: str) -> list[Provision]:
    """Read every ``.md`` file under ``corpus_root`` (sorted, stable)."""
    found: list[Provision] = []
    for name in sorted(os.listdir(corpus_root)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(corpus_root, name)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        act = _first(ACT_RE, text, "Unknown Act")
        section = _first(SECTION_RE, text, "")
        source = _first(SOURCE_RE, text, "")
        tags = TAG_RE.findall(text.lower())
        found.append(
            Provision(
                title=title or name,
                act=act,
                section=section,
                source=source,
                rel=name,
                tags=tags,
                body=text,
            )
        )
    return found


def _first(pattern: re.Pattern, text: str, default: str) -> str:
    match = pattern.search(text)
    return match.group(1).strip() if match else default


def score(question: str, provision: Provision) -> int:
    """Keyword score for one provision against a question.

    Title matches count 3, tag matches count 3, body matches count 1.
    Stopwords are ignored, so a generic question cannot match the
    whole corpus on words like "act" or "law".
    """
    return match_detail(question, provision)[0]


def match_detail(question: str, provision: Provision) -> tuple[int, int]:
    """(score, distinct matched words) for one provision.

    The distinct count matters for retrieval: a single word that
    happens to sit in a title (e.g. "punishment" in a question about
    murder) is not a grounded answer on its own.
    """
    tokens = {t for t in TOKEN_RE.findall(question.lower()) if t not in STOPWORDS}
    if not tokens:
        return 0, 0
    hits = 0
    matched: set[str] = set()
    title_tokens = set(TOKEN_RE.findall(provision.title.lower()))
    body_tokens = set(TOKEN_RE.findall(provision.body.lower()))
    for token in tokens:
        token_hits = 0
        if token in title_tokens:
            token_hits += 3
        if token in provision.tags:
            token_hits += 3
        # Whole-word body match, with a simple plural tolerance
        # ("product" finds "products", "products" finds "product").
        # Substring matching is deliberately NOT used: "data" must not
        # match "damage".
        variants = {token, f"{token}s", f"{token}es"}
        if token.endswith("s"):
            variants.add(token[:-1])
        if len(token) > 2 and variants & body_tokens:
            token_hits += 1
        if token_hits:
            matched.add(token)
        hits += token_hits
    return hits, len(matched)


def search_provisions(question: str, provisions: list[Provision], limit: int = 3) -> list[Provision]:
    """Best-matching provisions, highest score first, stable order.

    A provision counts as a hit only if it scores at least MIN_SCORE
    and either scores strongly (>= 5, e.g. a title + tag match on one
    word) or matches at least two distinct words. A single stray word
    is not a grounded answer.
    """
    ranked = sorted(
        ((match_detail(question, p), p.rel, p) for p in provisions),
        key=lambda item: (-item[0][0], item[1]),
    )
    return [
        item[2]
        for item in ranked
        if item[0][0] >= MIN_SCORE and (item[0][0] >= 5 or item[0][1] >= 2)
    ][:limit]


def list_by_act(provisions: list[Provision]) -> dict[str, list[Provision]]:
    """Group provisions by Act, preserving corpus order."""
    grouped: dict[str, list[Provision]] = {}
    for provision in provisions:
        grouped.setdefault(provision.act, []).append(provision)
    return grouped
