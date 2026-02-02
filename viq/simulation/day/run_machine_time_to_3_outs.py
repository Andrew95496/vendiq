import numpy as np
import pandas as pd
from colorama import Fore, Style, init

from machine_time_to_3_outs_sim import MachineTimeToThreeOutsSimulation
from stats_utils import get_month_columns, daily_stats_since_launch

init(autoreset=True)

if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    SIMS = 10_000

    df_main = pd.read_excel("/Users/andrewleacock1/Downloads/12717.xlsx", header=12)
    df_par  = pd.read_excel("/Users/andrewleacock1/Downloads/12717_par.xlsx", header=12)

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
            row, month_columns, DAYS_PER_MONTH
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

    sim = MachineTimeToThreeOutsSimulation(
        items=items,
        number_of_simulations=SIMS
    )

    result = sim.run()

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "MACHINE TIME / SALES / OUTS")
    print(Fore.CYAN + "=" * 60)

    print(
        Fore.WHITE
        + "Avg Days to 3 Outs: "
        + Style.BRIGHT
        + Fore.YELLOW
        + f"{result['avg_days_to_3_outs']}"
    )

    print(
        Fore.WHITE
        + "Avg Vends @ 3 Outs: "
        + Style.BRIGHT
        + Fore.YELLOW
        + f"{result['avg_vends_at_3_outs']}"
    )

    print(Fore.CYAN + "-" * 60)

    print(
        Fore.WHITE
        + "Avg Days to 120 Vends: "
        + Style.BRIGHT
        + Fore.YELLOW
        + f"{result['avg_days_to_120_vends']}"
    )

    print(
        Fore.WHITE
        + "Avg Outs @ 120 Vends: "
        + Style.BRIGHT
        + Fore.YELLOW
        + f"{result['avg_outs_at_120_vends']}"
    )

    print(Fore.CYAN + "-" * 60)

    print(
        Fore.WHITE
        + "P(120 Vends Before 3 Outs): "
        + Style.BRIGHT
        + Fore.YELLOW
        + f"{result['prob_120_vends_before_3_outs']:.1%}"
    )

    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "TOP ITEMS TO RUN OUT (FIRST 3)")
    print(Fore.CYAN + "=" * 60)

    for i, (item, pct) in enumerate(
        result["top_10_items_to_run_out"].items(), 1
    ):
        print(
            f"{Style.BRIGHT}{Fore.CYAN}{i:>2}. "
            f"{Fore.WHITE}{item:<30} "
            f"{Style.BRIGHT}{Fore.YELLOW}{pct:.1%}"
        )

    print(Fore.CYAN + "=" * 60)
