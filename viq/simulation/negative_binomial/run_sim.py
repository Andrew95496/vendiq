# run_sim.py

import pandas as pd

from asset_sim import AssetSimulation
from stats_utils import get_month_columns, daily_stats_since_launch


# -----------------------------
# ANSI COLORS
# -----------------------------
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    DAYS_BETWEEN_VISITS = 21
    LEAD_TIME_DAYS = 2
    SIMS = 10_000

    df_main = pd.read_excel(
        "/Users/andrewleacock1/Downloads/14414.xlsx",
        header=12
    )

    df_par = pd.read_excel(
        "/Users/andrewleacock1/Downloads/14414_par.xlsx",
        header=12
    )

    month_columns = get_month_columns(df_main)

    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError("Missing par column")

    if "Capacity" not in df_par.columns:
        raise ValueError("Missing Capacity column")

    par_lookup = df_par.set_index("Item Name")[par_col]
    capacity_lookup = df_par.set_index("Item Name")["Capacity"]

    results = []
    sales_rows = []

    for _, row in df_main.iterrows():
        item = row["Item Name"]

        if item not in par_lookup:
            continue

        mean, std = daily_stats_since_launch(
            row,
            month_columns,
            DAYS_PER_MONTH
        )

        if mean <= 0:
            continue

        sim = AssetSimulation(
            item_name=item,
            avg_daily_sales=mean,
            daily_std=std,
            days_between_visits=DAYS_BETWEEN_VISITS,
            lead_time_days=LEAD_TIME_DAYS,
            par_level=int(par_lookup[item]),
            number_of_simulations=SIMS
        )

        result = sim.run()
        results.append(result)

        for i, demand in enumerate(result["simulated_sales"]):
            sales_rows.append({
                "Item Name": item,
                "Simulation": i + 1,
                "Cycle Demand": demand,
                "Par Level": result["current_par_level"],
                "Avg Daily Sales": result["avg_daily_sales"],
                "Daily Std": result["daily_std"]
            })

    # -----------------------------
    # PRINT SUMMARY WITH FLAGS
    # -----------------------------
    for r in results:
        item = r["item_name"]
        capacity = capacity_lookup.get(item)
        par = r["current_par_level"]

        color = RESET

        if capacity is not None:
            # RED: avg demand physically exceeds capacity
            if r["avg_cycle_demand"] > capacity:
                color = RED

            # YELLOW: tail risk exceeds capacity
            elif r["p95_cycle_demand"] > capacity:
                color = YELLOW

            # GREEN: sim says raise par AND capacity allows it
            elif (
                r["avg_cycle_demand"] > par
                and r["p95_cycle_demand"] > par
                and capacity > par
            ):
                color = GREEN

        print(color + "=" * 60)
        print(item)
        print(f"Avg Daily Sales:      {r['avg_daily_sales']}")
        print(f"Daily Std:            {r['daily_std']}")
        print(f"Avg Cycle Demand:     {r['avg_cycle_demand']}")
        print(f"P95 Cycle Demand:     {r['p95_cycle_demand']}")
        print(f"Current Par Level:   {par}")
        print(f"Capacity:             {capacity}")
        print(f"Effective Inventory: {r['effective_inventory']}")
        print(f"Availability:        {r['availability']:.2%}")
        print(f"Stockout Prob:       {r['stockout_probability']:.2%}")
        print("=" * 60 + RESET)

    # -----------------------------
    # EXPORT SIMULATED SALES
    # -----------------------------
    df_sales = pd.DataFrame(sales_rows)

    df_sales.to_csv(
        "/Users/andrewleacock1/Downloads/simulated_sales_255.csv",
        index=False
    )
