"""Tests: legal agent — grounded answers, citations, grounded refusal."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.agent import LegalAgent
from nyayavault.config import NyayaVaultConfig

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "corpus")


def _agent(cap: int = 10) -> LegalAgent:
    return LegalAgent(NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True, daily_call_cap=cap))


class TestAgentAsk(unittest.TestCase):
    def test_identity_theft_answer_is_grounded_and_cited(self) -> None:
        agent = _agent()
        detail = agent.ask_detailed("Someone stole my password and used my account. What does Indian law say?")
        self.assertTrue(detail.ok)
        self.assertTrue(detail.answer.startswith("[mock]"))
        self.assertIn("not legal advice", detail.answer)
        rels = [p.rel for p in detail.citations]
        self.assertIn("it-act-s66c.md", rels)
        self.assertEqual(detail.mode, "mock")

    def test_free_speech_answer_cites_article_19(self) -> None:
        agent = _agent()
        detail = agent.ask_detailed("Can the government restrict free speech online?")
        self.assertTrue(detail.ok)
        rels = [p.rel for p in detail.citations]
        self.assertIn("constitution-art-19.md", rels)

    def test_section_66a_question_answers_void(self) -> None:
        agent = _agent()
        detail = agent.ask_detailed("Is section 66A of the IT Act still valid law?")
        self.assertTrue(detail.ok)
        rels = [p.rel for p in detail.citations]
        self.assertIn("it-act-s66a-void.md", rels)

    def test_dpdp_question_refuses_groundedly(self) -> None:
        agent = _agent()
        detail = agent.ask_detailed("What does the DPDP Act 2023 say about a data breach?")
        self.assertFalse(detail.ok)
        self.assertEqual(detail.mode, "refused")
        self.assertIn("not in the NyayaVault corpus", detail.error)

    def test_refusal_costs_no_budget(self) -> None:
        agent = _agent()
        agent.ask_detailed("What does the DPDP Act 2023 say about a data breach?")
        self.assertEqual(agent.ledger.calls_used, 0)

    def test_secret_in_question_refused_by_guardrail(self) -> None:
        agent = _agent()
        detail = agent.ask_detailed("password: hunter2hunter2, is it stolen?")
        self.assertFalse(detail.ok)
        self.assertIn("secret", detail.error)

    def test_budget_cap_blocks_third_call(self) -> None:
        agent = _agent(cap=2)
        question = "Someone stole my password and used my account."
        self.assertTrue(agent.ask_detailed(question).ok)
        self.assertTrue(agent.ask_detailed(question).ok)
        third = agent.ask_detailed(question)
        self.assertFalse(third.ok)
        self.assertIn("budget", third.error)

    def test_ask_returns_plain_text(self) -> None:
        agent = _agent()
        text = agent.ask("What is a contract under Indian law?")
        self.assertIn("contract", text.lower())


class TestResearchBrief(unittest.TestCase):
    def test_brief_has_all_sections(self) -> None:
        agent = _agent()
        brief = agent.research_brief("Someone stole my password and used my account.")
        for heading in ("## Short answer", "## What the law says", "## What is NOT covered", "## Next steps"):
            self.assertIn(heading, brief)
        self.assertIn("Section 66C", brief)  # citation present
        self.assertIn("not legal advice", brief)

    def test_brief_for_unanswerable_question_states_no_answer(self) -> None:
        agent = _agent()
        brief = agent.research_brief("What does the DPDP Act 2023 say about a data breach?")
        self.assertIn("not in the NyayaVault corpus", brief)
        self.assertIn("## What is NOT covered", brief)


if __name__ == "__main__":
    unittest.main()
