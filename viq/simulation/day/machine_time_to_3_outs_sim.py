import numpy as np
from collections import Counter
import math


class MachineTimeToThreeOutsSimulation:
    """
    Simulates vending machine performance between services.

    No restocking occurs.

    Tracks:
    - Days until 3 items run out
    - Days until cumulative sales reach vend_threshold
    - Whether 120 vends is even achievable before collapse
    """

    def __init__(
        self,
        items,
        number_of_simulations,
        max_days=365,
        vend_threshold=120
    ):
        # Remove placeholder SKUs
        self.items = [
            item for item in items
            if not item["item_name"].lower().startswith("zz")
        ]

        self.number_of_simulations = number_of_simulations
        self.max_days = max_days
        self.vend_threshold = vend_threshold

        # Convert item data to NumPy arrays for performance
        self.item_names = np.array(
            [item["item_name"] for item in self.items]
        )

        self.means = np.array(
            [item["avg_daily_sales"] for item in self.items],
            dtype=float
        )

        self.stds = np.array(
            [item["daily_std"] for item in self.items],
            dtype=float
        )

        self.pars = np.array(
            [item["par_level"] for item in self.items],
            dtype=float
        )

        self.n_items = len(self.items)

    def run(self):

        sims = self.number_of_simulations
        max_days = self.max_days

        days_to_3_outs = np.zeros(sims)
        days_to_120_vends = np.full(sims, np.nan)

        vends_at_3_outs = np.zeros(sims)
        outs_at_120_vends = np.zeros(sims)

        hit_120_before_3 = 0
        hit_120_total = 0

        out_counter = Counter()

        for sim in range(sims):

            # Start fully stocked
            inventory = self.pars.copy()
            outs = np.zeros(self.n_items, dtype=bool)

            cumulative_sales = 0.0
            day_3 = None
            day_120 = None

            for day in range(1, max_days + 1):

                # Generate daily demand per SKU
                demand = np.random.normal(self.means, self.stds)
                demand = np.where(demand < 0, 0, demand)

                # Sales limited by available inventory
                sold = np.minimum(demand, inventory)

                inventory -= sold
                cumulative_sales += sold.sum()

                # Detect newly exhausted SKUs
                new_outs = (inventory <= 0) & (~outs)

                if new_outs.any():
                    indices = np.where(new_outs)[0]
                    for idx in indices:
                        out_counter[self.item_names[idx]] += 1

                outs |= new_outs

                # First time 3 items are out
                if day_3 is None and outs.sum() >= 3:
                    day_3 = day
                    vends_at_3_outs[sim] = cumulative_sales

                # First time cumulative sales reach threshold
                if day_120 is None and cumulative_sales >= self.vend_threshold:
                    day_120 = day
                    outs_at_120_vends[sim] = outs.sum()
                    hit_120_total += 1

                # If inventory completely depleted, stop simulation
                if inventory.sum() <= 0:
                    break

                # Stop early if both milestones reached
                if day_3 is not None and day_120 is not None:
                    break

            if day_3 is None:
                day_3 = max_days

            if day_120 is not None:
                days_to_120_vends[sim] = day_120

            if day_120 is not None and day_120 <= day_3:
                hit_120_before_3 += 1

            days_to_3_outs[sim] = day_3

        # Determine correct reporting for 120 vends
        if hit_120_total == 0:
            avg_days_to_120 = "Cannot reach 120 vends between services"
            avg_outs_at_120 = None
        else:
            avg_days_to_120 = int(np.ceil(np.nanmean(days_to_120_vends)))
            avg_outs_at_120 = int(np.ceil(np.nanmean(outs_at_120_vends)))

        # Compute item-level out probabilities
        item_out_percentages = {
            item: count / sims
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
            "avg_days_to_3_outs": int(np.floor(np.mean(days_to_3_outs))),
            "avg_days_to_120_vends": avg_days_to_120,
            "prob_120_vends_before_3_outs": hit_120_before_3 / sims,
            "avg_vends_at_3_outs": int(np.ceil(np.mean(vends_at_3_outs))),
            "avg_outs_at_120_vends": avg_outs_at_120,
            "item_out_percentages": item_out_percentages,
            "top_10_items_to_run_out": top_10_out_items
        }
