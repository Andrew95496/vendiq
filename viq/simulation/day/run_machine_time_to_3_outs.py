import numpy as np
import pandas as pd
from colorama import Fore, Style, init

from machine_time_to_3_outs_sim import MachineTimeToThreeOutsSimulation
from stats_utils import get_month_columns, daily_stats_since_launch

init(autoreset=True)


if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    SIMS = 10_000

    df_main = pd.read_excel("/Users/andrewleacock1/Downloads/3853.xlsx")
    df_par  = pd.read_excel("/Users/andrewleacock1/Downloads/3853_par.xlsx")

    month_columns = get_month_columns(df_main)

    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError("Missing par column")

    par_lookup = df_par.set_index("Item Name")[par_col]

    items = []

    for _, row in df_main.iterrows():
        item = row["Item Name"]

        if not isinstance(item, str) or item.lower().startswith("zz"):
            continue

        if item not in par_lookup:
            continue

        mean, std = daily_stats_since_launch(
            row,
            month_columns,
            DAYS_PER_MONTH
        )

        if (
            mean is None
            or std is None
            or not np.isfinite(mean)
            or not np.isfinite(std)
            or mean <= 0
        ):
            continue

        par = par_lookup[item]

        if not np.isfinite(par) or par <= 0:
            continue

        items.append({
            "item_name": item,
            "avg_daily_sales": float(mean),
            "daily_std": float(std),
            "par_level": int(par)
        })

    if not items:
        raise RuntimeError("No valid items after filtering")

    sim = MachineTimeToThreeOutsSimulation(
        items=items,
        number_of_simulations=SIMS
    )

    result = sim.run(return_raw=True)

    df_sims = pd.DataFrame(result["raw_simulations"])
    csv_path = "machine_time_to_3_outs_simulations.csv"
    df_sims.to_csv(csv_path, index=False)

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "MACHINE TIME TO 3 OUTS")
    print(Fore.CYAN + "=" * 60)

    print(Fore.WHITE + "Avg Days to 3 Outs: " + Style.BRIGHT + Fore.YELLOW + f"{result['avg_days_to_3_outs']:.1f}")
    print(Fore.WHITE + "P50 Days:           " + Style.BRIGHT + Fore.GREEN  + f"{result['p50_days']:.0f}")
    print(Fore.WHITE + "P75 Days:           " + Style.BRIGHT + Fore.MAGENTA + f"{result['p75_days']:.0f}")
    print(Fore.WHITE + "P95 Days:           " + Style.BRIGHT + Fore.RED     + f"{result['p95_days']:.0f}")
    print(Fore.WHITE + "Avg Sales @ 3 Outs: " + Style.BRIGHT + Fore.YELLOW + f"{result['avg_sales_at_3_outs']:.1f}")

    print(Fore.CYAN + "=" * 60)
