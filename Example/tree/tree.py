#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:28:31 2020

@author: yoonseojin
"""

import pandas as pd
import numpy as np
import pickle
from Statistics_Package import stat_module

# Make Data
diameter = [21.0, 21.8, 22.3, 26.6, 27.1, 27.4, 27.9, 27.9, 29.7, 32.7, 32.7, 33.7, 34.7, 35.0, 40.6]

height = [21.33, 19.81, 19.20, 21.94, 24.68, 25.29, 20.11, 22.86, 21.03, 22.55, 25.90, 26.21, 21.64, 19.50, 21.94]

volume = [0.291, 0.291, 0.288, 0.464, 0.532, 0.557, 0.441, 0.515, 0.603, 0.628, 0.956, 0.775, 0.727, 0.704, 1.084]

data = pd.DataFrame([diameter, height, volume])

data = data.transpose()
data.columns = ['diameter(cm)', 'height(m)', 'volume(m^3)']
data.to_pickle('/Users/yoonseojin/Desktop/데이터 분석/tree.pkl')

# Load Data
pkl_file = open('/Users/yoonseojin/Desktop/데이터 분석/tree.pkl', 'rb')
data = pickle.load(pkl_file)

response = np.array(data['volume(m^3)'])
variables = np.array([np.array(data['diameter(cm)']), np.array(data['height(m)'])]).transpose()

stat_module.bonferroni_simultaneous_confidence_interval(variables, response, 0.95, [1, 2])


