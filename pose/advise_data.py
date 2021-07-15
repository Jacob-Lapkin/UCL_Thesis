from scipy.signal.ltisys import dfreqresp
from pro_angle_data import smoothed_df, make_df
import numpy as np
import pandas as pd


# Getting pro data for recommendation 
def grab_min(path, angle, phase):
    df = make_df(path, angle)
    split_d = df[(df['phase'] == phase)]
    value = min(list(split_d['angle']))
    return value

def grab_max(path, angle, phase):
    df = make_df(path, angle)
    split_d = df[(df['phase'] == phase)]
    value = max(list(split_d['angle']))
    return value

#print(grab_min('pose/data/serve_data/djokservelegs.csv', 'hip2ankle_right', 2))




