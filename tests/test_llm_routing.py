"""Tests: mock provider + routing — deterministic, budget-counted."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.config import NyayaVaultConfig
from nyayavault.llm import MockProvider, extractive_answer
from nyayavault.routing import RoutingLedger, choose_primary_model, run_with_fallback

CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")


class TestMockProvider(unittest.TestCase):
    def test_extractive_answer_returns_corpus_sentence(self) -> None:
        context = (
            "# Section 66C\n\n"
            "## Statutory text (verbatim extract)\n\n"
            "> \"Whoever, fraudulently or dishonestly make use of the electronic "
            "signature, password or any other unique identification feature of "
            "any other person, shall be punished with imprisonment of either "
            "description for a term which may extend to three years.\""
        )
        answer = extractive_answer("what is identity theft", context)
        self.assertIn("fraudulently", answer)
        self.assertIn("password", answer)

    def test_extractive_answer_empty_context(self) -> None:
        self.assertEqual(extractive_answer("q", ""), "")

    def test_mock_never_invents(self) -> None:
        context = (
            "# Art 19\n\n"
            "## Statutory text (verbatim extract)\n\n"
            "Freedom of speech and expression is guaranteed to citizens under "
            "Article 19(1)(a) of the Constitution of India, subject to the "
            "reasonable restrictions listed in Article 19(2)."
        )
        result = MockProvider().ask("q", context)
        self.assertEqual(result.provider, "mock")
        self.assertIn("Freedom of speech", result.text)


class TestRouting(unittest.TestCase):
    def test_mock_primary_chosen_without_key(self) -> None:
        config = NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True)
        decision = choose_primary_model(config)
        self.assertEqual(decision.model, "mock-extractive")
        self.assertEqual(decision.provider, "mock")

    def test_mock_call_counts_one_unit(self) -> None:
        config = NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True)
        ledger = RoutingLedger(cap=10)
        result, decision = run_with_fallback(config, "q", "# T\n\nSome long enough sentence here for the mock.", "en", ledger)
        self.assertEqual(ledger.calls_used, 1)
        self.assertEqual(decision.provider, "mock")
        self.assertFalse(decision.fallback_used)

    def test_budget_exhausted_raises(self) -> None:
        config = NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True)
        ledger = RoutingLedger(cap=1)
        run_with_fallback(config, "q", "# T\n\nSome long enough sentence here for the mock.", "en", ledger)
        with self.assertRaises(RuntimeError):
            run_with_fallback(config, "q", "# T\n\nSome long enough sentence here for the mock.", "en", ledger)
        self.assertTrue(ledger.exhausted)


if __name__ == "__main__":
    unittest.main()
