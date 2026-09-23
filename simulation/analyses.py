"""The Baitome, computed.

Three mechanisms over the declared registry (registry.py):

1. The registry as a measured object. Level-mixing quantified: compound
   pairs that collide in action space against formula collisions; element
   usage; compression statistics.

2. The generative response model and the Mendeleev tests that can be run
   before field data exist. Compound signatures from affinities plus
   bonds; recovery of the vernacular families from behavioral signatures
   alone (cluster purity); identifiability of affinities and bonds from
   the named registry (the bond design is rank-deficient: the vernacular
   underdetermines the chemistry); the empty cells counted and ranked,
   locating the seed's two predicted unnamed compounds; held-out compound
   signature prediction against family-mean and global baselines, labeled
   as internal consistency of the framework, never as empirical
   validation.

3. The ecology. Creators learn by reinforcement over compounds, users
   habituate per element, engagement ranking multiplies exposure.
   Engagement ranking concentrates production and tilts it toward the
   conflict family; habituation makes dominance cyclical; a chronological
   control preserves diversity; freezing habituation freezes dominance.

Structural calibration throughout; the paper states it. Seeded and
bit-for-bit reproducible. Invariants fail the run.
"""
from __future__ import annotations

import numpy as np

import registry as R

SEED = 20260826
N_E = len(R.ELEMENTS)          # 32
N_A = len(R.ACTIONS)           # 12
NAMES = list(R.COMPOUNDS)
N_C = len(NAMES)               # 40
FAM_OF = {n: R.COMPOUNDS[n][0] for n in NAMES}


def _py(x):
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


def _beta() -> np.ndarray:
    B = np.zeros((N_E, N_A))
    for e, row in R.AFFINITY.items():
        for a, v in row.items():
            B[R.E[e], R.A[a]] = v
    return B


def _incidence() -> np.ndarray:
    M = np.zeros((N_C, N_E))
    for i, n in enumerate(NAMES):
        for e in R.COMPOUNDS[n][1]:
            M[i, R.E[e]] = 1.0
    return M


def _signatures(M: np.ndarray, B: np.ndarray) -> np.ndarray:
    L = M @ B
    for (e1, e2, a, s) in R.BONDS:
        both = M[:, R.E[e1]] * M[:, R.E[e2]]
        L[:, R.A[a]] += s * both
    return L


# ----------------------------------------------------------------------
# mechanism 1: the registry as a measured object
# ----------------------------------------------------------------------

def run_registry(M: np.ndarray, L: np.ndarray) -> dict:
    sizes = M.sum(axis=1)
    # formula collisions: identical element sets
    seen = {}
    fcoll = 0
    for i, n in enumerate(NAMES):
        key = tuple(sorted(R.COMPOUNDS[n][1]))
        fcoll += key in seen
        seen[key] = n
    # action collisions: identical top-2 action sets
    top2 = [tuple(sorted(np.argsort(-L[i])[:2])) for i in range(N_C)]
    acoll = 0
    for i in range(N_C):
        for j in range(i + 1, N_C):
            acoll += top2[i] == top2[j]
    used = (M.sum(axis=0) > 0)
    unused = [R.ELEMENTS[k] for k in range(N_E) if not used[k]]
    return {
        "n_elements": N_E,
        "n_actions": N_A,
        "n_compounds": N_C,
        "n_families": len(R.COMPOUND_FAMILIES),
        "mean_formula_size": float(sizes.mean()),
        "formula_collisions": int(fcoll),
        "top2_action_collisions": int(acoll),
        "n_compound_pairs": N_C * (N_C - 1) // 2,
        "elements_unused": unused,
        "n_elements_used": int(used.sum()),
    }


# ----------------------------------------------------------------------
# mechanism 2: periodicity, identifiability, empty cells, held-out
# ----------------------------------------------------------------------

def _kmeans(X, k, seed, iters=200, restarts=20):
    rng = np.random.default_rng(seed)
    best, best_inertia = None, np.inf
    for _ in range(restarts):
        idx = rng.choice(len(X), k, replace=False)
        C = X[idx].copy()
        for _ in range(iters):
            d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)
            lab = d.argmin(1)
            newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j]
                             for j in range(k)])
            if np.allclose(newC, C):
                break
            C = newC
        inertia = ((X - C[lab]) ** 2).sum()
        if inertia < best_inertia:
            best_inertia, best = inertia, lab.copy()
    return best


def run_periodicity(M: np.ndarray, B: np.ndarray, L: np.ndarray) -> dict:
    # z-score signatures so clustering sees shape, not magnitude
    Z = (L - L.mean(0)) / (L.std(0) + 1e-9)
    lab = _kmeans(Z, k=len(R.COMPOUND_FAMILIES), seed=SEED)
    fams = [FAM_OF[n] for n in NAMES]
    purity_n = 0
    misfiled = []
    for j in set(lab):
        members = [i for i in range(N_C) if lab[i] == j]
        counts = {}
        for i in members:
            counts[fams[i]] = counts.get(fams[i], 0) + 1
        major = max(counts, key=counts.get)
        purity_n += counts[major]
        misfiled += [NAMES[i] for i in members if fams[i] != major]
    purity = purity_n / N_C

    # identifiability: linear fit ignoring bonds
    Bhat, *_ = np.linalg.lstsq(M, L, rcond=None)
    used = M.sum(0) > 0
    corr = np.corrcoef(Bhat[used].ravel(), B[used].ravel())[0, 1]
    rank_M = int(np.linalg.matrix_rank(M))
    # pair design over realized pairs
    pairs = []
    pair_cols = []
    for i in range(N_E):
        for j in range(i + 1, N_E):
            col = M[:, i] * M[:, j]
            if col.any():
                pairs.append((R.ELEMENTS[i], R.ELEMENTS[j]))
                pair_cols.append(col)
    P = np.array(pair_cols).T if pair_cols else np.zeros((N_C, 0))
    full = np.hstack([M, P])
    rank_full = int(np.linalg.matrix_rank(full))
    n_pairs_total = N_E * (N_E - 1) // 2
    n_realized = len(pairs)
    n_params = N_E + n_realized

    # empty cells, ranked by best-action combined affinity
    empty = []
    realized_set = set(pairs)
    for i in range(N_E):
        for j in range(i + 1, N_E):
            key = (R.ELEMENTS[i], R.ELEMENTS[j])
            if key in realized_set:
                continue
            score = float((B[i] + B[j]).max())
            act = R.ACTIONS[int((B[i] + B[j]).argmax())]
            empty.append({"pair": list(key), "best_action": act,
                          "score": score})
    empty.sort(key=lambda d: -d["score"])
    # the seed's two predicted unnamed compounds
    def pair_rank(a, b):
        for r, d in enumerate(empty):
            if set(d["pair"]) == {a, b}:
                return r + 1
        return None
    seed_cells = {
        "VE_ER": pair_rank("VE", "ER"),
        "MM_TH": pair_rank("MM", "TH"),
    }
    # synthesis predictions for the two proposed compounds
    def predict(formula):
        m = np.zeros(N_E)
        for e in formula:
            m[R.E[e]] = 1.0
        v = m @ B
        for (e1, e2, a, s) in R.BONDS:
            if m[R.E[e1]] and m[R.E[e2]]:
                v[R.A[a]] += s
        top = np.argsort(-v)[:3]
        return {R.ACTIONS[t]: float(v[t]) for t in top}
    synth = {
        "praise-correction bait (VE+ER+CO)": predict(["VE", "ER", "CO"]),
        "nostalgic-threat bait (MM+TH+IN)": predict(["MM", "TH", "IN"]),
    }

    # held-out compound prediction (internal consistency)
    errs_comp, errs_fam, errs_glob = [], [], []
    for i in range(N_C):
        keep = [j for j in range(N_C) if j != i]
        Bh, *_ = np.linalg.lstsq(M[keep], L[keep], rcond=None)
        pred = M[i] @ Bh
        fam = FAM_OF[NAMES[i]]
        fam_rows = [j for j in keep if FAM_OF[NAMES[j]] == fam]
        fam_mean = L[fam_rows].mean(0)
        glob_mean = L[keep].mean(0)
        denom = np.linalg.norm(L[i]) + 1e-9
        errs_comp.append(np.linalg.norm(pred - L[i]) / denom)
        errs_fam.append(np.linalg.norm(fam_mean - L[i]) / denom)
        errs_glob.append(np.linalg.norm(glob_mean - L[i]) / denom)
    return {
        "family_recovery_purity": purity,
        "misfiled_compounds": misfiled,
        # cluster memberships reported for the prose (read-only view of the clustering above)
        "clusters": [[NAMES[i] for i in range(N_C) if lab[i] == j] for j in sorted(set(lab))],
        "ragebait_cluster_size": int(sum(1 for i in range(N_C) if lab[i] == lab[NAMES.index("ragebait")])),
        "linear_recovery_correlation": float(corr),
        "rank_incidence": rank_M,
        "n_elements_used": int(used.sum()),
        "pairs_total": n_pairs_total,
        "pairs_realized": n_realized,
        "pairs_empty": n_pairs_total - n_realized,
        "rank_full_design": rank_full,
        "n_params_linear_plus_realized_bonds": n_params,
        "bond_design_deficit": n_params - rank_full,
        "empty_cells_top10": empty[:10],
        "seed_predicted_cells_rank": seed_cells,
        "synthesis_predictions": synth,
        "heldout_relative_error": {
            "compositional": float(np.mean(errs_comp)),
            "family_mean": float(np.mean(errs_fam)),
            "global_mean": float(np.mean(errs_glob)),
        },
    }


# ----------------------------------------------------------------------
# mechanism 3: the ecology
# ----------------------------------------------------------------------

T_STEPS = 400
N_CREATORS = 60
ETA_HAB = 0.015        # susceptibility loss per unit exposure
RHO_REC = 0.01         # recovery toward full susceptibility
AMP = 2.0              # engagement-ranking amplification strength
Q_LR = 0.15            # creator learning rate
SOFTMAX_T = 0.25
ENGAGE_W = {"Rp": 1.3, "Sh": 1.3, "Qs": 1.2, "Rx": 1.0, "Ck": .8,
            "Dw": .6, "Or": .3, "Fo": .8, "Rt": .8, "Cv": .5, "Ds": .2,
            "Mb": .5}
CONFLICT = {"conflict"}


def _ecology(M, B, ranking: str, habituation: bool, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    w = np.array([ENGAGE_W[a] for a in R.ACTIONS])
    s = np.ones(N_E)                        # element susceptibilities
    Q = np.zeros((N_CREATORS, N_C))
    fam_idx = {f: [i for i, n in enumerate(NAMES) if FAM_OF[n] == f]
               for f in R.COMPOUND_FAMILIES}
    fam_share = {f: [] for f in R.COMPOUND_FAMILIES}
    feed_share = {f: [] for f in R.COMPOUND_FAMILIES}
    hhi_series, ent_series = [], []
    dominant = []
    for t in range(T_STEPS):
        probs = np.exp(Q / SOFTMAX_T)
        probs /= probs.sum(axis=1, keepdims=True)
        choice = np.array([rng.choice(N_C, p=probs[c])
                           for c in range(N_CREATORS)])
        counts = np.bincount(choice, minlength=N_C).astype(float)
        # per-exposure response with current susceptibilities
        Ms = M * s[None, :]
        Ls = Ms @ B
        for (e1, e2, a, st) in R.BONDS:
            Ls[:, R.A[a]] += st * Ms[:, R.E[e1]] * Ms[:, R.E[e2]]
        y = np.maximum(Ls, 0) @ w           # engagement yield per compound
        rel = y / (y.mean() + 1e-9)
        if ranking == "engagement":
            exposure = np.maximum(1.0 + AMP * (rel - 1.0), 0.1)
        else:
            exposure = np.ones(N_C)
        reward = y * exposure
        for c in range(N_CREATORS):
            k = choice[c]
            Q[c, k] += Q_LR * (reward[k] - Q[c, k])
        if habituation:
            exp_elem = (M[choice] * exposure[choice][:, None]).sum(0)
            exp_elem /= max(exp_elem.max(), 1e-9)
            s = np.clip(s - ETA_HAB * exp_elem + RHO_REC * (1 - s), 0.05, 1.0)
        share = counts / counts.sum()
        feed = counts * exposure
        feed = feed / feed.sum()
        for f in R.COMPOUND_FAMILIES:
            fam_share[f].append(float(share[fam_idx[f]].sum()))
            feed_share[f].append(float(feed[fam_idx[f]].sum()))
        hhi_series.append(float((share ** 2).sum()))
        nz = share[share > 0]
        ent_series.append(float(-(nz * np.log(nz)).sum()))
        dominant.append(int(counts.argmax()))
    # dominance switches over the second half (after learning warms up)
    half = T_STEPS // 2
    switches = 0
    run_dom = dominant[half]
    for d in dominant[half:]:
        if d != run_dom:
            switches += 1
            run_dom = d
    last = slice(T_STEPS - 100, T_STEPS)
    return {
        "hhi_mean_last100": float(np.mean(hhi_series[last])),
        "entropy_mean_last100": float(np.mean(ent_series[last])),
        "conflict_share_last100": float(np.mean(fam_share["conflict"][last])),
        "feed_conflict_share_last100": float(np.mean(feed_share["conflict"][last])),
        "dominance_switches_2nd_half": switches,
        "fam_share_series": {f: fam_share[f] for f in R.COMPOUND_FAMILIES},
        "feed_share_series": {f: feed_share[f] for f in R.COMPOUND_FAMILIES},
        "hhi_series": hhi_series,
    }


def run_ecology(M, B) -> dict:
    eng = _ecology(M, B, "engagement", habituation=True, seed=SEED)
    chron = _ecology(M, B, "chronological", habituation=True, seed=SEED)
    frozen = _ecology(M, B, "engagement", habituation=False, seed=SEED)
    return {
        "constants": {"T_STEPS": T_STEPS, "N_CREATORS": N_CREATORS,
                      "ETA_HAB": ETA_HAB, "RHO_REC": RHO_REC, "AMP": AMP,
                      "Q_LR": Q_LR, "SOFTMAX_T": SOFTMAX_T},
        "engagement": {k: v for k, v in eng.items()
                       if not k.endswith("_series")},
        "chronological": {k: v for k, v in chron.items()
                          if not k.endswith("_series")},
        "no_habituation": {k: v for k, v in frozen.items()
                           if not k.endswith("_series")},
        "_series": {"engagement": eng["fam_share_series"],
                    "engagement_feed": eng["feed_share_series"],
                    "chronological": chron["fam_share_series"],
                    "hhi_eng": eng["hhi_series"],
                    "hhi_chron": chron["hhi_series"]},
    }


# ----------------------------------------------------------------------
# cited records
# ----------------------------------------------------------------------

CITED_RECORDS = {
    "negativity_ctr_pct_per_word": {"value": 2.3,
        "source": "Robertson et al. 2023, Nat. Hum. Behav. 7: 812-822"},
    "clickbait_detector_agreement_pct": {"value": 47,
        "source": "Molina, Sundar, Rony and Hassan 2021, CHI"},
    "outgroup_sharing_multiplier": {"value": 2,
        "source": "Rathje, Van Bavel and van der Linden 2021, PNAS 118"},
    "ragebait_usage_multiplier_2025": {"value": 3,
        "source": "Oxford University Press, December 1, 2025"},
    "hybrid_model_n_users": {"value": 2696,
        "source": "Nature Communications 2026, 10.1038/s41467-026-73547-6"},
}


# ----------------------------------------------------------------------
# invariants and orchestration
# ----------------------------------------------------------------------

def _checks(reg, per, eco) -> dict:
    c = {}
    c["registry_shape"] = (reg["n_elements"] == 32 and reg["n_actions"] == 12
                           and reg["n_compounds"] == 40)
    c["formulas_all_distinct"] = reg["formula_collisions"] == 0
    c["labels_collide_in_action_space"] = reg["top2_action_collisions"] >= 30
    c["formulas_sparse"] = 2.5 <= reg["mean_formula_size"] <= 4.5
    c["most_elements_used"] = reg["n_elements_used"] >= 26
    c["family_recovery_substantial"] = per["family_recovery_purity"] >= 0.6
    c["family_recovery_imperfect"] = per["family_recovery_purity"] < 1.0
    c["linear_affinities_recoverable"] = per["linear_recovery_correlation"] > 0.85
    c["registry_underdetermines_bonds"] = per["bond_design_deficit"] > 0
    c["most_cells_empty"] = per["pairs_empty"] > per["pairs_total"] // 2
    c["seed_cells_present"] = all(v is not None
                                  for v in per["seed_predicted_cells_rank"].values())
    c["heldout_compositional_beats_family"] = (
        per["heldout_relative_error"]["compositional"]
        < per["heldout_relative_error"]["family_mean"])
    c["heldout_family_beats_global"] = (
        per["heldout_relative_error"]["family_mean"]
        < per["heldout_relative_error"]["global_mean"])
    c["engagement_concentrates"] = (eco["engagement"]["hhi_mean_last100"]
                                    > eco["chronological"]["hhi_mean_last100"])
    c["engagement_tilts_the_feed_to_conflict"] = (
        eco["engagement"]["feed_conflict_share_last100"]
        > eco["chronological"]["feed_conflict_share_last100"])
    c["production_tilt_weaker_than_feed_tilt"] = (
        (eco["engagement"]["feed_conflict_share_last100"]
         - eco["chronological"]["feed_conflict_share_last100"])
        > (eco["engagement"]["conflict_share_last100"]
           - eco["chronological"]["conflict_share_last100"]))
    c["chronological_preserves_diversity"] = (
        eco["chronological"]["entropy_mean_last100"]
        > eco["engagement"]["entropy_mean_last100"])
    c["habituation_cycles_dominance"] = (
        eco["engagement"]["dominance_switches_2nd_half"] >= 2)
    c["frozen_susceptibility_freezes_dominance"] = (
        eco["no_habituation"]["dominance_switches_2nd_half"]
        <= eco["engagement"]["dominance_switches_2nd_half"] // 2)
    return c


def run() -> dict:
    B = _beta()
    M = _incidence()
    L = _signatures(M, B)
    reg = run_registry(M, L)
    per = run_periodicity(M, B, L)
    eco = run_ecology(M, B)
    checks = _checks(reg, per, eco)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    eco_out = {k: v for k, v in eco.items() if k != "_series"}
    return _py({
        "registry": reg,
        "periodicity": per,
        "ecology": eco_out,
        "cited_records": CITED_RECORDS,
        "constants": {"SEED": SEED},
        "checks": checks,
    }), {"M": M, "B": B, "L": L, "eco_series": eco["_series"]}
