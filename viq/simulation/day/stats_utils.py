# stats_utils.py

import re
import numpy as np
import pandas as pd


def get_month_columns(df):
    pattern = re.compile(r"^\d{2}/\d{4}$")
    return [c for c in df.columns if pattern.match(str(c))]


def daily_stats_since_launch(row, month_columns, days_per_month):
    monthly = (
        pd.to_numeric(row[month_columns], errors="coerce")
        .fillna(0.0)
        .values
    )

    for i, v in enumerate(monthly):
        if v > 0:
            daily = monthly[i:] / days_per_month

            n = len(daily)

            # increasing weights so most recent month is weighted highest
            weights = np.arange(1, n + 1)

            # weighted mean
            weighted_mean = np.average(daily, weights=weights)

            # weighted standard deviation
            weighted_var = np.average(
                (daily - weighted_mean) ** 2,
                weights=weights
            )
            weighted_std = np.sqrt(weighted_var)

            return weighted_mean, weighted_std

    return 0.0, 0.0
