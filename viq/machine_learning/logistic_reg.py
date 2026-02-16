import numpy as np
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("/Users/andrewleacock1/Downloads/log.xlsx")

# ----- Define Over-Serviced -----
sales_threshold = 70
y = (df["Avg Qty Sold per Visit"] < sales_threshold).astype(int).values

# Feature
X_raw = df["Avg Outs per Visit"].values

# Scale feature
X_mean = X_raw.mean()
X_std = X_raw.std()
X = (X_raw - X_mean) / X_std

# ----- Train Logistic Regression -----
w = 0.0
b = 0.0
lr = 0.01
epochs = 5000
n = len(X)

for _ in range(epochs):
    z = w * X + b
    p = 1 / (1 + np.exp(-z))

    dw = (1/n) * np.sum((p - y) * X)
    db = (1/n) * np.sum(p - y)

    w -= lr * dw
    b -= lr * db

print("Best w:", w)
print("Best b:", b)

# ----- Graph -----
x_range = np.linspace(X_raw.min(), X_raw.max(), 1000)
x_scaled = (x_range - X_mean) / X_std

z = w * x_scaled + b
prob_curve = 1 / (1 + np.exp(-z))

fig = px.scatter(
    x=X_raw,
    y=y,
    labels={"x": "Avg Outs per Visit", "y": "Over-Serviced (0/1)"},
    title="Probability Machine Is Over-Serviced"
)

fig.add_scatter(
    x=x_range,
    y=prob_curve,
    mode="lines",
    name="Logistic Curve"
)

fig.show()
