# The Baitome

Toward a Compositional and Mathematical Theory of Digital Bait. The internet's bait vocabulary, clickbait, ragebait, flamebait, fearbait, FOMO bait, engagement bait and dozens more, mixes levels: some names describe a target action, some an emotion, some a social outcome, some a platform objective, some a deceptive relation. This paper proposes that named baits are compounds rather than elements and builds the periodic system the claim requires: 32 candidate appraisal elements in 7 families, an action alphabet of 12, action-specific bonds, platform conditions as catalysts, and a registry of 40 named compounds as sparse formulas. The structure is then computed. The names collide 50 times in top-action space against 0 formula collisions; play is the registry's noble gas, an element no named bait uses. Clustering compounds by behavioral signature alone recovers the vernacular families at purity 0.6, and the failures teach: ragebait is a cluster of one, fearbait files with phishing in a fear-and-return group, intelligence bait is clickbait in dress clothes. The registry identifies linear element affinities at correlation 0.95 while leaving the bond design rank-deficient by 106 parameters, and 382 of 496 element pairs appear in no named compound: the vocabulary cannot identify most of its own chemistry, and the ranked empty cells become a synthesis list on which dread-curiosity outranks the paper's own two proposals. A held-out compound's signature is predictable from its formula at relative error 0.20 against 0.63 for the family mean, stated as internal consistency rather than validation. An ecology of reinforcement-learning creators, habituating users, and engagement ranking prices the catalysis: ranking concentrates production and tilts the feed toward conflict, and without habituation the feed locks onto conflict at 0.64 and never leaves, while habituating users dissolve the tilt into churn at 115 dominance switches. The rage-farming dystopia assumes non-habituating users; the ecosystem's own damper is fatigue. Five separated quantities, efficacy, intent, deception, autonomy gap, and harm, keep the ethics measurable, and the Mendeleev criteria with explicit kill conditions keep the periodic claim falsifiable.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build the-baitome`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
