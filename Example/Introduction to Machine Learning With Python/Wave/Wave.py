import mglearn
import matplotlib.pylab as plt

X, y = mglearn.datasets.make_wave(n_samples=40)
plt.plot(X, y, "o")
plt.ylim(-3, 3)
plt.xlabel("feature")
plt.ylabel("target")