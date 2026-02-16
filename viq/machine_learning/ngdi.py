import numpy as np
import matplotlib.pyplot as plt

# Random synthetic dataset
td_x = np.random.randint(0, 100, size=1000)
td_y = np.random.randint(0, 100, size=1000)

# Random initialization (starting point in parameter space)
w = np.random.rand()
b = np.random.rand()

lr = 0.000001          # step size for gradient descent
epochs = 50          # full passes over dataset
batch_size = 16      # How much of the data it iterates over before it updates

n = len(td_x)
losses = []          # track training loss after each parameter update

for epoch in range(epochs):

    # Randomizes the data for each batch
    indices = np.random.permutation(n)
    x_shuffled = td_x[indices]
    y_shuffled = td_y[indices]

    for i in range(0, n, batch_size):

        x_batch = x_shuffled[i:i+batch_size]
        y_batch = y_shuffled[i:i+batch_size]

        # Forward pass: current model prediction
        y_hat = w * x_batch + b
        errors = y_hat - y_batch

        m = len(x_batch)

        # Gradients: direction that increases loss
        # We subtract them to move downhill
        dw = (2/m) * np.sum(errors * x_batch)
        db = (2/m) * np.sum(errors)

        # Parameter update (actual learning step)
        w -= lr * dw
        b -= lr * db

        # Track global training loss to visualize convergence
        full_pred = w * td_x + b
        mse = np.mean((full_pred - td_y) ** 2)
        losses.append(mse)

# Plot how loss changes after every update step
plt.figure()
plt.plot(losses)
plt.xlabel("Iteration")
plt.ylabel("MSE")
plt.title("Training Loss Over Iterations")
plt.show()
