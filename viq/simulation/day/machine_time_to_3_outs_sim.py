import numpy as np
from collections import Counter


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
            return 0

        if not np.isfinite(std) or std <= 0:
            return int(round(mean))

        demand = np.random.normal(mean, std)

        if not np.isfinite(demand):
            return 0

        return max(int(round(demand)), 0)

    def run(self):
        days_3_outs = []
        days_120 = []

        hit_120_before_3 = 0

        out_counter = Counter()

        for _ in range(self.number_of_simulations):

            inventory = {
                item["item_name"]: item["par_level"]
                for item in self.items
            }

            outs = set()
            days = 0

            cumulative_sales = 0

            day_3 = None
            day_120 = None

            while days < self.max_days:
                days += 1

                for item in self.items:
                    name = item["item_name"]

                    demand = self._sample_daily_demand(
                        item["avg_daily_sales"],
                        item["daily_std"]
                    )

                    # SALES ALWAYS COUNT
                    cumulative_sales += demand

                    # INVENTORY ONLY FOR OUT DETECTION
                    if name not in outs:
                        sold = min(demand, inventory[name])
                        inventory[name] -= sold

                        if inventory[name] <= 0:
                            outs.add(name)
                            out_counter[name] += 1

                if day_3 is None and len(outs) >= 3:
                    day_3 = days

                if day_120 is None and cumulative_sales >= self.vend_threshold:
                    day_120 = days

                if day_3 is not None and day_120 is not None:
                    break

            if day_3 is None:
                day_3 = self.max_days

            if day_120 is None:
                day_120 = self.max_days

            if day_120 <= day_3:
                hit_120_before_3 += 1

            days_3_outs.append(day_3)
            days_120.append(day_120)

        return {
            "avg_days_to_3_outs": float(np.mean(days_3_outs)),
            "avg_days_to_120_vends": float(np.mean(days_120)),

            "p50_days": float(np.percentile(days_3_outs, 50)),
            "p75_days": float(np.percentile(days_3_outs, 75)),
            "p95_days": float(np.percentile(days_3_outs, 95)),

            "p50_days_to_3_outs": float(np.percentile(days_3_outs, 50)),
            "p75_days_to_3_outs": float(np.percentile(days_3_outs, 75)),
            "p95_days_to_3_outs": float(np.percentile(days_3_outs, 95)),

            "p50_days_to_120_vends": float(np.percentile(days_120, 50)),
            "p75_days_to_120_vends": float(np.percentile(days_120, 75)),
            "p95_days_to_120_vends": float(np.percentile(days_120, 95)),

            "prob_120_vends_before_3_outs": hit_120_before_3 / self.number_of_simulations,

            "item_out_percentages": {
                item: count / self.number_of_simulations
                for item, count in out_counter.items()
            }
        }
