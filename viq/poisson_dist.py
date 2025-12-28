import math
import random
import numpy as np


class DailyDemand:
    def __init__(self, average_daily_sales):
        self.average_daily_sales = average_daily_sales

    def draw_units_sold(self):
        cutoff_value = math.exp(-self.average_daily_sales)
        units_sold_today = 0
        random_product = 1.0

        while random_product > cutoff_value:
            units_sold_today += 1
            random_product *= random.random()

        return units_sold_today - 1


class AssetSimulator:
    def __init__(
        self,
        average_daily_sales,
        days_between_visits,
        lead_time_days,
        par_level,
        number_of_simulations
    ):
        self.average_daily_sales = average_daily_sales
        self.days_between_visits = days_between_visits
        self.lead_time_days = lead_time_days
        self.par_level = par_level
        self.number_of_simulations = number_of_simulations
        self.daily_demand = DailyDemand(average_daily_sales)

    def starting_inventory(self):
        return max(
            self.par_level
            - (self.average_daily_sales * self.lead_time_days),
            0
        )

    def run(self):
        cycle_totals = []
        stockouts = 0
        inventory_at_start = self.starting_inventory()

        for _ in range(self.number_of_simulations):
            total_units_sold = 0

            for _ in range(self.days_between_visits):
                total_units_sold += self.daily_demand.draw_units_sold()

            cycle_totals.append(total_units_sold)

            if total_units_sold > inventory_at_start:
                stockouts += 1

        return f'''\nstockout_probability: {stockouts / self.number_of_simulations}
        \nproduct_at_service: {1 - (stockouts / self.number_of_simulations)}
        \navg_demand: {np.mean(cycle_totals)}
        \np95_demand: {np.percentile(cycle_totals, 95)}
        \neffective_inventory: {math.floor(inventory_at_start)}'''

        


if __name__ == "__main__":
    item = AssetSimulator(
        average_daily_sales=4.74,
        days_between_visits=2,
        lead_time_days=2,
        par_level=21,
        number_of_simulations=10_000
    )

    result = item.run()
    print("Item:", result)
