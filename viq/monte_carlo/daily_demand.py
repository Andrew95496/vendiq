import math
import random


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

if __name__ == "__main__":
    daily_demand = DailyDemand(average_daily_sales=5)
    print([daily_demand.draw_units_sold() for _ in range(10)])