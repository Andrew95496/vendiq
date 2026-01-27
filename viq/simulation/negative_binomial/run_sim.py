# run_sim.py

import pandas as pd

from asset_sim import AssetSimulation
from stats_utils import get_month_columns, daily_stats_since_launch


if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    DAYS_BETWEEN_VISITS = 21
    LEAD_TIME_DAYS = 2
    SIMS = 10_000

    df_main = pd.read_excel("/Users/andrewleacock1/Downloads/10191.xlsx")
    df_par  = pd.read_excel("/Users/andrewleacock1/Downloads/10191_par.xlsx")

    month_columns = get_month_columns(df_main)

    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError("Missing par column")

    par_lookup = df_par.set_index("Item Name")[par_col]

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
    # PRINT SUMMARY
    # -----------------------------
    for r in results:
        print("=" * 60)
        print(r["item_name"])
        print(f"Avg Daily Sales:      {r['avg_daily_sales']}")
        print(f"Daily Std:            {r['daily_std']}")
        print(f"P95 Cycle Demand:     {r['p95_cycle_demand']}")
        print(f"Avg Cycle Demand:     {r['avg_cycle_demand']}")
        print(f"Effective Inventory: {r['effective_inventory']}")
        print(f"Availability:        {r['availability']:.2%}")
        print(f"Stockout Prob:       {r['stockout_probability']:.2%}")
        print(f"Current Par Level:   {r['current_par_level']}")
    print("=" * 60)

    # -----------------------------
    # EXPORT SIMULATED SALES
    # -----------------------------
    df_sales = pd.DataFrame(sales_rows)

    df_sales.to_excel(
        "/Users/andrewleacock1/Downloads/simulated_sales_10191.xlsx",
        index=False
    )
