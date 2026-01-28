# stats_utils.py

import re
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
            return daily.mean(), daily.std(ddof=1)

    return 0.0, 0.0
