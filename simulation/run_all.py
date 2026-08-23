"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. Seeded; a rerun
reproduces every number bit for bit. A failed invariant fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results, aux = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_table, plot_mendeleev, plot_ecology
    plot_table(results, aux, str(OUT / "figures" / "table.png"))
    plot_mendeleev(results, aux, str(OUT / "figures" / "mendeleev.png"))
    plot_ecology(results, aux, str(OUT / "figures" / "ecology.png"))

    reg = results["registry"]
    print(f"registry: {reg['n_compounds']} compounds over {reg['n_elements']} "
          f"elements, mean formula {reg['mean_formula_size']:.2f}; "
          f"{reg['formula_collisions']} formula collisions, "
          f"{reg['top2_action_collisions']} action collisions; unused: "
          f"{reg['elements_unused']}")
    p = results["periodicity"]
    print(f"periodicity: purity {p['family_recovery_purity']:.2f}, linear "
          f"recovery r {p['linear_recovery_correlation']:.3f}, pairs "
          f"{p['pairs_realized']}/{p['pairs_total']} realized, bond deficit "
          f"{p['bond_design_deficit']}; seed cells rank "
          f"{p['seed_predicted_cells_rank']}")
    print(f"  held-out error: compositional "
          f"{p['heldout_relative_error']['compositional']:.3f}, family mean "
          f"{p['heldout_relative_error']['family_mean']:.3f}, global "
          f"{p['heldout_relative_error']['global_mean']:.3f}")
    e = results["ecology"]
    for arm in ("engagement", "chronological", "no_habituation"):
        v = e[arm]
        print(f"  {arm}: hhi {v['hhi_mean_last100']:.3f}, entropy "
              f"{v['entropy_mean_last100']:.2f}, feed conflict "
              f"{v['feed_conflict_share_last100']:.3f}, switches "
              f"{v['dominance_switches_2nd_half']}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
