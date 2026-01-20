import math
import numpy as np
from pprint import pprint

from daily_demand import DailyDemand

'''Module to simulate asset inventory and stockouts using Monte Carlo simulation'''

class CycleSimulator:
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
    "soldout": stockouts / self.number_of_simulations,
    "availability": 1 - (stockouts / self.number_of_simulations),
    "average_cycle_demand": int(np.mean(cycle_totals)),
    "p95_cycle_demand": float(np.percentile(cycle_totals, 95)),
    "effective_inventory": math.floor(inventory_at_start)
}
        
if __name__ == "__main__":
    simulator = CycleSimulator(
        average_daily_sales=1,
        days_between_visits=30,
        lead_time_days=2,
        par_level=20,
        number_of_simulations=100000
    )
    results = simulator.sim()
    pprint(results)