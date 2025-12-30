import plotly.express as px


class DailyPlots:
    def __init__(self, df):
        self.df = df

    def plot_daily_totals(self):
        daily_totals = (
            self.df
            .groupby("Date", as_index=False)["Quantity"]
            .sum()
        )

        fig = px.bar(
            daily_totals,
            x="Date",
            y="Quantity",
            title="Total Quantity Sold Per Day"
        )

        fig.show()

    def plot_day_of_week_totals(self):
        dow_totals = (
            self.df
            .groupby("Day_of_Week", as_index=False)["Quantity"]
            .sum()
        )

        fig = px.bar(
            dow_totals,
            x="Day_of_Week",
            y="Quantity",
            title="Total Quantity Sold by Day of Week"
        )

        fig.show()


if __name__ == "__main__":
    print("DailyPlots module loaded")
