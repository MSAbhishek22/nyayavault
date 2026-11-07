"""NyayaVault CLI: ask the corpus, draft a brief, list provisions.

Usage:
    python3 -m nyayavault.cli ask "Someone stole my password — what does the law say?"
    python3 -m nyayavault.cli brief "Can the government shut down the internet?"
    python3 -m nyayavault.cli list
    python3 -m nyayavault.cli samples
"""

from __future__ import annotations

import argparse
import os
import sys

from .agent import LegalAgent
from .config import config_from_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_ROOT = os.path.join(BASE_DIR, "corpus")
SAMPLES_ROOT = os.path.join(BASE_DIR, "samples")


def _agent() -> LegalAgent:
    return LegalAgent(config_from_env(CORPUS_ROOT))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nyayavault", description="NyayaVault legal research assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="Ask a grounded legal question")
    ask.add_argument("question")
    ask.add_argument("--language", default="en", choices=["en", "hi", "hinglish"])

    brief = sub.add_parser("brief", help="Draft a structured research brief")
    brief.add_argument("question")
    brief.add_argument("--language", default="en", choices=["en", "hi", "hinglish"])
    brief.add_argument("--out", help="Write the brief to this file")

    sub.add_parser("list", help="List every provision in the corpus")
    sub.add_parser("samples", help="List the sample legal outputs")

    args = parser.parse_args(argv)
    agent = _agent()

    if args.command == "ask":
        detail = agent.ask_detailed(args.question, args.language)
        if detail.ok:
            print(detail.answer)
            print()
            print("Citations:")
            for provision in detail.citations:
                print(f"  - {provision.title} ({provision.citation})")
            print(f"Mode: {detail.mode} · Model: {detail.model}")
        else:
            print(detail.error, file=sys.stderr)
            return 1
        return 0
    if args.command == "brief":
        text = agent.research_brief(args.question, args.language)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(text)
            print(f"Brief written to {args.out}")
        else:
            print(text)
        return 0
    if args.command == "list":
        for provision in agent.provisions:
            print(f"{provision.rel}: {provision.title} ({provision.citation})")
        print(f"{len(agent.provisions)} provisions.")
        return 0
    if args.command == "samples":
        for name in agent.list_samples(SAMPLES_ROOT):
            print(name)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
