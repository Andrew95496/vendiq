import numpy as np
X = np.random.randint(0, 100, size=10)
y = np.random.randint(0, 100, size=10)


w = np.random.normal()
b = np.random.normal()
lr = 0.000001
n = len(X)


# Stochastic gradient descent

for _ in range(n):
    i = np.random.randint(n)
    z = w * X[i] + b
    lg = 1 / (1 + np.exp(-z))

    dw = (lg - y[i]) * X[i]
    db = (lg - y[i])

    w -= lr * dw
    b -= lr * db
    print(f"Stochastic: {'weight(s):':<15}{w:>10.6f} | {'bias:':<6}{b:>10.6f}")


#  Full batch gradient descent

for _ in range(n):
    z = w * X + b
    lg = 1 / (1 + np.exp(-z))

    dw = (1/n) * np.sum((lg - y) * X)
    db = (1/n) * np.sum(lg - y)

    w -= lr * dw
    b -= lr * db
    print(f"Full Batch: {'weight(s):':<15}{w:>10.6f} | {'bias:':<6}{b:>10.6f}")


