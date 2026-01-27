# sim_risk_plot.py

import pandas as pd
import plotly.express as px


class SimulationRiskBoxPlot:
    def __init__(
        self,
        df: pd.DataFrame,
        item_col: str = "Item Name",
        demand_col: str = "Cycle Demand",
        par_col: str = "Par Level",
    ):
        self.df = df.copy()
        self.item_col = item_col
        self.demand_col = demand_col
        self.par_col = par_col

        self._prepare_data()

    def _prepare_data(self):
        self.p95 = (
            self.df.groupby(self.item_col, observed=True)[self.demand_col]
            .quantile(0.95)
        )

        self.p95_order = self.p95.sort_values().index

        self.df[self.item_col] = pd.Categorical(
            self.df[self.item_col],
            categories=self.p95_order,
            ordered=True
        )

        self.df["Stockout"] = self.df[self.demand_col] > self.df[self.par_col]

        self.stockout_prob = (
            self.df.groupby(self.item_col, observed=True)["Stockout"]
            .mean()
        )

        self.df["Stockout Probability"] = self.df[self.item_col].map(
            self.stockout_prob
        )

        self.df["Risk Tier"] = pd.cut(
            self.df["Stockout Probability"],
            bins=[-0.01, 0.05, 0.15, 1.0],
            labels=["Low Risk", "Medium Risk", "High Risk"]
        )

        self.par_lookup = (
            self.df.groupby(self.item_col, observed=True)[self.par_col]
            .first()
        )

    def plot(self):
        fig = px.box(
            self.df,
            x=self.item_col,
            y=self.demand_col,
            points="outliers",
            color="Risk Tier",
            category_orders={self.item_col: list(self.p95_order)},
        )

        for i, item in enumerate(self.p95_order):
            fig.add_shape(
                type="line",
                x0=i - 0.4,
                x1=i + 0.4,
                y0=self.par_lookup[item],
                y1=self.par_lookup[item],
                line=dict(dash="dash", width=2, color="black"),
                opacity=0.7
            )

        return fig


# -------------------------------------------------
# run directly
# -------------------------------------------------
if __name__ == "__main__":

    df = pd.read_excel(
        "/Users/andrewleacock1/Downloads/simulated_sales_10191.xlsx"
    )

    plotter = SimulationRiskBoxPlot(df)
    fig = plotter.plot()
    fig.show()
