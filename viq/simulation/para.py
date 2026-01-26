import math
import re
import numpy as np
import pandas as pd


# -----------------------------
# SIMULATION CLASS
# -----------------------------
class ItemRestockingSimulation:
    def __init__(
        self,
        item_name,
        avg_daily_sales,
        daily_std,
        days_between_visits,
        lead_time_days,
        par_level,
        number_of_simulations
    ):
        self.item_name = item_name
        self.avg_daily_sales = avg_daily_sales
        self.daily_std = daily_std
        self.days_between_visits = days_between_visits
        self.lead_time_days = lead_time_days
        self.par_level = par_level
        self.number_of_simulations = number_of_simulations

        # set up distribution params once
        var = daily_std ** 2
        if var > avg_daily_sales and avg_daily_sales > 0:
            self.r = (avg_daily_sales ** 2) / (var - avg_daily_sales)
            self.p = self.r / (self.r + avg_daily_sales)
            self.use_negbin = True
        else:
            self.use_negbin = False

    def _daily_sales(self):
        if self.use_negbin:
            return np.random.negative_binomial(self.r, self.p)
        else:
            return np.random.poisson(self.avg_daily_sales)

    def _on_hand(self):
        return max(
            self.par_level - (self.avg_daily_sales * self.lead_time_days),
            0
        )

    def sim(self):
        inventory = math.floor(self._on_hand())
        cycle_totals = []
        stockouts = 0

        for _ in range(self.number_of_simulations):
            sold = sum(
                self._daily_sales()
                for _ in range(self.days_between_visits)
            )
            cycle_totals.append(sold)
            if sold > inventory:
                stockouts += 1

        return {
            "item_name": self.item_name,
            "avg_daily_sales": round(self.avg_daily_sales, 4),
            "daily_std": round(self.daily_std, 4),
            "p95_cycle_demand": int(np.percentile(cycle_totals, 95)),
            "avg_cycle_demand": int(np.mean(cycle_totals)),
            "effective_inventory": inventory,
            "availability": 1 - stockouts / self.number_of_simulations,
            "stockout_probability": stockouts / self.number_of_simulations,
            "current_par_level": self.par_level,
        }


# -----------------------------
# HELPERS
# -----------------------------
def get_month_columns(df):
    pattern = re.compile(r"^\d{2}/\d{4}$")
    return [c for c in df.columns if pattern.match(str(c))]


def daily_stats_since_launch(row, month_columns, days_per_month):
    monthly = (
        pd.to_numeric(row[month_columns], errors="coerce")
        .fillna(0.0)
        .values
    )

    for i, v in enumerate(monthly):
        if v > 0:
            daily = monthly[i:] / days_per_month
            return daily.mean(), daily.std(ddof=1)

    return 0.0, 0.0


def display_results(results):
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
# MAIN
# -----------------------------
if __name__ == "__main__":

    DAYS_PER_MONTH = 30
    DAYS_BETWEEN_VISITS = 21
    LEAD_TIME_DAYS = 2
    SIMS = 10_000

    df_main = pd.read_excel("/Users/andrewleacock1/Downloads/19367.xlsx")
    df_par  = pd.read_excel("/Users/andrewleacock1/Downloads/19367_par.xlsx")

    month_columns = get_month_columns(df_main)

    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError("Missing par column")

    par_lookup = df_par.set_index("Item Name")[par_col]

    results = []

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

        sim = ItemRestockingSimulation(
            item_name=item,
            avg_daily_sales=mean,
            daily_std=std,
            days_between_visits=DAYS_BETWEEN_VISITS,
            lead_time_days=LEAD_TIME_DAYS,
            par_level=int(par_lookup[item]),
            number_of_simulations=SIMS
        )

        results.append(sim.sim())

    display_results(results)
