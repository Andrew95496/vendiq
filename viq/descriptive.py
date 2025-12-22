import pandas as pd
from loader import ExcelLoader

pd.set_option("display.float_format", "{:.0f}".format)


class Baseline:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def average_weekly_sales(self) -> pd.DataFrame:
        numeric_df = self.df.select_dtypes(include="number")

        baseline_df = pd.DataFrame({
            "item_name": self.df.iloc[:, 0],
            "avg_units_per_week": numeric_df.mean(axis=1)
        })

        return baseline_df


if __name__ == "__main__":

    loader = ExcelLoader("samples/sales-2.xlsx")
    df = loader.load()

    baseline = Baseline(df)
    result = baseline.average_weekly_sales()

    print(result)