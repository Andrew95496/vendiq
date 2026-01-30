# machine_time_to_3_outs_sim.py

import numpy as np
from collections import Counter
import math


class MachineTimeToThreeOutsSimulation:
    def __init__(
        self,
        items,
        number_of_simulations,
        max_days=365,
        vend_threshold=120
    ):
        self.items = [
            item for item in items
            if not item["item_name"].lower().startswith("zz")
        ]
        self.number_of_simulations = number_of_simulations
        self.max_days = max_days
        self.vend_threshold = vend_threshold

    def _sample_daily_demand(self, mean, std):
        if not np.isfinite(mean) or mean <= 0:
            return 0.0
        if not np.isfinite(std) or std <= 0:
            return float(mean)
        x = np.random.normal(mean, std)
        return max(x, 0.0) if np.isfinite(x) else 0.0

    def run(self):
        days_to_3_outs = []
        days_to_120_vends = []

        vends_at_3_outs = []
        outs_at_120_vends = []

        hit_120_before_3 = 0
        out_counter = Counter()

        for _ in range(self.number_of_simulations):

            inventory = {
                item["item_name"]: float(item["par_level"])
                for item in self.items
            }

            outs = []
            cumulative_sales = 0.0

            day_3 = None
            day_120 = None
            sales_at_3 = None
            outs_at_120 = None

            for day in range(1, self.max_days + 1):
                daily_sales = 0.0

                for item in self.items:
                    name = item["item_name"]
                    demand = self._sample_daily_demand(
                        item["avg_daily_sales"],
                        item["daily_std"]
                    )

                    daily_sales += demand

                    if name not in outs:
                        sold = min(demand, inventory[name])
                        inventory[name] -= sold
                        if inventory[name] <= 0:
                            outs.append(name)
                            if len(outs) <= 3:
                                out_counter[name] += 1

                cumulative_sales += daily_sales

                if day_3 is None and len(outs) >= 3:
                    day_3 = day
                    sales_at_3 = cumulative_sales

                if day_120 is None and cumulative_sales >= self.vend_threshold:
                    day_120 = day
                    outs_at_120 = len(outs)

                if day_3 is not None and day_120 is not None:
                    break

            if day_3 is None:
                day_3 = self.max_days
                sales_at_3 = cumulative_sales

            if day_120 is None:
                day_120 = self.max_days
                outs_at_120 = len(outs)

            if day_120 <= day_3:
                hit_120_before_3 += 1

            days_to_3_outs.append(day_3)
            days_to_120_vends.append(day_120)
            vends_at_3_outs.append(sales_at_3)
            outs_at_120_vends.append(outs_at_120)

        item_out_percentages = {
            item: count / self.number_of_simulations
            for item, count in out_counter.items()
        }

        top_10_out_items = dict(
            sorted(
                item_out_percentages.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        )

        return {
            "avg_days_to_3_outs": int(math.floor(np.mean(days_to_3_outs))),
            "avg_days_to_120_vends": int(math.ceil(np.mean(days_to_120_vends))),

            "p50_days": float(np.percentile(days_to_3_outs, 50)),
            "p75_days": float(np.percentile(days_to_3_outs, 75)),
            "p95_days": float(np.percentile(days_to_3_outs, 95)),

            "p50_days_to_120_vends": float(np.percentile(days_to_120_vends, 50)),
            "p75_days_to_120_vends": float(np.percentile(days_to_120_vends, 75)),
            "p95_days_to_120_vends": float(np.percentile(days_to_120_vends, 95)),

            "avg_vends_at_3_outs": int(math.ceil(np.mean(vends_at_3_outs))),
            "avg_outs_at_120_vends": int(math.ceil(np.mean(outs_at_120_vends))),

            "prob_120_vends_before_3_outs": hit_120_before_3 / self.number_of_simulations,

            "item_out_percentages": item_out_percentages,
            "top_10_items_to_run_out": top_10_out_items
        }
