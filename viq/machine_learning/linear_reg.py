import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class SimpleLinearRegressionModel:
    def __init__(self, file_path: str, x_column: str, y_column: str):
        self.file_path = file_path
        self.x_column = x_column
        self.y_column = y_column
        self.model = LinearRegression()
        self.data = None
        self.X = None
        self.y = None

    def load_data(self):
        self.data = pd.read_excel(self.file_path)
        self.X = self.data[[self.x_column]]
        self.y = self.data[self.y_column]

    def fit(self):
        if self.X is None or self.y is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        self.model.fit(self.X, self.y)

    def predict(self, value: float):
        X_new = np.array([[value]])
        return self.model.predict(X_new)[0]

    def get_coefficients(self):
        return {
            "intercept": self.model.intercept_,
            "slope": self.model.coef_[0]
        }

    def plot(self):
        x_min = self.X[self.x_column].min()
        x_max = self.X[self.x_column].max()

        x_range = np.linspace(x_min, x_max, 100).reshape(-1, 1)
        y_pred = self.model.predict(x_range)

        plt.figure(figsize=(8, 6))
        plt.scatter(self.X, self.y, alpha=0.3)
        plt.plot(x_range, y_pred, linewidth=2)

        plt.xlabel(self.x_column)
        plt.ylabel(self.y_column)
        plt.title(f"{self.x_column} vs {self.y_column}")
        plt.show()


if __name__ == "__main__":
    file_path = "/Users/andrewleacock1/Downloads/machine_visits_revenue_2025.xlsx"

    model = SimpleLinearRegressionModel(
        file_path=file_path,
        x_column="Avg Qty Sold per Visit",
        y_column="Avg Outs per Visit"
    )

    model.load_data()
    model.fit()

    prediction = model.predict(70)
    coeffs = model.get_coefficients()

    print("Prediction:", prediction)
    print("Intercept:", coeffs["intercept"])
    print("Slope:", coeffs["slope"])

    model.plot()

