import numpy as np
import pandas as pd
from colorama import Fore, Style, init

from machine_time_to_3_outs_sim import MachineTimeToThreeOutsSimulation
from stats_utils import get_month_columns, daily_stats_since_launch

init(autoreset=True)


if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    SIMS = 10_000

    # -------------------------
    # LOAD DATA
    # -------------------------

    df_main = pd.read_excel("/Users/andrewleacock1/Downloads/3853.xlsx")
    df_par  = pd.read_excel("/Users/andrewleacock1/Downloads/3853_par.xlsx")

    month_columns = get_month_columns(df_main)

    # -------------------------
    # PAR COLUMN RESOLUTION
    # -------------------------

    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError("Missing par column")

    par_lookup = df_par.set_index("Item Name")[par_col]

    # -------------------------
    # BUILD ITEMS (HARD GUARDED)
    # -------------------------

    items = []
    dropped_nan = 0
    dropped_zero = 0

    for _, row in df_main.iterrows():
        item = row["Item Name"]

        # Skip ZZ items
        if not isinstance(item, str) or item.lower().startswith("zz"):
            continue

        # Skip if no par
        if item not in par_lookup:
            continue

        mean, std = daily_stats_since_launch(
            row,
            month_columns,
            DAYS_PER_MONTH
        )

        # -------- HARD GUARDS --------
        if mean is None or std is None:
            dropped_nan += 1
            continue

        if not np.isfinite(mean) or not np.isfinite(std):
            dropped_nan += 1
            continue

        if mean <= 0:
            dropped_zero += 1
            continue

        par = par_lookup[item]

        if not np.isfinite(par) or par <= 0:
            continue
        # --------------------------------

        items.append({
            "item_name": item,
            "avg_daily_sales": float(mean),
            "daily_std": float(std),
            "par_level": int(par)
        })

    if not items:
        raise RuntimeError("No valid items after filtering. Simulation aborted.")

    # -------------------------
    # RUN SIMULATION
    # -------------------------

    sim = MachineTimeToThreeOutsSimulation(
        items=items,
        number_of_simulations=SIMS
    )

    result = sim.run()

    # -------------------------
    # OUTPUT
    # -------------------------

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "MACHINE TIME TO 3 OUTS")
    print(Fore.CYAN + "=" * 60)

    print(Fore.WHITE + "Avg Days to 3 Outs: " + Style.BRIGHT + Fore.YELLOW + f"{result['avg_days_to_3_outs']:.1f}")
    print(Fore.WHITE + "P50 Days:           " + Style.BRIGHT + Fore.GREEN  + f"{result['p50_days']:.0f}")
    print(Fore.WHITE + "P75 Days:           " + Style.BRIGHT + Fore.MAGENTA + f"{result['p75_days']:.0f}")
    print(Fore.WHITE + "P95 Days:           " + Style.BRIGHT + Fore.RED     + f"{result['p95_days']:.0f}")
    print(Fore.WHITE + "Avg Sales @ 3 Outs: " + Style.BRIGHT + Fore.YELLOW + f"{result['avg_sales_at_3_outs']:.1f}")

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "TOP 10 ITEMS MOST FREQUENTLY IN 3 OUTS")
    print(Fore.CYAN + "=" * 60)

    for i, (item, pct) in enumerate(
        sorted(
            result["item_out_percentages"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10],
        start=1
    ):
        print(
            f"{Style.BRIGHT}{Fore.CYAN}{i:>2}. "
            f"{Fore.WHITE}{item:<30} "
            f"{Style.BRIGHT}{Fore.YELLOW}{pct:.1%}"
        )

    print(Fore.CYAN + "=" * 60)

    print(
        Fore.WHITE
        + f"Dropped items (NaN stats): {dropped_nan} | "
        + f"Dropped items (zero mean): {dropped_zero}"
    )
