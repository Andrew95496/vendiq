import numpy as np
import plotly.express as px
import pandas as pd

df = pd.read_excel("/Users/andrewleacock1/Downloads/xxx.xlsx")

# split the two tables
left = df[["Asset ID","rev"]].dropna()
right = df[["Asset ID.1","Visit Count 90"]].dropna()

right = right.rename(columns={
    "Asset ID.1":"Asset ID",
    "Visit Count 90":"visit_90d"
})

merged = left.merge(right, on="Asset ID", how="inner")

# Data
X = merged["visit_90d"].to_numpy(dtype=float)
y = merged["rev"].to_numpy(dtype=int)

# Train / Test split
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
n = len(X_train)

# scale using train only
mu = X_train.mean()
sigma = X_train.std()

X_train = (X_train - mu) / sigma
X_test  = (X_test  - mu) / sigma

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def compute_loss(z, y):
    lg = sigmoid(z)
    lg = np.clip(lg, 1e-15, 1 - 1e-15)
    return -(y * np.log(lg) + (1 - y) * np.log(1 - lg))

def accuracy(w, b):
    preds = sigmoid(w * X_test + b)
    preds_class = (preds >= 0.5).astype(int)
    return (preds_class == y_test).mean()

lr = 0.01
epochs = 5

# =========================
# SGD
# =========================
w = np.random.randn()
b = np.random.randn()
sgd_loss = []

for _ in range(epochs):
    for i in np.random.permutation(n):
        z = w * X_train[i] + b
        sgd_loss.append(compute_loss(z, y_train[i]))

        lg = sigmoid(z)
        w -= lr * (lg - y_train[i]) * X_train[i]
        b -= lr * (lg - y_train[i])

print("\nSGD Results")
print("w:", w)
print("b:", b)
print("Test Accuracy:", accuracy(w, b))

fig1 = px.line(y=sgd_loss, title="SGD Loss")
fig1.show()

# =========================
# Mini Batch
# =========================
w = np.random.randn()
b = np.random.randn()
batch_size = 256
mini_loss = []

for _ in range(epochs):
    idx = np.random.permutation(n)
    X_shuff = X_train[idx]
    y_shuff = y_train[idx]

    for i in range(0, n, batch_size):
        Xb = X_shuff[i:i+batch_size]
        yb = y_shuff[i:i+batch_size]

        z = w * Xb + b
        mini_loss.append(np.mean(compute_loss(z, yb)))

        lg = sigmoid(z)
        w -= lr * np.mean((lg - yb) * Xb)
        b -= lr * np.mean(lg - yb)

print("\nMini Batch Results")
print("w:", w)
print("b:", b)
print("Test Accuracy:", accuracy(w, b))

fig2 = px.line(y=mini_loss, title="Mini Batch Loss")
fig2.show()

# =========================
# Full Batch
# =========================
w = np.random.randn()
b = np.random.randn()
full_loss = []

for _ in range(epochs * 100):
    z = w * X_train + b
    full_loss.append(np.mean(compute_loss(z, y_train)))

    lg = sigmoid(z)
    w -= lr * np.mean((lg - y_train) * X_train)
    b -= lr * np.mean(lg - y_train)

print("\nFull Batch Results")
print("w:", w)
print("b:", b)
print("Test Accuracy:", accuracy(w, b))

fig3 = px.line(y=full_loss, title="Full Batch Loss")
fig3.show()

# =========================
# Model Evaluation
# =========================
probs = sigmoid(w * X_test + b)
preds = (probs >= 0.5).astype(int)

tp = np.sum((preds==1)&(y_test==1))
fp = np.sum((preds==1)&(y_test==0))
fn = np.sum((preds==0)&(y_test==1))
tn = np.sum((preds==0)&(y_test==0))

precision = tp/(tp+fp) if (tp+fp)>0 else 0
recall = tp/(tp+fn) if (tp+fn)>0 else 0
accuracy = (tp+tn)/len(y_test)

print("\nConfusion Matrix")
print("TP:",tp,"FP:",fp,"FN:",fn,"TN:",tn)

print("\nMetrics")
print("Accuracy:",accuracy)
print("Precision:",precision)
print("Recall:",recall)

order = np.argsort(-probs)
top = y_test[order][:50]

print("\nTop 50 predicted bad machines actually bad rate:")
print(top.mean())