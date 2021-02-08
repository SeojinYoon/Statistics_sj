# https://machinelearningmastery.com/curve-fitting-with-python/

from scipy.optimize import curve_fit
from pandas import read_csv
from matplotlib import pyplot
import os
import numpy as np

# load the dataset
pj_home_path = os.getcwd()
data_dir_path = os.path.join(pj_home_path, "Example", "CurveFitting", "Data")
longley_csv_path = os.path.join(data_dir_path, "longley.csv")
dataframe = read_csv(longley_csv_path, header=None)
data = dataframe.values
# choose the input and output variables
x, y = data[:, 4], data[:, -1]

"""
fit data to linear function
"""
#plot input vs output
pyplot.scatter(x, y)
# define the true objective function
def objective(x, a, b):
    return a * x + b
# curve fit
popt, _ = curve_fit(objective, x, y)
# summarize the parameter values
a, b = popt
print("y = %.5f * x + %.5f" % (a,b))
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(x), max(x), 1)
# calculate the output for the range
y_line = objective(x_line, a, b)
# create a line plot for the mapping function
pyplot.scatter(x, y)
pyplot.plot(x_line, y_line, "--", color="red")

"""
fit data to curve
"""
# define the true objective function
def objective(x, a, b, c):
	return a * x + b * x**2 + c
# curve fit
popt, _ = curve_fit(objective, x, y)
# summarize the parameter values
a, b, c = popt
print('y = %.5f * x + %.5f * x^2 + %.5f' % (a, b, c))
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(x), max(x), 1)
# calculate the output for the range
y_line = objective(x_line, a, b, c)
# create a line plot for the mapping function
pyplot.scatter(x, y)
pyplot.plot(x_line, y_line, "--", color="red")

# define the true objective function
def objective(x, a, b, c, d, e, f):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f
# curve fit
popt, _ = curve_fit(objective, x, y)
# summarize the parameter values
a, b, c, d, e, f = popt
# plot input vs output
pyplot.scatter(x, y)
# define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(x), max(x), 1)
# calculate the output for the range
y_line = objective(x_line, a, b, c, d, e, f)
# create a line plot for the mapping function
pyplot.scatter(x, y)
pyplot.plot(x_line, y_line, '--', color='red')
