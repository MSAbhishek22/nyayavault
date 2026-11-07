"""Tests: corpus index — load, search, grouping."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.index import list_by_act, load_provisions, search_provisions

CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")


class TestIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.provisions = load_provisions(CORPUS)

    def test_loads_all_seventeen(self) -> None:
        self.assertEqual(len(self.provisions), 17)

    def test_every_provision_has_act_section_source(self) -> None:
        for provision in self.provisions:
            self.assertTrue(provision.act, provision.rel)
            self.assertTrue(provision.section, provision.rel)
            self.assertTrue(provision.source.startswith("http"), provision.rel)
            self.assertTrue(provision.tags, provision.rel)

    def test_five_groups_present(self) -> None:
        grouped = list_by_act(self.provisions)
        self.assertEqual(len(grouped), 5)
        self.assertIn("Constitution of India, 1950", grouped)
        self.assertIn("Information Technology Act, 2000 (Act 21 of 2000)", grouped)
        self.assertIn("Consumer Protection Act, 2019 (Act 35 of 2019)", grouped)
        self.assertIn("Indian Contract Act, 1872 (Act 9 of 1872)", grouped)
        self.assertIn("Coverage notes", grouped)

    def test_search_password_theft_finds_66c(self) -> None:
        hits = search_provisions("someone stole my password and used my account", self.provisions)
        self.assertTrue(hits)
        self.assertEqual(hits[0].rel, "it-act-s66c.md")

    def test_search_free_speech_finds_article_19(self) -> None:
        hits = search_provisions("freedom of speech and expression online", self.provisions)
        self.assertTrue(hits)
        self.assertEqual(hits[0].rel, "constitution-art-19.md")

    def test_search_consumer_refund_finds_cpa(self) -> None:
        hits = search_provisions("seller refused my refund consumer complaint", self.provisions)
        self.assertTrue(hits)
        self.assertTrue(hits[0].rel.startswith("cpa-"))

    def test_search_broken_contract_finds_s73(self) -> None:
        hits = search_provisions("broken contract compensation damages breach", self.provisions)
        self.assertTrue(hits)
        self.assertIn(hits[0].rel, ("contract-s73.md", "contract-s10.md"))

    def test_search_dpdp_returns_coverage_note(self) -> None:
        # The corpus has a coverage note for the DPDP Act 2023, so a
        # question about it retrieves the note — not a guess from
        # another Act.
        hits = search_provisions("what does the DPDP Act 2023 say about a data breach", self.provisions)
        self.assertTrue(hits)
        self.assertEqual(hits[0].rel, "coverage-dpdp-act-2023.md")

    def test_search_truly_unknown_topic_returns_empty(self) -> None:
        hits = search_provisions("what is the punishment for murder under the IPC", self.provisions)
        self.assertEqual(hits, [])

    def test_search_is_deterministic(self) -> None:
        question = "identity theft password"
        first = [p.rel for p in search_provisions(question, self.provisions)]
        second = [p.rel for p in search_provisions(question, self.provisions)]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
