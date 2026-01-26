import math
import re
import numpy as np
import pandas as pd

from viq.simulation.poisson.daily_demand import DailyDemand


# -----------------------------
# MONTE CARLO CLASS
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
            "current_par_level": self.par_level
        }


# -----------------------------
# HELPERS
# -----------------------------
def get_month_columns(df):
    pattern = re.compile(r"^\d{2}/\d{4}$")
    return [c for c in df.columns if pattern.match(str(c))]


def compute_avg_daily_sales_after_first_sale(row, month_columns, days_per_month):
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
    total_days = len(valid_sales) * days_per_month

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
        print(f"Current Par Level:   {r['current_par_level']}")
    print("=" * 60)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    # -----------------------------
    # CONFIG
    # -----------------------------
    DAYS_PER_MONTH = 30
    DAYS_BETWEEN_VISITS = 3
    LEAD_TIME_DAYS = 2
    SIMS = 10_000

    # -----------------------------
    # LOAD DATA (YOUR PATHS)
    # -----------------------------
    df_main = pd.read_excel(
        "/Users/andrewleacock1/Downloads/276.xlsx"
    )

    df_par = pd.read_excel(
        "/Users/andrewleacock1/Downloads/276_par.xlsx"
    )


    # -----------------------------
    # DETECT MONTH COLUMNS
    # -----------------------------
    month_columns = get_month_columns(df_main)

    # -----------------------------
    # PAR LOOKUP
    # Presence in df_par == in machine
    # -----------------------------
    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError(
            "Par file must contain either 'Vending Par Level' or 'MM Par'"
        )

    par_lookup = (
        df_par
        .set_index("Item Name")[par_col]
    )

    # -----------------------------
    # RUN SIMS (ONLY ITEMS IN MACHINE)
    # -----------------------------
    results = []

    for _, row in df_main.iterrows():

        item_name = row["Item Name"]

        # NOT IN PAR FILE -> NOT IN MACHINE
        if item_name not in par_lookup:
            continue

        avg_daily_sales = compute_avg_daily_sales_after_first_sale(
            row=row,
            month_columns=month_columns,
            days_per_month=DAYS_PER_MONTH
        )

        if avg_daily_sales <= 0:
            continue

        mc = ItemRestockingMonteCarlo(
            item_name=item_name,
            average_daily_sales=avg_daily_sales,
            days_between_visits=DAYS_BETWEEN_VISITS,
            lead_time_days=LEAD_TIME_DAYS,
            par_level=int(par_lookup[item_name]),
            number_of_simulations=SIMS
        )

        results.append(mc.sim())

    # -----------------------------
    # OUTPUT
    # -----------------------------
    display_results(results)
