
import pandas as pd
import numpy as np
import pickle
from Statistics_Package import stat_module

# Make Data and serialize using pickle
pages = pd.Series([637, 336, 336, 430, 164, 533, 529, 509, 419, 596, 496, 673, 562, 229, 316, 217, 296, 115, 257, 649], name="pages")
prices = pd.Series([27.0, 15.0, 14.0, 15.0, 9.5, 20.0, 22.0, 20.0, 16.0, 24.0, 20.0, 25.0, 24.0, 10.0, 13.0, 8.0, 12.0, 7.0, 11.0, 22.0], name="price(1000)")

df = pd.DataFrame([pages, prices])

data = df.transpose()
data.to_pickle('./book.pkl')

# Load Data
pkl_file = open('/Users/yoonseojin/Desktop/데이터 분석/book.pkl', 'rb')
data = pickle.load(pkl_file)

# Data Analysis
s2 = stat_module.est_standard_error(np.array(data['pages']), np.array(data['price(1000)']))

stat_module.find_reg_coeff(np.array(data['pages']), np.array(data['price(1000)']))

np.sum(np.array(data['pages']))


