# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 24 CSL entries. 1 resolved through doi.org (turner2026), 15 matched in Crossref, aubin2025 completed from its DOI record (10.1038/s41598-024-81575-9, article 994), and 7 entered by hand (brehm1966, cialdini1984, simon1971, tajfel1979, mendeleev1869, meta2017, oup2025 renamed from oxford2025; the two web documents re-fetched). In-text citations converted to Pandoc [@id]; legacy list replaced by the citeproc list.
- Bibliographic corrections: molina2021 has six authors in the Crossref record (Molina, Sundar, Rony, Hassan, Le, Lee), the legacy entry four; aubin2025 gained its DOI and article number; meta2017 dated 18 December 2017 from the page. No prose change (the text cites "Molina et al.").
- analyses.py: added read-only fields /periodicity/clusters and /periodicity/ragebait_cluster_size so the cluster statements in the prose are checkable; every pre-existing value unchanged.
- claims.yaml: 62 claims (40 computation, 11 source, 5 interpretation, 3 definition, 2 assumption, 1 normative). Source claims checked against Crossref/OpenAlex abstracts (Robertson et al., Molina et al., Rathje et al., Lerner and Keltner, Turner et al., Aubin Le Quéré and Matias, Gray et al., Reynolds and John, Luo et al., Lindström et al., Brady et al. 2021) and the re-fetched OUP and Meta pages.
- Unverified, not bound: Pennycook et al. (no abstract retrievable; the "one-line accuracy prompt" statement rests on the original verification), Crockett (2017) outrage economics (no abstract), Moors et al. and the Cialdini/Brehm/Tajfel/Simon attributions (conceptual, book-level).
- Execution receipt: run id baitome (verification/baitome.json), `uv run python run_all.py`, 19/19 invariants, all prior results.json values reproduced.
- metadata claims_target: claim-ledger.

## 2026-09-22 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, Prior evidence, Five measures of bait, Elements, cues, actions and catalysts, Behavioral signatures and family recovery, Identifiability of the registry, Creator-user-platform ecology, Field programme and failure criteria, Ethics and dual use, Objections, Falsification, Conclusion, Reproducibility).

Corrections found during the pass:
  - The bond-design parameter count was stated as 145; results.json gives 146 (periodicity.n_params_linear_plus_realized_bonds), and the stated deficit of 106 = 146 - 40 already used 146. Text corrected.
  - The 2026 hybrid reward-learning-and-habit study was cited as "(Nature Communications, 2026)" with the journal as author. Crossref (10.1038/s41467-026-73547-6) gives Turner, Gunschera, Subrahmanya, Salecha, Eichstaedt, Palminteri and Orben, volume 17, article 7170; the in-text citation and the bibliography entry now name them.
  - The Mendeleev figure title referred to "the seed's two proposals"; now "two proposed compounds".
results.json unchanged by the figure edits.

## 2026-08-26 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 24 entries verified against Crossref or the live record. Seed corrections logged in research.md: the CHI citation resolved to Molina, Sundar, Rony and Hassan (2021) with the 47 percent detector-agreement figure; the concreteness study resolved to Aubin Le Quéré and Matias (2025); the "2026 follow-up" resolved to the Nature Communications hybrid reward-learning-and-habit model with n 2,696; the Cart Narcs study resolved to Reynolds and John (2026); the seed's game-theoretic clickbait and German-handbook recommender citations were unresolvable as given and dropped, with the SIGIR counterfactual paper carrying the exposure-response point; the seed's 8 psychological families consolidated to 7, since its own compound formulas dissolve the eighth into epistemic and status elements.
  - Simulation design iterations logged: the registry initially held 41 compounds against the declared 40 (one near-duplicate dropped); the chronological arm's exposure was a scalar where an array was needed; and the conflict-tilt invariant as first written compared production shares, which do not tilt, because habituation erodes exactly the elements the amplifier rewards. The corrected metric separates feed composition from production composition, and the separation became a finding: ranking changes what is seen more than what is made.
  - Honest results kept rather than tuned away: the seed's two proposed unnamed compounds rank 148 and 160 of 382 empty cells, mid-table, behind combinations like dread-curiosity that no one proposed; family-recovery purity is 0.6 with instructive misfilings rather than a triumphant match; the held-out prediction result is labeled internal consistency of a self-generated world, never validation; and the no-habituation counterfactual, the feed locking onto conflict at 0.64, is presented with its converse, that habituating users dissolve the tilt into churn, so the model disciplines the dystopia it is usually invoked to support.
  - Voice: draft came in at 0 errors, 7 review-candidates; all 7 rewritten; a 23-sentence run without a short sentence broken to 15; "load-separated" removed.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 24 in-text keys, 24 bib entries, 0 missing, 0 unused
  - claims: 53 sim values, 16 decimal claims in prose, 0 without a match
  - build: 12 pages, no missing-character warnings
  - simulation: 19/19 invariants
  - check => PASS
