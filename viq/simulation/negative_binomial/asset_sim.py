# asset_sim.py

import math
import numpy as np
from daily_demand import DailyDemand


class AssetSimulation:
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
        self.days_between_visits = days_between_visits
        self.lead_time_days = lead_time_days
        self.par_level = par_level
        self.number_of_simulations = number_of_simulations

        self.demand = DailyDemand(avg_daily_sales, daily_std)
        self.avg_daily_sales = avg_daily_sales
        self.daily_std = daily_std

    def _effective_inventory(self):
        return math.floor(
            max(
                self.par_level
                - (self.avg_daily_sales * self.lead_time_days),
                0
            )
        )

    def run(self):
        inventory = self._effective_inventory()
        cycle_totals = []
        stockouts = 0

        for _ in range(self.number_of_simulations):
            sold = sum(
                self.demand.sample()
                for _ in range(self.days_between_visits)
            )
            cycle_totals.append(sold)

            if sold > inventory:
                stockouts += 1

        cycle_totals = np.array(cycle_totals)

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

            # ✅ THIS FIXES EVERYTHING
            "simulated_sales": cycle_totals.tolist()
        }
