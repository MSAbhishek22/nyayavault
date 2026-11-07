"""Tests: sample legal outputs — they exist, are labelled, and cite
only provisions that exist in the corpus (no invented sections)."""

import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.index import load_provisions

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "corpus")
SAMPLES = os.path.join(BASE, "samples")

# Section references of the form "s. 66C", "ss. 34–35", "Art 19" that
# a sample may cite. Every such reference must name a section that
# exists in the corpus.
SECTION_REF_RE = re.compile(r"\b(?:s|ss|Art|Article)\.?\s+([0-9][0-9A-Za-z()\-–]*)")


class TestSamples(unittest.TestCase):
    def setUp(self) -> None:
        self.provisions = load_provisions(CORPUS)
        self.sample_names = sorted(
            name for name in os.listdir(SAMPLES) if name.endswith(".md")
        )

    def test_three_samples_exist(self) -> None:
        self.assertEqual(len(self.sample_names), 3)
        self.assertIn("sample-research-brief-identity-theft.md", self.sample_names)
        self.assertIn("sample-research-brief-free-speech-online.md", self.sample_names)
        self.assertIn("sample-contract-summary-freelance-agreement.md", self.sample_names)

    def test_every_sample_carries_the_disclaimer(self) -> None:
        for name in self.sample_names:
            with open(os.path.join(SAMPLES, name), encoding="utf-8") as handle:
                text = handle.read()
            self.assertIn("not legal advice", text.lower(), name)

    def test_every_sample_cites_only_corpus_sections(self) -> None:
        # Section numbers that exist in the corpus, e.g. "66C", "10",
        # "2(7)", "34", "35".
        num_re = re.compile(r"\b(\d+[A-Za-z]?(?:\([a-z0-9]+\))*)")
        known = set()
        for provision in self.provisions:
            known |= set(num_re.findall(provision.section))
            known |= set(num_re.findall(provision.short_section))
        for name in self.sample_names:
            with open(os.path.join(SAMPLES, name), encoding="utf-8") as handle:
                text = handle.read()
            for match in SECTION_REF_RE.finditer(text):
                ref = match.group(1)
                # "(s. 10)" captures "10)" — strip a closing paren
                # that has no opening paren in the reference.
                if ref.endswith(")") and "(" not in ref:
                    ref = ref[:-1]
                # A reference may be a prefix of a known label
                # ("19(1)" of "19(1)(a)") or vice versa.
                ok = ref in known or any(
                    label.startswith(ref) or ref.startswith(label)
                    for label in known
                )
                self.assertTrue(ok, f"{name}: cites unknown section {ref!r}")

    def test_contract_sample_is_labelled_synthetic(self) -> None:
        with open(
            os.path.join(SAMPLES, "sample-contract-summary-freelance-agreement.md"),
            encoding="utf-8",
        ) as handle:
            text = handle.read()
        self.assertIn("SYNTHETIC", text)
        self.assertIn("fictional", text.lower())


if __name__ == "__main__":
    unittest.main()
