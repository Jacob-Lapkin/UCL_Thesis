from numpy.lib.shape_base import split
from pro_angle_data import smoothed_df, phase_divider, grab_label, split_data, split_label, display_df
from user_angle_data import smoothed_user_df, grab_user_label, display_user_df, phase_user_divider
from multi_class_azure import StrokeList

#############################################################################
########### CREATING CLASSES TO USE FOR PRO AND USER ON DASHBOARD ###########
#############################################################################

# class to get data from user or professional 
class Player_data:

    def __init__(self, path, angle, name):
        self.path = path
        self.angle = angle
        self.name = name
    # getting all the data at once
    def get_data(self):
        data = smoothed_df(self.path, self.angle)
        return data

    # getting only a phase of the data
    def get_split_data(self, phase):
        data = split_data(self.path, self.angle, phase)
        return data

    # getting a breakdown of the phases
    def doughnut(self):
        doughnut_data = phase_divider(self.path)
        return doughnut_data

    # gettinga all the labels or frames
    def labels(self):
        labels = grab_label(self.path, self.angle)
        return labels
    
    # getting all the labels or frames by phase
    def splitting_label(self, phase):
        getting_split = split_label(self.path, self.angle, phase)
        labels = []
        for i in getting_split:
            labels.append(str(i))
        return labels


#djok = Player_data('pose/data/serve_data/djokserve45.csv', 'hip2ankle_right', 'Djokovic')
#print(djok.get_split_data(0))
#print(djok.splitting_label(0))
#print(djok.get_data())
#print(djok.labels())



class User_data():
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.df = display_user_df(path)

    def get_data(self, angle):
        #data = smoothed_user_df(self.path)
        data = smoothed_user_df(self.df)
        return data[angle]
    
    def labels(self):
        data = self.df
        labels = grab_user_label(data)
        return labels
    
    @staticmethod
    def doughnut(name, base, folder):
        doughnut_data = phase_user_divider(name, base, folder)
        return doughnut_data



#user = User_data('pose/videos/serve/djok/djokserve45.mp4','Jacob')

# player_data_r = list(user.get_data('hip2ankle_right'))

#print(User_data.doughnut('Jacob', 'User_test','User_test'))