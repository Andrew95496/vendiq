import numpy as np
import plotly.express as px

w = np.random.random()

b = np.random.random()

x = x = np.linspace(np.random.randint(-100, 100), np.random.randint(-100, 100), 1000)

z = b + w*x

probx = np.exp(z)/ (1 + np.exp(z))

print(probx)

fig = px.line(x=x, y=probx, title="Logistic Regression")
fig.show()