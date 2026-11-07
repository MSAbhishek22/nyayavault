"""NyayaVault guardrails: keep secrets and personal data out of prompts.

The app answers from a public legal corpus, so nothing a user types
should leave the machine. These rules reject text that looks like a
credential, a token, or a financial secret — before any provider is
called — and the app never stores what it refused.
"""

from __future__ import annotations

import re

# Patterns adapted from the BharatCode sibling: things a user should
# never paste into a legal question (or any prompt).
DENY = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?key|secret|token|password)\s*[:=]\s*\S{8,}"),
    re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),  # card-like number
    re.compile(r"\b\d{12}\b"),  # Aadhaar-like number (12 digits)
]

LEGAL_NOTE = (
    "NyayaVault gives general legal information, not legal advice. "
    "For your specific situation, consult a licensed advocate."
)


def guard_question(question: str) -> str | None:
    """Return a refusal string when the text must not be sent onward.

    Returns ``None`` when the question is safe to process.
    """
    text = question.strip()
    if not text:
        return "Ask a legal question about the corpus — for example, what happens if someone steals my password?"
    if len(text) > 800:
        return "That question is too long. Please keep it under 800 characters."
    for pattern in DENY:
        if pattern.search(text):
            return (
                "That question looks like it contains a secret, a password, "
                "a token, or a personal number. NyayaVault never sends such "
                "things to any model. Remove it and ask again — for example, "
                "describe what happened without pasting the password or the "
                "number itself."
            )
    return None
