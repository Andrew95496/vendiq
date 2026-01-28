# machine_time_to_3_outs_sim.py

import numpy as np
from collections import Counter


class MachineTimeToThreeOutsSimulation:
    def __init__(
        self,
        items,
        number_of_simulations,
        max_days=365
    ):
        self.items = [
            item for item in items
            if not item["item_name"].lower().startswith("zz")
        ]
        self.number_of_simulations = number_of_simulations
        self.max_days = max_days

    def _sample_daily_demand(self, mean, std):
        demand = np.random.normal(mean, std)
        return max(demand, 0)

    def run(self):
        days_to_3_outs = []
        total_sales_at_3_outs = []
        out_counter = Counter()

        for _ in range(self.number_of_simulations):
            inventory = {
                item["item_name"]: item["par_level"]
                for item in self.items
            }

            outs = []
            days = 0
            cumulative_sales = 0

            while len(outs) < 3 and days < self.max_days:
                days += 1

                for item in self.items:
                    name = item["item_name"]

                    if name in outs:
                        continue

                    demand = self._sample_daily_demand(
                        item["avg_daily_sales"],
                        item["daily_std"]
                    )

                    sold = min(demand, inventory[name])
                    inventory[name] -= sold
                    cumulative_sales += sold

                    if inventory[name] <= 0:
                        inventory[name] = 0
                        outs.append(name)

                        if len(outs) == 3:
                            break

            days_to_3_outs.append(days)
            total_sales_at_3_outs.append(cumulative_sales)

            for name in outs[:3]:
                out_counter[name] += 1

        total_sims = self.number_of_simulations

        return {
            "avg_days_to_3_outs": float(np.mean(days_to_3_outs)),
            "p50_days": float(np.percentile(days_to_3_outs, 50)),
            "p75_days": float(np.percentile(days_to_3_outs, 75)),
            "p95_days": float(np.percentile(days_to_3_outs, 95)),
            "avg_sales_at_3_outs": float(np.mean(total_sales_at_3_outs)),
            "item_out_percentages": {
                item: count / total_sims
                for item, count in out_counter.items()
            }
        }
