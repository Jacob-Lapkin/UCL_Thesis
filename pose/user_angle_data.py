from numpy.core.fromnumeric import take
import pandas as pd
import numpy as np
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import scipy.signal as signal
from pose.pose_finder import angle_from_video
from pose.multi_class_azure import StrokeList

######################################################################
########### FUNCTIONS TO USE AND MANIPILATE PRO PLAYER DATA###########
######################################################################

# CREATE ORIGINAL DATA FRAME FOR GIVEN PATH
def display_user_df(path):
    unclean_df = angle_from_video(path)
    z_score = stats.zscore(unclean_df)
    abs_z_scores = np.abs(z_score)   
    filtered_entries = (abs_z_scores < 3). all(axis=1)
    new_df = unclean_df[filtered_entries]
    return new_df


#print(display_user_df('pose/videos/serve/djok/djokserve45.mp4'))

# CREATE SMOOTH VERSION OF DATA FRAME FOR GIVEN ANGLE
def smoothed_user_df(data):
    df = data
    frame = df['frame']
    right_leg = df['hip2ankle_right']
    left_leg = df['hip2ankle_left']
    right_arm = df['shoulder2wrist_right']
    left_arm = df['shoulder2wrist_left']
    right_body = df['elbow2hip_right']
    left_body = df['elbow2hip_left']

    # First, design the Butterworth filter
    N  = 3    # Filter order
    Wn = 0.03 # Cutoff frequency
    B, A = signal.butter(N, Wn, output='ba')
    smooth_frame = signal.filtfilt(B,A, frame)
    smooth_right = signal.filtfilt(B,A, right_leg)
    smooth_left = signal.filtfilt(B,A, left_leg)
    smooth_right_arm = signal.filtfilt(B,A, right_arm)
    smooth_left_arm = signal.filtfilt(B,A, left_arm)
    smooth_right_body = signal.filtfilt(B,A, right_body)
    smooth_left_body = signal.filtfilt(B,A, left_body)
    d = {'frame':list(smooth_frame),'hip2ankle_right':list(smooth_right), 'hip2ankle_left':list(smooth_left),
            'shoulder2wrist_right':list(smooth_right_arm), 'shoulder2wrist_left':list(smooth_left_arm),
            'elbow2hip_right':list(smooth_right_body), 'elbow2hip_left':list(smooth_left_body) }
    df = pd.DataFrame(d)
    return df

#print(smoothed_user_df('pose/videos/serve/djok/djokserve45.mp4'))


# EXTRACT THE PHASES OUT FROM THE CSV FILE
def grab_user_phase(data):
    phase_df = data
    phase_df = phase_df['phase']
    return list(phase_df)

# Diving the phases and calulating the breakdown of the phases in the shot
def phase_user_divider(data):
    df = data
    counting_phases = df['label'].tolist()
    start_count = counting_phases.count(0)
    take_load_count = counting_phases.count(1)
    extend_count = counting_phases.count(2)
    finish_count = counting_phases.count(3)
    if finish_count == 0:
        finish_count = 10
    if start_count == 0:
        start_count = 10
    if take_load_count == 0:
        take_load_count = 10
    if finish_count == 0:
        finish_count = 10
    total_count = start_count + take_load_count + extend_count + finish_count 
    percent_start = round(start_count / total_count * 100)
    percent_take_load = round(take_load_count / total_count * 100)
    percent_extend = round(extend_count / total_count * 100)
    percent_finish = round(finish_count / total_count * 100)
    final_percentage = [percent_start, percent_take_load, percent_extend, percent_finish]
    return final_percentage
    
#print(phase_user_divider('Jacob', str(1), str(1)))

# making a new dataframe connecting phase with angle
def make_user_df(data):
    data = smoothed_user_df(data)
    phase = grab_user_phase(data)
    get_frame = display_user_df(data)
    frame_col = get_frame['frame'].tolist()
    data['phase'] = phase
    data['frame'] = frame_col
    return data

# splitting the data into different phases
def split_user_data(data, phase):
    data = make_user_df(data)
    split_d = data[(data['phase'] == phase)]
    angle_d = split_d['angle'].tolist()
    return angle_d

# splitting labels into different phases
def split_user_label(data, phase):
    data = make_user_df(data)
    split_l = data[(data['phase'] == phase)]['frame']
    label_l = split_l.tolist()
    return label_l


# grabbing the labels for use in the Players class in CanvasData.py file
def grab_user_label(data):
    df = smoothed_user_df(data)
    data = df['hip2ankle_right']
    empty_label =[]
    # getting labels by finding index 
    for ind, value in enumerate(range(len(data))): 
        empty_label.append(ind)
    # adding each index converted to a percentage to a list 
    real_labels = []
    for i in empty_label:
        real_labels.append(str(round(i / max(empty_label)* 100)))
    labels = real_labels
    return labels


# PLOTS ORIGINAL DATA
def plot_user_unsmooth_data(path, angle):
    df = display_user_df(path)
    new_df = df[angle]
    plt.plot(new_df)
    plt.show()

#print(plot_user_unsmooth_data('pose/videos/serve/jake.mov', 'hip2ankle_right'))


# PLOTS SMOOTH ANGLES
def plot_angles(path):
    df = display_user_df(path)
    new_df = smoothed_user_df(df)
    new_df = df['hip2ankle_right']
    plt.plot(new_df,'b-')
    plt.show()

#print(plot_angles('pose/videos/serve/jake.mov'))
