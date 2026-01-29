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
        self.par_level = int(par_level)
        self.number_of_simulations = number_of_simulations

        # DailyDemand.sample() RETURNS AN INT (rounded up or down stochastically)
        self.demand = DailyDemand(avg_daily_sales, daily_std)
        self.avg_daily_sales = avg_daily_sales
        self.daily_std = daily_std

    def _effective_inventory(self):
        x = self.par_level - (self.avg_daily_sales * self.lead_time_days)
        if x <= 0:
            return 0

        base = int(np.floor(x))
        return base + (np.random.rand() < (x - base))

    def run(self):
        cycle_totals = []
        stockouts = 0
        effective_inventories = []

        for _ in range(self.number_of_simulations):
            inventory = self._effective_inventory()
            effective_inventories.append(inventory)

            # INTEGER SALES ONLY
            sold = sum(
                int(self.demand.sample())
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

            # ALL INTEGERS
            "p95_cycle_demand": int(np.percentile(cycle_totals, 95)),
            "avg_cycle_demand": int(round(np.mean(cycle_totals))),
            "effective_inventory": int(round(np.mean(effective_inventories))),

            "availability": 1 - stockouts / self.number_of_simulations,
            "stockout_probability": stockouts / self.number_of_simulations,
            "current_par_level": self.par_level,

            "simulated_sales": cycle_totals.tolist()
        }
