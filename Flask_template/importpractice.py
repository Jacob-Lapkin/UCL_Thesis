import sys
sys.path.append('/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose')
from angledata import display_df, smoothed_df

data = smoothed_df('pose/data/serve_data/djokserve45.csv', 'hip2ankle_right')
empty_label =[]
for ind, value in enumerate(range(len(data))):
    empty_label.append(f'frame{ind}')
labels = empty_label

