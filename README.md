# The Baitome

Toward a Compositional and Mathematical Theory of Digital Bait.

Oxford's lexicographers chose "rage bait" as the word of the year for 2025, reporting a threefold rise in use, and the working vocabulary of the internet now names dozens of baits: clickbait, flamebait, fearbait, thirst bait, correction bait, dunk bait, FOMO bait, engagement bait. The names mix levels of description (a target action, an emotion, a social outcome, a platform objective, a deceptive relation), and one post can carry several of them. We treat named baits as compounds of psychological elements and build a four-layer system: about 32 candidate appraisal elements in 7 families, an alphabet of 12 actions, action-specific bonds between elements, and platform conditions acting as catalysts that multiply exposure without creating appraisal. A registry of 40 named baits as sparse formulas (mean size 3.3) has 0 formula collisions against 50 collisions in top-action space. Clustering compounds by simulated behavioral signature recovers the vernacular families at purity 0.6: ragebait forms a singleton cluster, and fearbait groups with phishing. The registry identifies linear element affinities (correlation 0.95), but the bond design is rank-deficient by 106 parameters, and 382 of 496 element pairs occur in no named compound. A held-out compound's signature is predicted from its formula with relative error 0.20, against 0.63 for the family mean, a test of internal consistency only. In an ecology of learning creators, habituating users and engagement ranking, ranking concentrates production and tilts the feed toward conflict; without habituation the conflict share locks at 0.64, and with it dominance changes 115 times. We specify the field programme and the criteria under which the periodic-table analogy would fail.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Seeded, bit-for-bit reproducible; calibration is structural and stated as such. Nineteen invariant checks fail the run loudly if broken, among them: the registry's shape and sparsity with zero formula collisions against measured action collisions; the family-recovery purity band; linear recoverability against the bond-design deficit; the empty-cell majority with the proposed cells present and ranked; the held-out ordering of compositional over family-mean over global prediction; and the ecology's concentration, feed tilt, diversity ordering, habituation cycling, and no-habituation lock.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build the-baitome`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
