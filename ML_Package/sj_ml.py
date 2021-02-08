# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:04:18 2020

@author: frontis
"""

import numpy as np
from Higher_function import sj_higher_function

def numerical_gradient(f, x):
    """
    find numerical gradient about f at x

    :param f: function ex) lambda x,a,b: x**2 + a**3 + b
    :param x: specific value ex) [2,3,4]
    :return: list(numerical gradient)
    """
    x = np.array(x, dtype = np.float64)
    h = 1e-4
    grad = np.zeros_like(x)

    for idx in range(x.size):
        tmp_val = x[idx]
        x[idx] = tmp_val + h
        fxh1 = sj_higher_function.apply_function(f, x)

        x[idx] = tmp_val - h
        fxh2 = sj_higher_function.apply_function(f, x)
        
        grad[idx] = (fxh1 - fxh2) / (2*h)
        x[idx] = tmp_val
        
    return grad

def gradient_descent(f, init_x, lr, step_num = 100):
    """
    apply simultaneous gradient descent

    :param f: function for fitting ex) lambda x: x**2
    :param init_x: initial value ex) [2]
    :param lr: learning rate ex) 0.001
    :param step_num: number of learning steps ex) 100
    :return: fitted value
    """
    x = init_x 
    # Loss에 x를 input으로 넣을때, gradient를 구함
    # 파라미터 업데이트
    for i in range(0, step_num):
        grad = numerical_gradient(f, x)
        x -= lr * grad
        
    return x

if __name__ == "__main__":
    numerical_gradient(lambda x, a, b: 4 * x ** 2 + a ** 3 + b, [1, 2, 3])

    gradient_descent(lambda a, b: a ** 2 + b ** 2 + b, [3, 3], 0.01, step_num=300)
