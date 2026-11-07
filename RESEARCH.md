# NyayaVault — Research Log

**Date:** 8 Nov 2026 (research pass, ~00:00–00:45 IST)
**Researcher:** subagent (depth 1), for M S Abhishek
**Rule:** every corpus fact must be verified against an official or
Gazette source and cited. No invented case law, section numbers, or
judgments. Summaries are labelled as summaries, never as statute text.

## Corpus verification table

Every document in `corpus/` was checked against the sources below
during this pass. "Verbatim" means the quoted words were read in the
source text during this pass; "summary" means a plain-language
restatement, labelled as such in the document.

| # | Document | Act / Section | Verified against | What was verified |
|---|---|---|---|---|
| 1 | constitution-art-14.md | Constitution, Art 14 | India Code / Legislative Department text via aipgp.in (reference copy of the official text); testbook.com | Verbatim: "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India." |
| 2 | constitution-art-19.md | Constitution, Art 19(1)(a) + 19(2) | legalserviceindia.com (official English text, consolidated to 78th Amendment); theindianconstitution.com; juristco.com | Verbatim 19(1)(a) and the full 19(2) grounds list (sovereignty and integrity; security of the State; friendly relations; public order; decency or morality; contempt of court; defamation; incitement to an offence). Art 19 rights are for citizens only. Sub-clause (f) omitted by the 44th Amendment, 1978. |
| 3 | constitution-art-21.md | Constitution, Art 21 | testbook.com; sooperkanoon.com | Verbatim: "No person shall be deprived of his life or personal liberty except according to procedure established by law." Maneka Gandhi v. Union of India (1978) named as the landmark Art 21 case. |
| 4 | constitution-art-32.md | Constitution, Art 32 | testbook.com | Art 32 gives the right to move the Supreme Court for enforcement of Fundamental Rights, through the five writs: habeas corpus, mandamus, prohibition, certiorari, quo warranto. Dr B. R. Ambedkar called it the "heart and soul" of the Constitution. |
| 5 | it-act-s43.md | IT Act 2000, s. 43 | dpdpindia.in; cyberlawacademy.com | Civil liability: unauthorised access, download, virus, damage, denial of access, etc., without the owner's permission; damages by way of compensation, not exceeding ₹1 crore. Distinct from criminal s. 66. |
| 6 | it-act-s66.md | IT Act 2000, s. 66 | dpdpindia.in; cyberlawacademy.com | Whoever dishonestly or fraudulently does any act in s. 43: imprisonment up to 3 years, or fine up to ₹5 lakh, or both. |
| 7 | it-act-s66c.md | IT Act 2000, s. 66C | courtkutchehry.com (bare Act text) | Verbatim: fraudulent/dishonest use of another person's electronic signature, password or unique identification feature — up to 3 years and fine up to ₹1 lakh. |
| 8 | it-act-s66d.md | IT Act 2000, s. 66D | courtkutchehry.com (bare Act text) | Verbatim: cheating by personation by means of a computer resource or communication device — up to 3 years and fine up to ₹1 lakh. |
| 9 | it-act-s79.md | IT Act 2000, s. 79 | cybercrimehelpdesk.com; cyberlawacademy.com | Safe harbour: an intermediary is not liable for third-party information/data/link it hosts, if it observes due diligence and acts on notice (court/government). Conditional immunity, not a punishment. |
| 10 | it-act-s66a-void.md | IT Act 2000, s. 66A — VOID | dpdpindia.in; cyberlawacademy.com | CASE NOTE, not live law: s. 66A was struck down in its entirety by the Supreme Court in Shreya Singhal v. Union of India (2015) 5 SCC 1, as violating Art 19(1)(a). Void and unenforceable. |
| 11 | cpa-s2-definitions.md | CPA 2019, s. 2(7) + s. 2(9) | Gazette of India (soolegal.com copy of the Gazette); aaptaxlaw.com | Verbatim s. 2(7) "consumer" (buys goods / hires services for consideration; not for resale or commercial purpose). Verbatim s. 2(9) six "consumer rights". |
| 12 | cpa-s34-35-complaint.md | CPA 2019, ss. 34–35 | vidhijudicial.com; aaptaxlaw.com | s. 34: District Commission pecuniary limit — Act text ₹1 crore, operative limit ₹50 lakh under the 2021 Jurisdiction Rules; territorial grounds incl. where the complainant resides or personally works for gain (s. 34(2)(d)). s. 35: who may file (consumer; recognised association; group of consumers with permission; Central/State Government or Central Authority); complaint may be filed electronically. |
| 13 | cpa-s69-limitation.md | CPA 2019, s. 69 | Gazette of India; thelaw.institute | Complaint must be filed within two years from the date the cause of action arises; delay may be condoned for sufficient cause. |
| 14 | contract-s10.md | Contract Act 1872, ss. 2(h), 10 | bnblegal.com (bare Act); klelawcollege.edu.in | s. 2(h): "An agreement enforceable by law is a contract." Verbatim s. 10: free consent, competent parties, lawful consideration, lawful object, not expressly declared void. |
| 15 | contract-s73.md | Contract Act 1872, s. 73 | bnblegal.com; klelawcollege.edu.in | Verbatim s. 73 (first paragraph): compensation for loss naturally arising in the usual course of things, or which the parties knew was likely to result; no compensation for remote and indirect loss. |
| 16 | case-note-anuradha-bhasin.md | Anuradha Bhasin (2020) | juristco.com | CASE NOTE: Anuradha Bhasin v. Union of India (2020) 3 SCC 637 — access to the internet is protected under Art 19(1)(a); blanket internet shutdowns must satisfy proportionality. |
| 17 | coverage-dpdp-act-2023.md | Coverage note — DPDP Act 2023, NOT in the corpus | India Code (indacode.nic.in) — the Act exists there; the note records its absence from this corpus | Boundary marker, not a law: the DPDP Act 2023 is not in the corpus; the note exists so a question about it gets a grounded "not covered" answer instead of a guess borrowed from another Act (e.g. "breach" in Contract Act s. 73). |

## What was deliberately NOT included

- **No case law beyond two verified case notes.** The corpus has no
  judgments database; the app must never present a case it has not
  verified. Both case notes are labelled CASE NOTE, not statute.
- **No Section 66A as live law.** It is in the corpus only as a
  "void" note, so the app can answer "is s. 66A still valid?" with
  the correct answer (no) instead of hallucinating it as live.
- **No state amendments, no rules text, no 2023 DPDP Act.** The DPDP
  Act 2023 now governs much of personal-data protection; the corpus
  does not cover it, and the app must refuse questions about it
  rather than guess. (Future corpus expansion, not this build.)
- **No legal advice.** Every answer and sample carries "general
  legal information, not legal advice".

## Sources used (all fetched 7–8 Nov 2026)

- India Code — indiacode.nic.in (official statute portal)
- Legislative Department text via aipgp.in/constitution (reference
  copy, s. 52(1)(q) Copyright Act 1957)
- Gazette of India, Consumer Protection Act 2019 (No. 35 of 2019)
- courtkutchehry.com bare Act (IT Act 2000)
- bnblegal.com / klelawcollege.edu.in bare Act (Contract Act 1872)
- dpdpindia.in, cyberlawacademy.com, cybercrimehelpdesk.com (IT Act
  explainers, cross-checked against the bare Act text)
- aaptaxlaw.com, vidhijudicial.com, thelaw.institute,
  centurylawfirm.in (CPA 2019 explainers, cross-checked against the
  Gazette text)
- legalserviceindia.com, theindianconstitution.com, juristco.com,
  aspirantdaily.com (Constitution text and Art 19 analysis)
- testbook.com, sooperkanoon.com (Constitution article summaries,
  cross-checked)

## Design references (see design/DESIGN_REFERENCES.md)

Indian Kanoon, SCC Online, Harvey AI, PRS Legislative Research,
CourtListener — inspected 7 Nov 2026 via text fetch; visual layout
not verified from this environment (noted honestly per reference).
