import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load
visits_revenue = pd.read_excel(
    "/Users/andrewleacock1/Downloads/machine_visits_revenue_2025.xlsx"
)

# Define X and y
X = visits_revenue[["Avg Qty Sold per Visit"]]
y = visits_revenue["Avg Outs per Visit"]

# Fit model
model = LinearRegression()
model.fit(X, y)

# Create regression line
x_min = X["Avg Qty Sold per Visit"].min()
x_max = X["Avg Qty Sold per Visit"].max()

x_range = np.linspace(x_min, x_max, 100).reshape(-1, 1)
y_pred = model.predict(x_range)

# Plot
plt.figure(figsize=(8,6))
plt.scatter(X, y, color="blue", alpha=0.3)
plt.plot(x_range, y_pred, color="red", linewidth=2)

plt.xlabel("Avg Qty Sold per Visit")
plt.ylabel("Avg Outs per Visit")
plt.title("Avg Qty Sold per Visit vs Avg Outs per Visit")


# Console prediction example
X_new = np.array([[70]]) 
prediction = model.predict(X_new)

print("Predicted Avg Outs per Visit:", prediction[0])
print("Intercept:", model.intercept_)
print("Slope:", model.coef_[0])

plt.show()