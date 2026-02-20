from sklearn.datasets import fetch_openml
import plotly.express as px 
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

mnist = fetch_openml("mnist_784", version=1)

X, y = mnist.data, mnist.target
X = X.to_numpy()  
y = y.astype(np.uint8)

some_digit = X[16000]
# some_digit_img = some_digit.reshape(28, 28)

# fig = px.imshow(
#     some_digit_img,
#     color_continuous_scale="greys",
#     aspect="equal"
# )

# fig.update_layout(coloraxis_showscale=False)
# fig.show()

# test data/ training data

X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
shuffle_index = np.random.permutation(60000)
X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]
y_train_data = (y_train == 8) 
y_test_data = (y_test == 8)

# Training a Binary Clasifier
sgd_clf = SGDClassifier(max_iter=5, tol=None, random_state=42)
sgd_clf.fit(X_train, y_train_data)
y_pred = sgd_clf.predict(X_train)
print(y_pred)

# Cross Valadation
cssv = cross_val_score(sgd_clf, X_train, y_train_data, cv=3, scoring="accuracy")
print(f"Accuracy: {cssv}")

# Confusion Matrix
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_data, cv=3)
q = confusion_matrix(y_train_data, y_train_pred)
print(q)

# Precision and Recall
ps = precision_score(y_train_data, y_pred)

rs = recall_score(y_train_data, y_pred)

print(f"Precision Score: {ps} | Recall Score: {rs}")

#f1 score
f1 = f1_score(y_train_data, y_pred)
print(f1)