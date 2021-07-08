import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import scipy.signal as signal


# CREATE ORIGINAL DATA FRAME FOR GIVEN PATH
def display_df(path):
    unclean_df = pd.read_csv(path, index_col=0)
    z_score = stats.zscore(unclean_df)
    abs_z_scores = np.abs(z_score)   
    filtered_entries = (abs_z_scores < 3). all(axis=1)
    new_df = unclean_df[filtered_entries]
    return new_df

# CREATE SMOOTH VERSION OF DATA FRAME FOR GIVEN ANGLE
def smoothed_df(path, angle):
    df = display_df(path)
    new_df = df[angle]
    # First, design the Butterworth filter
    N  = 3    # Filter order
    Wn = 0.03 # Cutoff frequency
    B, A = signal.butter(N, Wn, output='ba')
    smooth_data = signal.filtfilt(B,A, new_df)
    return list(smooth_data)


# PLOTS ORIGINAL DATA
def plot_unsmooth_data(path, angle):
    df = display_df(path)
    new_df = df[angle]
    plt.plot(new_df)
    plt.show()


# PLOTS SMOOTH ANGLES
def plot_angles(path, angle):
    df = smoothed_df(path, angle)
    plt.plot(df,'b-')
    plt.show()


#plot_angles('pose/data/serve_data/fogserve.csv', 'hip2ankle_right')
#plot_angles('pose/data/serve_data/fritzserve45.csv', 'hip2ankle_right')

#plot_unsmooth_data('pose/data/serve_data/nadalserveside.csv', 'hip2ankle_right')
# # NADAL 
# # side angle
plot_unsmooth_data('pose/data/serve_data/nadalserveside.csv', 'hip2ankle_left')
plot_angles('pose/data/serve_data/nadalserveside.csv', 'hip2ankle_left')
# # back angle
#plot_unsmooth_data('pose/data/serve_data/nadalserveback.csv', 'hip2ankle_right')
#plot_angles('pose/data/serve_data/nadalserveback.csv', 'hip2ankle_right')


# # DJOKAVIC

# # side angle
#plot_unsmooth_data('pose/data/serve_data/djokserveside.csv', 'hip2ankle_left')
#plot_angles('pose/data/serve_data/djokserveside.csv', 'hip2ankle_left')
# # back angle 
#plot_unsmooth_data('pose/data/serve_data/djokserveback.csv', 'hip2ankle_left')
#plot_angles('pose/data/serve_data/djokserveback.csv', 'hip2ankle_left')
# # 45 angle
#plot_unsmooth_data('pose/data/serve_data/djokserve45.csv', 'hip2ankle_left')
#plot_angles('pose/data/serve_data/djokserve45.csv', 'hip2ankle_left')

