import pandas as pd
import plotly.graph_objects as go


class VendingHeatmap:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.slot_matrix = None
        self.pivot_qty = None
        self.pivot_items = None

    def load_data(self):
        self.df = pd.read_excel(self.excel_path)

        # Extract letters (row) and numbers (column)
        self.df["row"] = self.df["Selection"].str.extract(r"([A-Za-z]+)", expand=False)
        self.df["col"] = (
            self.df["Selection"]
            .str.extract(r"(\d+)", expand=False)
            .astype(int)
        )

        # Handle numeric-only selections like "100"
        self.df["row"] = self.df["row"].fillna("NUM")

    def aggregate(self):
        # Total quantity per slot
        slot_qty = (
            self.df.groupby(["row", "col"])["Quantity"]
            .sum()
            .reset_index()
        )

        # Item names per slot
        slot_items = (
            self.df.groupby(["row", "col"])["Item"]
            .apply(lambda x: ", ".join(x.dropna().unique()))
            .reset_index(name="Item")
        )

        self.slot_matrix = slot_qty.merge(slot_items, on=["row", "col"])

    def pivot(self):
        self.pivot_qty = self.slot_matrix.pivot(
            index="row",
            columns="col",
            values="Quantity"
        )

        self.pivot_items = self.slot_matrix.pivot(
            index="row",
            columns="col",
            values="Item"
        )

        # Sort rows and columns
        self.pivot_qty = (
            self.pivot_qty
            .sort_index()
            .reindex(sorted(self.pivot_qty.columns), axis=1)
        )

        self.pivot_items = (
            self.pivot_items
            .reindex(self.pivot_qty.index)
            .reindex(self.pivot_qty.columns, axis=1)
        )

    def plot(self):
        fig = go.Figure(
            go.Heatmap(
                z=self.pivot_qty.values,
                x=self.pivot_qty.columns,
                y=self.pivot_qty.index,
                customdata=self.pivot_items.values,
                colorscale="Plasma",
                hovertemplate=
                    "Slot: %{y}%{x}<br>"
                    "Value: %{z}<br>"
                    "Item: %{customdata}"
                    "<extra></extra>"
            )
        )

        fig.update_layout(
            title="Vending Machine Slot Heatmap",
            xaxis_title="Slot Number",
            yaxis_title="Row",
            yaxis_autorange="reversed"
        )

        fig.show()

    def run(self):
        self.load_data()
        self.aggregate()
        self.pivot()
        self.plot()


if __name__ == "__main__":
    heatmap = VendingHeatmap(
        "/Users/andrewleacock1/Downloads/sales.xlsx"
    )
    heatmap.run()
