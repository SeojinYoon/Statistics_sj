
import matplotlib.pylab as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

x = np.linspace(0, 10, 30)
y = np.sin(x)

plt.plot(x, y, 'o')

from Preprocessing_Package import sj_util
from Preprocessing_Package import sj_preprocessing
sj_util.partition_d1(10, 20, 10)

sj_preprocessing.counter([1,2,3], [(0,1), (1,2), (2,3)], "Left")

def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)

X, Y = np.meshgrid(x,y)
Z = f(X,Y)

plt.contour(X, Y, Z, 20, cmap='RdGy');
plt.colorbar()

Z.shape