# daily_demand.py
import numpy as np


class DailyDemand:
    def __init__(self, avg_daily_sales, daily_std):
        self.avg = avg_daily_sales
        self.std = daily_std

        var = daily_std ** 2
        if var > avg_daily_sales and avg_daily_sales > 0:
            self.r = (avg_daily_sales ** 2) / (var - avg_daily_sales)
            self.p = self.r / (self.r + avg_daily_sales)
            self.use_negbin = True
        else:
            self.use_negbin = False

    def sample(self):
        if self.use_negbin:
            return np.random.negative_binomial(self.r, self.p)
        return np.random.poisson(self.avg)
