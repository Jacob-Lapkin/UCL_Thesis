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
    
    def get_average_data(self):
        average_data = grab_average(self.path, self.angle)
        return average_data
    

    


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

    def get_range_data(self, angle):
        range_data = grab_user_range(self.df, angle, self.phase_df)
        return range_data

    def get_average_data(self, angle):
        range_data = grab_user_average(self.df, angle, self.phase_df)
        return range_data
    

# playerright_leg = Player_data(f'pose/data/serve_data/djokservelegs.csv', 'hip2ankle_right', 'djok')
# playerleft_leg = Player_data(f'pose/data/serve_data/djokservelegs.csv', 'hip2ankle_left', 'djok')
# playerright_arm = Player_data(f'pose/data/serve_data/djokservearm.csv', 'shoulder2wrist_right', 'djok')
# playerleft_arm = Player_data(f'pose/data/serve_data/djokservearm.csv', 'shoulder2wrist_left', 'djok')
# user = User_data('pose/videos/serve/jake.mov', 'Jacob', str(1), str(1))
# print(user.get_full_data('hip2ankle_right'))


####### IF STATEMENTS FOR RECOMMENDATIONS #######

# Legs
def legs_tips_start(user, playerright_leg, playerleft_leg):
    leg_tip_start = None
    score_lost = 0

    # less than the pro angles
    if user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.80) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.80):
        leg_tip_start = 'Try to standup a lot more during your ready position.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.90) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.90):
        leg_tip_start = 'Try to standup more during your ready position.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.95) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.95):
        leg_tip_start = 'Try to standup slightly more during your ready position.'
        score_lost += 2
    # grater than the pro angles
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.20) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.20):
        leg_tip_start = 'Try to bend your legs a lot more during your ready position.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.10) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.10):
        leg_tip_start = 'Try to bend your legs more during your ready position.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.05) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.05):
        leg_tip_start = 'Try to bend your legs slightly more during your ready position.'
        score_lost += 2
    # greater than one angle and less than the other
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.20) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 1.20):
        leg_tip_start = 'Your legs seem to be starting at very contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 1.10) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.10):
        leg_tip_start = 'Your legs seem to be starting at contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 1.05) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.05):
        leg_tip_start = 'Your legs seem to be starting at slighty contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        score_lost += 2
    else:
        leg_tip_start = 'Your legs are placed well, and your lower body posture looks good!'
    return [leg_tip_start, score_lost]

def legs_tips_load(user, playerright_leg, playerleft_leg):
    score_lost = 0
    leg_tip_load = None
    # bending legs too much during load
    if user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.80) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.80):
        leg_tip_load = 'You are loading your back leg too extremely. try standing much taller during your take back.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.90) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.90):
        leg_tip_load = 'You are loading your back legs too much, try standing taller during your take back.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.95) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.95):
        leg_tip_load = 'You are loading your back legs a bit too much, try standing slightly taller during your take back.'
        score_lost += 2
    # not bedning legs enough during laod
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.20) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.20):
        leg_tip_load = 'You can significatly increase power in your serve by bending your legs a convincing amount.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.10) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.10):
        leg_tip_load = 'You can increase power in your serve by bending your legs more.'    
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.05) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.05):
        leg_tip_load = 'You can slightly increase power in your serve by bending your legs a small amount.' 
        score_lost += 2
   # leaning forward during takeback
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.20) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.80):
        leg_tip_load = 'Your lower body is leaning significantly too far forward during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.10) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.90):
        leg_tip_load = 'Your lower body may be leaning too far forward during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.05) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.95):
        leg_tip_load = 'Your lower body may be leaning slightly forward during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 2
    # leaning backward during takeback
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.80) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.20):
        leg_tip_load = 'Your lower is leaning significantly too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.90) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.10):
        leg_tip_load = 'Your lower body is leaning too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.95) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.05):
        leg_tip_load = 'Your lower body is leaning slightly too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        score_lost += 2
    else:
        leg_tip_load = 'Your legs are well balanced during your takeback, and your legs are loading very well!'
    return [leg_tip_load, score_lost]

def legs_tips_extend(user, playerright_leg, playerleft_leg):
    score_lost = 0
    leg_tip_extend = None
    # not extending enough during contact
    if user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.80) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.80):
        leg_tip_extend = 'Your legs are significantly under extending during contact. Make sure to immensely increase drive with you legs on your extension.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.90) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.90):
        leg_tip_extend = 'Your legs are under extending during contact. Make sure to drive more with you legs on your extension.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.95) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.95):
        leg_tip_extend = 'Your legs are slightly under extending  during contact. Make sure to drive slightly more with you legs on your extension.'
        score_lost += 2
    # mirroring extension with the legs
    elif user.get_max_data('hip2ankle_right')[2] > (playerright_leg.get_max_data()[2] * 1.10) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.90):
        leg_tip_extend = 'Your back leg should extend more to be closer in line with your front leg during extension and contact.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.90) and user.get_max_data('hip2ankle_left')[2] > (playerleft_leg.get_max_data()[2] * 1.10):
        leg_tip_extend = 'Your front leg should extend more to be closer in line with your back leg during extension and contact.'
        score_lost += 4
    else:
        leg_tip_extend = 'Good job! Your legs are optimally extending on contact and consistently mirroring eachother.'
    return [leg_tip_extend, score_lost]

def legs_tips_finish(user, playerleft_leg):
    score_lost = 0
    leg_tip_finish = None

    if user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.80):
        leg_tip_finish = 'You are dipping your front leg significantly too much during the finish. Try landing a lot taller in the legs to optimize your recovery.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.90):
        leg_tip_finish = 'You are dipping your front leg too much during the finish. Try landing taller in the legs to optimize your recovery.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.95):
        leg_tip_finish = 'You are dipping your front leg slightly too much during the finish. Try landing a bit taller in the legs to optimize your recovery.'
        score_lost += 2
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.20):
        leg_tip_finish = 'You are standing significantly too tall during your finish. Try getting a lot lower in the legs to absorb your impact with the ground.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.10):
        leg_tip_finish = 'You are standing too tall during your finish. Try getting lower in the legs to absorb your impact with the ground.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.05):
        leg_tip_finish = 'You are standing slightly too tall during your finish. Try getting a bit lower in the legs to absorb your impact with the ground.'
        score_lost += 2
    else:
        leg_tip_finish = 'You are landing in a great position that is optimal for balance and recovery!'
    return [leg_tip_finish, score_lost]


def leg_score(user, playerright_leg, playerleft_leg):
    leg_start = legs_tips_start(user, playerright_leg, playerleft_leg)
    leg_load = legs_tips_load(user, playerright_leg, playerleft_leg)
    leg_extend = legs_tips_extend(user, playerright_leg, playerleft_leg)
    leg_finish = legs_tips_finish(user, playerright_leg)
    leg_tip_list = [leg_start, leg_load, leg_extend, leg_finish]
    score = []
    for i in leg_tip_list:
        score.append(i[0])
    return score

def leg_score_quant(user, playerright_leg, playerleft_leg):
    leg_start = legs_tips_start(user, playerright_leg, playerleft_leg)
    leg_load = legs_tips_load(user, playerright_leg, playerleft_leg)
    leg_extend = legs_tips_extend(user, playerright_leg, playerleft_leg)
    leg_finish = legs_tips_finish(user, playerright_leg)
    leg_tip_list = [leg_start, leg_load, leg_extend, leg_finish]
    score = []
    for i in leg_tip_list:
        score.append(i[-1])
    return score

# Arms
def arms_tips_start(user, playerright_arm, playerleft_arm):
    arm_tip_start_right = None
    arm_tip_start_both = None
    score = 0
    # right arm extended out too much
    if user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.20):
        arm_tip_start_right = 'Dominant arm is extended out significantly too much during the starting position.  Tuck your arm in a large amount to minimize the time it takes to start the takeback.'
        score += 7
    elif user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.10):
        arm_tip_start_right = 'Dominant arm is extended out too much during the starting position.  Tuck your arm in more to minimize the time it takes to start the takeback.'
        score += 4
    elif user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.05):
        arm_tip_start_right = 'Dominant arm is extended out slightly too much during the starting position.  Tuck your arm in a bit more to slightly minimize the time it takes to start the takeback.'
        score += 2
    # right arm tucked in too much
    elif user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.80):
        arm_tip_start_right = 'Dominant arm is tucked in significantly too much during the starting position.  Extend your arm out a large amout to to increase momentum going into the takeback.'
        score += 7
    elif user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.90):
        arm_tip_start_right = 'Dominant arm is tucked in too much during the starting position.  Extend your arm out more to to increase momentum going into the takeback.'
        score += 4
    elif user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.95):
        arm_tip_start_right = 'Dominant arm is tucked in slightly too much during the starting position.  Extend your arm out a bit more to to increase momentum going into the takeback.'
        score += 2
    else:
        arm_tip_start_right = 'Great works, your racquet seems to be starting in the right spot based on your right arm position!'
    
    # arms not aligned 
    if user.get_average_data('shoulder2wrist_left')[0] > (playerleft_arm.get_average_data()[0] * 1.20) and user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.80):
        arm_tip_start_both = 'Arms are significantly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        score += 7
    elif user.get_average_data('shoulder2wrist_left')[0] > (playerleft_arm.get_average_data()[0] * 1.10) and user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.90):
        arm_tip_start_both = 'Arms are not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        score += 4
    elif user.get_average_data('shoulder2wrist_left')[0] > (playerleft_arm.get_average_data()[0] * 1.05) and user.get_average_data('shoulder2wrist_right')[0] < (playerright_arm.get_average_data()[0] * 0.95):
        arm_tip_start_both = 'Arms are slightly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        score += 2
    elif user.get_average_data('shoulder2wrist_left')[0] < (playerleft_arm.get_average_data()[0] * 0.80) and user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.20):
        arm_tip_start_both = 'Arms are significantly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        score += 7
    elif user.get_average_data('shoulder2wrist_left')[0] < (playerleft_arm.get_average_data()[0] * 0.90) and user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.10):
        arm_tip_start_both = 'Arms are not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        score += 4
    elif user.get_average_data('shoulder2wrist_left')[0] < (playerleft_arm.get_average_data()[0] * 0.95) and user.get_average_data('shoulder2wrist_right')[0] > (playerright_arm.get_average_data()[0] * 1.05):
        arm_tip_start_both = 'Arms are slightly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        score += 2
    else:
        arm_tip_start_both = 'Overall, arms are aligned well during the starting position!'
    arm_tips_start = [arm_tip_start_right, arm_tip_start_both, score]
    return arm_tips_start

def arms_tips_load(user, playerright_arm, playerleft_arm):
    arm_tip_load_right = None
    arm_tip_load_left = None
    score = 0
    # bending arm too much 
    if user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.80):
        arm_tip_load_right = 'You are bending your dominant arm significantly too much on the loadup.  Extend your arm a lot more for more power.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.90):
        arm_tip_load_right = 'You are bending your dominant arm too much on the loadup.  Extend your arm to a comfortable position for more power.'
        score += 4
    elif user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.95):
        arm_tip_load_right = 'You are bending your dominant arm slightyl too much on the loadup.  Extend your arm a bit to a comfortable position for more power.'
        score += 2
    # not enough arm bend
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.20):
        arm_tip_load_right = 'You are significantly under retracting your dominant arm in the loadup.  Bend your arm a lot more to a comfortable position for more power.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.10):
        arm_tip_load_right = 'You are not bending your dominant arm enough on the loadup.  Bend your arm to a comfortable position for more power.'
        score += 4
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.05):
        arm_tip_load_right = 'You are not bending your dominant arm slightly enough on the loadup.  Bend your arm a bit to a comfortable position for more power.'
        score += 2
    else: 
        arm_tip_load_right = 'great work, your right arm is optimzed for power in the loadup!'
    
    # arm extension during toss
    if user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.80):
        arm_tip_load_left = 'Weak arm extention throughout the toss is significantly inconsistent.  Try to keep your left arm a lot straighter on the takeback and load.'
        score += 7
    elif user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.90):
        arm_tip_load_left = 'Weak arm extention throughout the toss is inconsistent.  Try to keep your left arm straighter on the takeback and load.'
        score += 4
    elif user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.95):
        arm_tip_load_left = 'Weak arm extention throughout the toss is slightly inconsistent.  Try to keep your left arm a bit straighter on the takeback and load.'
        score += 2
    else:
        arm_tip_load_left = 'Your tossing arm looks very fluid and consistent!'
    arm_tips_load = [arm_tip_load_right, arm_tip_load_left, score]
    return arm_tips_load


def arms_tips_extend(user, playerright_arm):
    arm_tip_extend_right = None
    score = 0
    if user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.80):
        arm_tip_extend_right = 'Dominant arm is significantly not extending enough during contact. Make sure to either toss the ball a lot higher and/or make contact at its apex.'
        score += 7
    elif user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.90):
        arm_tip_extend_right = 'Dominant arm is not extending enough during contact. Make sure to either toss the ball higher and/or make contact at its apex.'
        score += 4
    elif user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.95):
        arm_tip_extend_right = 'Dominant arm is slightly not extending enough during contact. Make sure to either toss the ball a bit higher and/or make contact at its apex.'
        score += 2
    else:
        arm_tip_extend_right = 'Good job, your arm is optimally extended on contact!'
    arm_tips_extend = [arm_tip_extend_right, score]
    return arm_tips_extend

def arms_tips_finish(user, playerleft_arm):
    arm_tip_finish_left = None
    score = 0
    if user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.20):
        arm_tip_finish_left = 'Your weak arm should be significantly closer to your body in preparation for an easier recovery of the racquet.'
        score += 7
    elif user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.10):
        arm_tip_finish_left = 'Your weak arm should be closer to your body in preparation for an easier recovery of the racquet.'
        score += 4
    elif user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.05):
        arm_tip_finish_left = 'Your weak arm should be slightly closer to your body in preparation for an easier recovery of the racquet.'
        score += 2
    else:
        arm_tip_finish_left = 'Nice, your arms seem to be positioned correctly on the finish!  Racquet recovery is much easier with optimal arm placement.'
    arm_tips_finish = [arm_tip_finish_left, score]
    return arm_tips_finish


def arm_tip_summary(user, playerright_arm, playerleft_arm):
    full_arm_list = []
    arm_start = arms_tips_start(user, playerright_arm, playerleft_arm)
    arm_load = arms_tips_load(user, playerright_arm, playerleft_arm)
    arm_extend = arms_tips_extend(user, playerright_arm)
    arm_finish = arms_tips_finish(user, playerleft_arm)
    arm_tip_list = [arm_start, arm_load, arm_extend, arm_finish]
    for i in arm_tip_list:
        for j in i:
            if type(j) != int:
                full_arm_list.append(j)
    return full_arm_list

def arm_score_quant(user, playerright_arm, playerleft_arm):
    arm_start = arms_tips_start(user, playerright_arm, playerleft_arm)
    arm_load = arms_tips_load(user, playerright_arm, playerleft_arm)
    arm_extend = arms_tips_extend(user, playerright_arm)
    arm_finish = arms_tips_finish(user, playerleft_arm)
    arm_tip_list = [arm_start, arm_load, arm_extend, arm_finish]
    score = []
    for i in arm_tip_list:
        score.append(i[-1])
        
    return score

# body
def body_tips_start(user, playerright_body):
    body_tip_start = None
    score_lost = 0
    # less than the pro angles
    if user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.80):
        body_tip_start = 'Your dominant arm is hanging significantly too low on the starting position.  Try raising your are by a large amount.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.90):
        body_tip_start = 'Your dominant arm is hanging too low on the starting position.  Try raising your amount.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.95):
        body_tip_start = 'Your dominant arm is hanging slightly too low on the starting position.  Try raising your are by a small amount.'
        score_lost += 2
    # grater than the pro angles
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.20):
        body_tip_start = 'Your dominant arm is raised significantly too high on the starting position.  Try lowering your are by a large amount.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.10):
        body_tip_start = 'Your dominant arm is raised too high on the starting position.  Try lowering your amount.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.05):
        body_tip_start = 'Your dominant arm is raised slightly too high on the starting position.  Try lowering your are by a small amount.'
        score_lost += 2
    else:
        body_tip_start = 'Your upper arms are the perfect distance from your body!'
    return [body_tip_start, score_lost]

def body_tips_load(user, playerleft_body):
    score_lost = 0
    body_tip_load_left = None
    # bending legs too much during load
    if  user.get_max_data('elbow2hip_left')[1] < (playerleft_body.get_max_data()[1] * 0.80):
        body_tip_load_left = 'The tossing side of your body is significantly under stretching during the load. Try to reach up with your tossing arm a lot more.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_left')[1] < (playerleft_body.get_min_data()[1] * 0.90):
        body_tip_load_left = 'The tossing side of your body is under stretching during the load. Try to reach up with your tossing arm more.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_left')[1] < (playerleft_body.get_min_data()[1] * 0.95):
        body_tip_load_left = 'The tossing side of your body is slighly under stretching during the load. Try to reach up with your tossing arm a bit more.'
        score_lost += 2
    elif  user.get_max_data('elbow2hip_left')[1] > (playerleft_body.get_max_data()[1] * 0.80):
        body_tip_load_left = 'The tossing side of your body is stretching significantly too much during the load. Try to align your tossing arm with the side of your body a lot more.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_left')[1] > (playerleft_body.get_min_data()[1] * 0.90):
        body_tip_load_left = 'The tossing side of your body is stretching too much during the load. Try to align your tossing arm with the side of your body more.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_left')[1] > (playerleft_body.get_min_data()[1] * 0.95):
        body_tip_load_left = 'The tossing side of your body is stretching slightly too much during the load. Try to align your tossing arm with the side of your body slightly more.'
        score_lost += 2
    else:
        body_tip_load_left = 'Your tossing arm and subsequent extension of your side look perfect on the toss!'
    return [body_tip_load_left, score_lost]

def body_tips_extend(user, playerright_body):
    score_lost = 0
    body_tip_extend = None
    # not extending enough during contact
    if user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.80):
        body_tip_extend = 'Your elbow on the dominant arm is significantly too low relative to your shoulder during the extension before contact.  Try strongly adjusting your toss or your body position during extension'
        score_lost += 7
    elif user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.90):
        body_tip_extend = 'Your elbow on the dominant arm is too low relative to your shoulder during the extension before contact.  Try adjusting your toss or your body position during extension'
        score_lost += 4
    elif user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.95):
        body_tip_extend = 'Your elbow on the dominant arm is slightly too low relative to your shoulder during the extension before contact.  Try partially adjusting your toss or your body position during extension'
        score_lost += 2
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 0.80):
        body_tip_extend = 'Your elbow on the dominant arm is significantly too high relative to your shoulder during the extension before contact.  Try strongly adjusting your toss or your body position during extension'
        score_lost += 7
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 0.90):
        body_tip_extend = 'Your elbow on the dominant arm is too high relative to your shoulder during the extension before contact.  Try adjusting your toss or your body position during extension'
        score_lost += 4
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 0.95):
        body_tip_extend = 'Your elbow on the dominant arm is slightly too high relative to your shoulder during the extension before contact.  Try partially adjusting your toss or your body position during extension'
        score_lost += 2
    else:
        body_tip_extend = 'Good job! the side of your body looks great during the extension into contact.  The toss is maximized for body involvement in the serve.'
    return [body_tip_extend, score_lost]




def body_score(user, playerright_body, playerleft_body):
    body_start = body_tips_start(user, playerright_body)
    body_load = body_tips_load(user, playerleft_body)
    body_extend = body_tips_extend(user, playerright_body)
    body_tip_list = [body_start, body_load, body_extend]
    score = []
    for i in body_tip_list:
        score.append(i[0])
    return score

def body_score_quant(user, playerright_body, playerleft_body):
    body_start = body_tips_start(user, playerright_body)
    body_load = body_tips_load(user, playerleft_body)
    body_extend = body_tips_extend(user, playerright_body)
    body_tip_list = [body_start, body_load, body_extend]
    score = []
    for i in body_tip_list:
        score.append(i[-1])
    return score

def total_score(user, playerright_leg, playerleft_leg, playerright_arm, playerleft_arm, playerright_body, playerleft_body):
    legs = sum(leg_score_quant(user, playerright_leg, playerleft_leg))
    arms = sum(arm_score_quant(user, playerright_arm, playerleft_arm))
    body = sum(body_score_quant(user, playerright_body, playerleft_body))
    score = 100 - (arms + legs + body)
    if score < 0:
        score = 0
    return score












