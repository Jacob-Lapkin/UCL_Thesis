import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

def display_df(path):
    unclean_df = pd.read_csv(path, index_col=0)
    z_score = stats.zscore(unclean_df)
    abs_z_scores = np.abs(z_score)   
    filtered_entries = (abs_z_scores < 3). all(axis=1)
    new_df = unclean_df[filtered_entries]
    return new_df 
    
def find_mean(path):
    dataframe = display_df(path)
    describe_frame = dataframe.describe()
    return describe_frame 

def plot_angles(path, angle):
    dataframe = display_df(path)
    y = dataframe[angle]
    x = list(range(len(y)))
    #z = dataframe[angle2]
    plt.xlabel('Frame')
    plt.ylabel('Angle in Degrees')
    plt.plot(x, y)
    plt.show()


#plot_angles('data/serve_data/fogserve.csv', 'hip2ankle_right')
#plot_angles('data/serve_data/fritzserve45.csv', 'hip2ankle_right')

# # NADAL 
# # side angle
#plot_angles('data/serve_data/nadalserveside.csv', 'hip2ankle_left')
# # back angle
# plot_angles('data/serve_data/nadalserveback.csv', 'hip2ankle_left')


# # DJOKAVIC
# # side angle
plot_angles('data/serve_data/djokserveside.csv', 'hip2ankle_left')
# # back angle 
plot_angles('data/serve_data/djokserveback.csv', 'hip2ankle_left')
# # 45 angle
plot_angles('data/serve_data/djokserve45.csv', 'hip2ankle_left')




