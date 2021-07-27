from scipy.signal.ltisys import dfreqresp
from pro_angle_data import smoothed_df, make_df
from user_angle_data import make_user_df, grab_user_phase, smoothed_user_df
import numpy as np
import pandas as pd


###### Getting pro data for recommendation #######
def grab_min(path, angle):
    df = make_df(path, angle)
    empty = []
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = min(split_d['angle'])
        empty.append(value)
    return empty

def grab_max(path, angle):
    df = make_df(path, angle)
    empty = []
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = max(split_d['angle'])
        empty.append(value)
    return empty


def grab_range(path, angle):
    df = make_df(path, angle)
    empty = []
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = max(split_d['angle']) - min(split_d['angle'])
        empty.append(value)
    return empty

def grab_average(path, angle):
    df = make_df(path, angle)
    empty = []
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = sum(split_d['angle']) / len(split_d['angle'])
        empty.append(value)
    return empty

#print(grab_average('pose/data/serve_data/djokservelegs.csv', 'hip2ankle_right'))


##### GETTING USER DATAFRAME THAT COMBINES PHASE WITH ANGLE DATA #######
# *** BE SURE TO MATCH THE n value and the n value in multi_class_azure.py file ###
def phase_w_data(data, angle, phase_data):
    data = smoothed_user_df(data)
    new_data = list(data[angle])
    empty=[]
    for ind, i in enumerate(new_data):
        n = 5
        if ind % n == 0:
            empty.append(i)
    phase_data = phase_data['label']
    dic = {'angle':empty, 'phase':phase_data}
    df = pd.DataFrame(dic)
    return df


def grab_user_min(data, angle, phase_data):
    df = phase_w_data(data, angle, phase_data)
    empty=[]
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = min(split_d['angle'])
        empty.append(value)
    return empty

def grab_user_max(data, angle, phase_data):
    df = phase_w_data(data, angle, phase_data)
    empty=[]
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = max(split_d['angle'])
        empty.append(value)
    return empty

def grab_user_range(data, angle, phase_data):
    df = phase_w_data(data, angle, phase_data)
    empty=[]
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = max(split_d['angle']) - min(split_d['angle'])
        empty.append(value)
    return empty

def grab_user_average(data, angle, phase_data):
    df = phase_w_data(data, angle, phase_data)
    empty=[]
    for i in range(4):
        split_d = df[(df['phase'] == i)]
        value = sum(split_d['angle']) / len(split_d['angle'])
        empty.append(value)
    return empty



###### Getting user data for recommendation #######
