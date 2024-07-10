import pandas as pd
import numpy as np
import sys
import os

__file__ = "inv_theory.py"
current_dir = os.path.dirname(os.path.abspath(__file__))

R = 0.055
b = 1/(1+R)
maturity_g = 0.073
time_frame = 10
start_earnings = 10

print(f'Current Directory: {current_dir}')

def predict_multiple(growth, t, R = R, b = b, maturity_g = maturity_g, time_frame = time_frame, start_earnings = start_earnings): 
    growth = min([growth/100,0.30])
    maturity_g = 0.065 + 0.1*(growth - 0.065)
    k_vec_m = 1 + maturity_g
    maturity_multiple = (k_vec_m*b*(1-(k_vec_m*b)**18)/(1-b*k_vec_m))
    maturity_multiple   
    b_vec = [b] * t
    k_vec = [1 + growth] * t
    b_vec = np.cumprod(b_vec)[:t]
    k_vec = np.cumprod(k_vec)[:t]
   
    return sum(k_vec*b_vec) + maturity_multiple*b_vec[-1]*k_vec[-1]

def predict_roi(growth, multiple, fut_multiple): 
    growth = min([growth/100,0.30])
    return (((1+growth)**6)*(1+(1/multiple)+(fut_multiple/multiple)))**1/6