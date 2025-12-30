import plotly.express as px


class RollingPlots:
    def __init__(self, df):
        self.df = df

    def plot_rolling_7_day(self):
        daily_totals = (
            self.df
            .groupby("Day", as_index=False)["Quantity"]
            .sum()
        )

        daily_totals["Rolling_7_Day"] = (
            daily_totals["Quantity"]
            .rolling(window=7, min_periods=1)
            .mean()
        )

        fig = px.line(
            daily_totals,
            x="Day",
            y=["Quantity", "Rolling_7_Day"],
            title="Daily Sales with Rolling 7-Day Average"
        )

        fig.show()


if __name__ == "__main__":
    print("RollingPlots module loaded")
