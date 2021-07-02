import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def display_df(path):
    df = pd.read_csv(path, index_col=0)
    return df

def find_mean(path):
    dataframe = display_df(path)
    mean = dataframe.describe(include='all').loc['mean']
    return mean

def find_min(path):
    dataframe = display_df(path)
    min = dataframe.describe(include='all').loc['min']
    return min

def find_max(path):
    dataframe = display_df(path)
    min = dataframe.describe(include='all').loc['max']
    return max

def plot_angles(path, angle):
    dataframe = display_df(path)
    y = dataframe[angle]
    x = list(range(len(y)))
    #z = dataframe[angle2]
    plt.xlabel('Frame')
    plt.ylabel('Angle in Degrees')
    plt.plot(x, y)
    plt.show()

plot_angles('data/nadal.csv', 'hip2ankle_left')

    
    
