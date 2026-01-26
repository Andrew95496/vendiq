# viq/simulation/daily_sales.py
import numpy as np


class DailySalesGenerator:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

        var = std ** 2
        if var > mean and mean > 0:
            self.r = (mean ** 2) / (var - mean)
            self.p = self.r / (self.r + mean)
            self.use_negbin = True
        else:
            self.use_negbin = False

    def sample(self):
        if self.use_negbin:
            return np.random.negative_binomial(self.r, self.p)
        return np.random.poisson(self.mean)
