import numpy as np
import matplotlib.pyplot as plt

#Jednostavan primjer perceptrona
# --------------------------------------
# 1. Dataset (AND problem)
# --------------------------------------
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([0, 0, 0, 1])  # AND funkcija

# --------------------------------------
# 2. Perceptron parametri
# --------------------------------------
weights = np.zeros(2)
bias = 0
lr = 0.1  # learning rate


# Step aktivacija
def step(z):
    return 1 if z >= 0 else 0


# --------------------------------------
# 3. Trening petlja
# --------------------------------------
for epoch in range(20):
    for i in range(len(X)):
        z = np.dot(X[i], weights) + bias
        y_pred = step(z)

        error = y[i] - y_pred

        # update rule
        weights += lr * error * X[i]
        bias += lr * error

print("Težine:", weights)
print("Bias:", bias)

# --------------------------------------
# 4. Vizualizacija decision boundary
# --------------------------------------
x_vals = np.linspace(-1, 2, 100)
y_vals = -(weights[0] * x_vals + bias) / weights[1]

plt.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm")
plt.plot(x_vals, y_vals, label="Decision boundary")
plt.title("Perceptron – linearna granica odlučivanja")
plt.xlabel("x1")
plt.ylabel("x2")
plt.legend()
plt.show()
