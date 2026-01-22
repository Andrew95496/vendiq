import math
import re
import numpy as np
import pandas as pd

from daily_demand import DailyDemand


# -----------------------------
# CONFIGURABLE MODEL CONSTANTS
# -----------------------------
DAYS_PER_MONTH = 30
DAYS_BETWEEN_VISITS = 14
LEAD_TIME_DAYS = 2
SIMS = 10_000


# -----------------------------
# MONTE CARLO CLASS (UNCHANGED)
# -----------------------------
class ItemRestockingMonteCarlo:
    def __init__(
        self,
        item_name,
        average_daily_sales,
        days_between_visits,
        lead_time_days,
        par_level,
        number_of_simulations
    ):
        self.item_name = item_name
        self.average_daily_sales = average_daily_sales
        self.days_between_visits = days_between_visits
        self.lead_time_days = lead_time_days
        self.par_level = par_level
        self.number_of_simulations = number_of_simulations
        self.daily_demand = DailyDemand(average_daily_sales)

    def __on_hand__(self):
        return max(
            self.par_level
            - (self.average_daily_sales * self.lead_time_days),
            0
        )

    def sim(self):
        cycle_totals = []
        stockouts = 0
        inventory_at_start = self.__on_hand__()

        for _ in range(self.number_of_simulations):
            total_units_sold = 0

            for _ in range(self.days_between_visits):
                total_units_sold += self.daily_demand._units_sold_()

            cycle_totals.append(total_units_sold)

            if total_units_sold > inventory_at_start:
                stockouts += 1

        return {
            "item_name": self.item_name,
            "avg_daily_sales_used": round(self.average_daily_sales, 4),
            "p95_cycle_demand": float(np.percentile(cycle_totals, 95)),
            "average_cycle_demand": int(np.mean(cycle_totals)),
            "effective_inventory": math.floor(inventory_at_start),
            "availability": 1 - (stockouts / self.number_of_simulations),
            "stockout_probability": stockouts / self.number_of_simulations,
        }


# -----------------------------
# HELPERS
# -----------------------------
def get_month_columns(df):
    pattern = re.compile(r"^\d{2}/\d{4}$")
    return [c for c in df.columns if pattern.match(str(c))]


def compute_avg_daily_sales_after_first_sale(row, month_columns):
    monthly_sales = (
    pd.to_numeric(row[month_columns], errors="coerce")
    .fillna(0.0)
    .values
)

    first_sale_idx = None
    for i, val in enumerate(monthly_sales):
        if val > 0:
            first_sale_idx = i
            break

    if first_sale_idx is None:
        return 0.0

    valid_sales = monthly_sales[first_sale_idx:]
    total_units = valid_sales.sum()
    total_days = len(valid_sales) * DAYS_PER_MONTH

    return total_units / total_days


def display_results(results):
    for r in results:
        print("=" * 60)
        print(r["item_name"])
        print(f"Avg Daily Sales Used: {r['avg_daily_sales_used']}")
        print(f"P95 Cycle Demand:     {r['p95_cycle_demand']:.1f}")
        print(f"Avg Cycle Demand:     {r['average_cycle_demand']}")
        print(f"Effective Inventory: {r['effective_inventory']}")
        print(f"Availability:        {r['availability']:.2%}")
        print(f"Stockout Prob:       {r['stockout_probability']:.2%}")
    print("=" * 60)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    # load files (YOUR paths)
    df_main = pd.read_excel(
        "/Users/andrewleacock1/Downloads/15432.xlsx",
        header=11
    )

    df_par = pd.read_excel(
        "/Users/andrewleacock1/Downloads/15432_par.xlsx",
        header=11
    )

    # detect month columns dynamically
    month_columns = get_month_columns(df_main)

    # par lookup (no merge)
    par_lookup = (
        df_par
        .set_index("Item Name")["Vending Par Level"]
    )

    df_main["Par Level"] = (
        df_main["Item Name"]
        .map(par_lookup)
        .fillna(0)
        .astype(int)
    )

    results = []

    for _, row in df_main.iterrows():

        avg_daily_sales = compute_avg_daily_sales_after_first_sale(
            row=row,
            month_columns=month_columns
        )

        if avg_daily_sales <= 0:
            continue

        mc = ItemRestockingMonteCarlo(
            item_name=row["Item Name"],
            average_daily_sales=avg_daily_sales,
            days_between_visits=DAYS_BETWEEN_VISITS,
            lead_time_days=LEAD_TIME_DAYS,
            par_level=row["Par Level"],
            number_of_simulations=SIMS
        )

        results.append(mc.sim())

    display_results(results)
