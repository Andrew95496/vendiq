import pandas as pd

class SalesReport:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        return pd.read_excel(self.excel_path)

    def _total_sales(self) -> float:
        return self.df["total_sales"].sum()

    def _avg_daily_sales(self) -> float:
        return (
            self.df
            .groupby("date")["total_sales"]
            .sum()
            .mean()
        )

    def _top_products(self, n: int = 5):
        return (
            self.df
            .groupby("product")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
        )

    def generate(self) -> str:
        total_sales = self._total_sales()
        avg_daily_sales = self._avg_daily_sales()
        top_products = self._top_products()

        lines = []
        lines.append("SALES PERFORMANCE REPORT\n")
        lines.append(f"Total Sales: ${total_sales:,.2f}")
        lines.append(f"Average Daily Sales: ${avg_daily_sales:,.2f}\n")

        lines.append("Top Performing Products:")
        for product, sales in top_products.items():
            lines.append(f"- {product}: ${sales:,.2f}")

        return "\n".join(lines)


if __name__ == "__main__":
    report = SalesReport("data/sales_data.xlsx")
    print(report.generate())