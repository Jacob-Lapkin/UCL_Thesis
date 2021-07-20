from numpy.lib.shape_base import split
from pro_angle_data import smoothed_df, phase_divider, grab_label, split_data, split_label, display_df
from user_angle_data import smoothed_user_df, grab_user_label, display_user_df, phase_user_divider
from multi_class_azure import StrokeList
from recommendations_data import *
import matplotlib.pyplot as plt

#############################################################################
########### CREATING CLASSES TO USE FOR PRO AND USER ON DASHBOARD ###########
#############################################################################

######### class to get data from  professional ############
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


    def get_min_data(self):
        min_data = grab_min(self.path, self.angle)
        return min_data

    def get_max_data(self):
        max_data = grab_max(self.path, self.angle)
        return max_data

    def get_range_data(self):
        range_data = grab_range(self.path, self.angle)
        return range_data
    


########### class to get data from user ###########
class User_data():
    def __init__(self, path, name, base, folder):
        self.path = path
        self.name = name
        self.df = display_user_df(path)
        self.phase_df = StrokeList(name, base, folder)

    def get_data(self, angle):
        #data = smoothed_user_df(self.path)
        data = smoothed_user_df(self.df)
        return data[angle]
    
    def labels(self):
        data = self.df
        labels = grab_user_label(data)
        return labels
    
    def doughnut(self):
        data = self.phase_df
        doughnut_data = phase_user_divider(data)
        return doughnut_data

    def get_full_data(self, angle):
        df = phase_w_data(self.df, angle, self.phase_df)
        return df
    
    def get_min_data(self, angle):
        min_data = grab_user_min(self.df, angle, self.phase_df)
        return min_data
    
    def get_max_data(self, angle):
        max_data = grab_user_max(self.df, angle, self.phase_df)
        return max_data


# playerright_leg = Player_data(f'pose/data/serve_data/djokservelegs.csv', 'hip2ankle_right', 'djok')
# playerleft_leg = Player_data(f'pose/data/serve_data/djokservelegs.csv', 'hip2ankle_left', 'djok')
# playerright_arm = Player_data(f'pose/data/serve_data/djokservearm.csv', 'shoulder2wrist_right', 'djok')
# playerleft_arm = Player_data(f'pose/data/serve_data/djokservearm.csv', 'shoulder2wrist_left', 'djok')
# user = User_data('pose/videos/serve/jake.mov', 'Jacob', str(1), str(1))
# print(user.get_full_data('hip2ankle_right'))


####### IF STATEMENTS FOR RECOMMENDATIONS #######

    
def legs_tips_start(user, playerright_leg, playerleft_leg):
    leg_tip_start = None
    if user.get_max_data('hip2ankle_right')[0] < playerright_leg.get_max_data()[0] and user.get_max_data('hip2ankle_left')[0] < playerleft_leg.get_max_data()[0]:
        leg_tip_start = 'Try to stand straighter during your ready position.'
    elif user.get_max_data('hip2ankle_right')[0] > playerright_leg.get_max_data()[0] and user.get_max_data('hip2ankle_left')[0] > playerleft_leg.get_max_data()[0]:
        leg_tip_start = 'Try to bend your legs more during your ready position.'
    elif user.get_max_data('hip2ankle_right')[0] > playerright_leg.get_max_data()[0] and user.get_max_data('hip2ankle_left')[0] < playerleft_leg.get_max_data()[0]:
        leg_tip_start = 'Your legs seem to be starting at very contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
    elif user.get_max_data('hip2ankle_right')[0] < playerright_leg.get_max_data()[0] and user.get_max_data('hip2ankle_left')[0] > playerleft_leg.get_max_data()[0]:
        leg_tip_start = 'Your legs seem to be starting at very contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
    return leg_tip_start

def legs_tips_load(user, playerright_leg, playerleft_leg):
    leg_tip_load = None
    if user.get_min_data('hip2ankle_right')[1] < playerright_leg.get_min_data()[1] and user.get_min_data('hip2ankle_left')[1] < playerleft_leg.get_min_data()[1]:
        leg_tip_load = 'You are loading your back leg too much, try standing taller during your take back. '
    elif user.get_min_data('hip2ankle_right')[1] > playerright_leg.get_min_data()[1] and user.get_min_data('hip2ankle_right')[1] > playerright_leg.get_min_data()[1]:
        leg_tip_load = 'You could increase power in your serve by bending your legs more.'
    elif user.get_min_data('hip2ankle_right')[1] > playerright_leg.get_min_data()[1] and user.get_min_data('hip2ankle_left')[1] < playerleft_leg.get_min_data()[1]:
        leg_tip_load = 'Your lower body may be leaning too far forward during you takeback. Try to more equally match the bend in your right and left legs.'
    elif user.get_min_data('hip2ankle_right')[1] < playerright_leg.get_min_data()[1] and user.get_min_data('hip2ankle_left')[1] > playerleft_leg.get_min_data()[1]:
        leg_tip_load = 'Your lower body may be leaning too far back during you takeback. Try to more equally match the bend in your right and left legs.'
    return leg_tip_load

def legs_tips_extend(user, playerright_leg, playerleft_leg):
    leg_tip_extend = None
    if user.get_max_data('hip2ankle_right')[2] < playerright_leg.get_max_data()[2] and user.get_max_data('hip2ankle_left')[2] < playerleft_leg.get_max_data()[2]:
        leg_tip_extend = 'Your legs are not extending enough during contact. Make sure to drive more with you legs on your extension.'
    elif user.get_max_data('hip2ankle_right')[2] > playerright_leg.get_max_data()[2] and user.get_max_data('hip2ankle_left')[2] < playerleft_leg.get_max_data()[2]:
        leg_tip_extend = 'Your back leg should extend more to be closer in line with your front leg during extension and contact.'
    elif user.get_max_data('hip2ankle_right')[2] < playerright_leg.get_max_data()[2] and user.get_max_data('hip2ankle_left')[2] > playerleft_leg.get_max_data()[2]:
        leg_tip_extend = 'Your front leg should extend more to be closer in line with your back leg during extension and contact.'
    return leg_tip_extend

def legs_tips_finish(user, playerleft_leg):
    leg_tip_finish = None
    if user.get_min_data('hip2ankle_left')[3] < playerleft_leg.get_min_data()[3]:
        leg_tip_finish = 'You are dipping your front leg too much during the finish. Try landing taller to optimize your recovery.'
    if user.get_min_data('hip2ankle_left')[3] > playerleft_leg.get_min_data()[3]:
        leg_tip_finish = 'You are standing too tall during your finish. Try getting lower to absorb your impact with the ground.'
    return leg_tip_finish

#print(legs_tips_start())
# print(legs_tips_load())
# print(legs_tips_extend())
#print(legs_tips_finish())
def leg_tip_summary(user, playerright_leg, playerleft_leg):
    leg_start = legs_tips_start(user, playerright_leg, playerleft_leg)
    leg_load = legs_tips_load(user, playerright_leg, playerleft_leg)
    leg_extend = legs_tips_extend(user, playerright_leg, playerleft_leg)
    leg_finish = legs_tips_finish(user, playerright_leg)
    leg_tip_list = [leg_start, leg_load, leg_extend, leg_finish]
    return leg_tip_list













