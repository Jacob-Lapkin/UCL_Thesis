from numpy.lib.shape_base import split
from pose.pro_angle_data import smoothed_df, phase_divider, grab_label, split_data, split_label, display_df
from pose.user_angle_data import smoothed_user_df, grab_user_label, display_user_df, phase_user_divider
from pose.multi_class_azure import StrokeList
from pose.recommendations_data import *
import matplotlib.pyplot as plt
import random

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
    leg_tip_start_first = None
    leg_tip_start_second = None

    score_lost = 0

    # less than the pro angles
    if user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.80) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.80):
        leg_tip_start_first = 'Try to standup significantly more during your ready position.'
        leg_tip_start_second = 'Stand remarkably higher on your ready position.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.90) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.90):
        leg_tip_start_first = 'Try to standup more during your ready position.'
        leg_tip_start_second = 'Stand higher on your ready position.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 0.95) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 0.95):
        leg_tip_start_first = 'Try to standup more during your ready position.'
        leg_tip_start_second = 'Stand slightly higher on your ready position.'
        score_lost += 2
    # grater than the pro angles
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.20) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.20):
        leg_tip_start_first = 'Try to bend your legs significantly more during your ready position.'
        leg_tip_start_second = 'Your legs are much too straight on the ready position.  Bend them remarkably more.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.10) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.10):
        leg_tip_start_first = 'Try to bend your legs more during your ready position.'
        leg_tip_start_second = 'Your legs are too straight on the ready position.  Bend them more.'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.05) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.05):
        leg_tip_start_first = 'Try to bend your legs slightly more during your ready position.'
        leg_tip_start_second = 'Your legs are slightly too straight on the ready position.  Bend them a bit more.'
        score_lost += 2
    # greater than one angle and less than the other
    elif user.get_max_data('hip2ankle_right')[0] > (playerright_leg.get_max_data()[0] * 1.20) and user.get_max_data('hip2ankle_left')[0] < (playerleft_leg.get_max_data()[0] * 1.20):
        leg_tip_start_first = 'Your legs seem to be starting at significantly contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        leg_tip_start_second = 'Your legs are strongly out of sync. Try mirroring your leg positions significantly more during the ready position'

        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 1.10) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.10):
        leg_tip_start_first = 'Your legs seem to be starting at contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        leg_tip_start_second = 'Your legs are out of sync. Try mirroring your leg positions more during the ready position'
        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[0] < (playerright_leg.get_max_data()[0] * 1.05) and user.get_max_data('hip2ankle_left')[0] > (playerleft_leg.get_max_data()[0] * 1.05):
        leg_tip_start_first = 'Your legs seem to be starting at slighty contrasting angles. Try copying your leg positions more during your ready position to increase balance.'
        leg_tip_start_second = 'Your legs are slightly out of sync. Try mirroring your leg positions slightly more during the ready position'
        score_lost += 2
    else:
        leg_tip_start_first = 'Your legs are placed well, and your lower body posture looks good!'
        leg_tip_start_second = 'You do not need to adjust your legs on your ready position.  Your lower body posture looks good!'
    pick_from_this = [leg_tip_start_first, leg_tip_start_second]
    leg_tip_start = random.choice(pick_from_this)
    return [leg_tip_start, score_lost]

def legs_tips_load(user, playerright_leg, playerleft_leg):
    score_lost = 0
    leg_tip_load_first = None
    leg_tip_load_second = None
    # bending legs too much during load
    if user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.80) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.80):
        leg_tip_load_first = 'You are loading your back leg too extremely. try standing much taller during your take back.'
        leg_tip_load_second = 'You do not need to bend your back leg so extremely on the load. Try standing up much more on your takeback to keep yourself from being too low.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.90) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.90):
        leg_tip_load_first = 'You are loading your back legs too much, try standing taller during your take back.'
        leg_tip_load_second = 'You do not need to bend your back leg that much on the load. Try standing up more on your takeback to keep yourself from being too low.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.95) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.95):
        leg_tip_load_first = 'You are loading your back legs a bit too much, try standing slightly taller during your take back.'
        leg_tip_load_second = 'Your are bending your back leg slightly too much on the load. Try standing up a bit more on your takeback to keep yourself from being too low.'
        score_lost += 2
    # not bedning legs enough during laod
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.20) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.20):
        leg_tip_load_first = 'You can significatly increase power in your serve by bending your legs a convincing amount.'
        leg_tip_load_second = 'Bend your legs much more to significantly decrease the angle of them in your load and subsequently significantly increase power'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.10) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.10):
        leg_tip_load_first = 'You can increase power in your serve by bending your legs more.'    
        leg_tip_load_second = 'Bend your legs more to decrease the angle of them in your load and subsequently increase power'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.05) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.05):
        leg_tip_load_first = 'You can slightly increase power in your serve by bending your legs a small amount.' 
        leg_tip_load_second = 'Bend your legs slightly more to decrease the angle of them in your load and subsequently slightly increase power'
        score_lost += 2
   # leaning forward during takeback
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.20) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.80):
        leg_tip_load_first = 'Your lower body is leaning significantly too far forward during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning ramarkably too far forward during your takeback.  Try to mirror your legs much more.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.10) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.90):
        leg_tip_load_first = 'Your lower body may be leaning too far forward during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning too far forward during your takeback.  Try to mirror your legs more.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] > (playerright_leg.get_min_data()[1] * 1.05) and user.get_min_data('hip2ankle_left')[1] < (playerleft_leg.get_min_data()[1] * 0.95):
        leg_tip_load_first = 'Your lower body may be leaning slightly forward during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning a bit too far forward during your takeback.  Try to mirror your legs a small fraction more.'
        score_lost += 2
    # leaning backward during takeback
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.80) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.20):
        leg_tip_load_first = 'Your lower body is leaning significantly too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning ramarkably too far back during your takeback.  Try to mirror your legs much more.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.90) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.10):
        leg_tip_load_first = 'Your lower body is leaning too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning too far back during your takeback.  Try to mirror your legs more.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_right')[1] < (playerright_leg.get_min_data()[1] * 0.95) and user.get_min_data('hip2ankle_left')[1] > (playerleft_leg.get_min_data()[1] * 1.05):
        leg_tip_load_first = 'Your lower body is leaning slightly too far back during you takeback. Try to more equally match the bend in your right and left legs.'
        leg_tip_load_second = 'You seem to be leaning a bit too far back during your takeback.  Try to mirror your legs a small fraction more.'
        score_lost += 2
    else:
        leg_tip_load_first = 'Your legs are well balanced during your takeback, and your legs are loading very well!'
        leg_tip_load_second = 'Your balance does not need any improvement at this point because your legs are loading very well!'
    pick_from_this = [leg_tip_load_first, leg_tip_load_second]
    leg_tip_load = random.choice(pick_from_this)
    return [leg_tip_load, score_lost]

def legs_tips_extend(user, playerright_leg, playerleft_leg):
    score_lost = 0
    leg_tip_extend_first = None
    leg_tip_extend_second = None

    # not extending enough during contact
    if user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.80) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.80):
        leg_tip_extend_first = 'Your legs are significantly under extending during contact. Make sure to immensely increase drive with you legs on your extension.'
        leg_tip_extend_second = 'You are remarkably too low on your extension during contact.  Drive much more with your legs to be straighter on contact.'
        score_lost += 7
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.90) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.90):
        leg_tip_extend_first = 'Your legs are under extending during contact. Make sure to drive more with you legs on your extension.'
        leg_tip_extend_second = 'You are too low on your extension during contact.  Drive more with your legs to be straighter on contact.'

        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.95) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.95):
        leg_tip_extend_first = 'Your legs are slightly under extending  during contact. Make sure to drive slightly more with you legs on your extension.'
        leg_tip_extend_second = 'You are slightly too low on your extension during contact.  Drive a bit more with your legs to be straighter on contact.'
        score_lost += 2
    # mirroring extension with the legs
    elif user.get_max_data('hip2ankle_right')[2] > (playerright_leg.get_max_data()[2] * 1.10) and user.get_max_data('hip2ankle_left')[2] < (playerleft_leg.get_max_data()[2] * 0.90):
        leg_tip_extend_first = 'Your back leg should extend more to be closer in line with your front leg during extension and contact.'
        leg_tip_extend_second = 'Your legs should be closely in line during extension and contact.  Try to extend your back leg more to accompish this.'

        score_lost += 4
    elif user.get_max_data('hip2ankle_right')[2] < (playerright_leg.get_max_data()[2] * 0.90) and user.get_max_data('hip2ankle_left')[2] > (playerleft_leg.get_max_data()[2] * 1.10):
        leg_tip_extend_first = 'Your front leg should extend more to be closer in line with your back leg during extension and contact.'
        leg_tip_extend_second = 'Your legs should be closely in line during extension and contact.  Try to extend your front leg more to accompish this.'
        score_lost += 4
    else:
        leg_tip_extend_first = 'Good job! Your legs are optimally extending on contact and consistently mirroring eachother.'
        leg_tip_extend_second = 'Your legs are optimally extending on contact and consistently mirroring eachother! There is no need to adjust your legs during your extension.'
    pick_from_this = [leg_tip_extend_first, leg_tip_extend_second]
    leg_tip_extend = random.choice(pick_from_this)
    return [leg_tip_extend, score_lost]

def legs_tips_finish(user, playerleft_leg):
    score_lost = 0
    leg_tip_finish_first = None
    leg_tip_finish_second = None

    if user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.80):
        leg_tip_finish_start = 'You are dipping your front leg significantly too much during the finish. Try landing a lot taller in the legs to optimize your recovery.'
        leg_tip_finish_second = 'Your front leg is absorbing remarkably too much on the finish.  You need to finish much taller to have a better chance at recovery.'
        score_lost += 7
    elif user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.90):
        leg_tip_finish_first = 'You are dipping your front leg too much during the finish. Try landing taller in the legs to optimize your recovery.'
        leg_tip_finish_second = 'Your front leg is absorbing too strongly on the finish.  You need to finish taller to have a better chance at recovery.'
        score_lost += 4
    elif user.get_min_data('hip2ankle_left')[3] < (playerleft_leg.get_min_data()[3] * 0.95):
        leg_tip_finish_first = 'You are dipping your front leg slightly too much during the finish. Try landing a bit taller in the legs to optimize your recovery.'
        leg_tip_finish_second = 'Your front leg is absorbing slightly too much on the finish.  You need to finish a bit taller to have a better chance at recovery.'
        score_lost += 2
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.20):
        leg_tip_finish_first = 'You are standing significantly too tall during your finish. Try getting a lot lower in the legs to absorb your impact with the ground.'
        leg_tip_finish_second = 'You are remarkably too high on the finish.  You need to get much lower and absorb the impact with your legs more.  '
        score_lost += 7
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.10):
        leg_tip_finish_first = 'You are standing too tall during your finish. Try getting lower in the legs to absorb your impact with the ground.'
        leg_tip_finish_second = 'You are too high on the finish.  You need to get lower and absorb the impact with your legs more.  '
        score_lost += 4
    elif user.get_min_data('hip2ankle_left')[3] > (playerleft_leg.get_min_data()[3] * 1.05):
        leg_tip_finish_first = 'You are standing slightly too tall during your finish. Try getting a bit lower in the legs to absorb your impact with the ground.'
        leg_tip_finish_second = 'You are slightly too high on the finish.  You need to get a bit lower and absorb the impact with your legs more.  '
        score_lost += 2
    else:
        leg_tip_finish_first = 'You are landing in a great position that is optimal for balance and recovery!'
        leg_tip_finish_second = 'Your landing is neither to0 low nor too high! You are optimzed for a strong recovery after the serve.'
    pick_from_this = [leg_tip_finish_first, leg_tip_finish_second]
    leg_tip_finish = random.choice(pick_from_this)
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
    arm_tip_start_right_first = None
    arm_tip_start_right_first = None
    arm_tip_start_both_first = None
    arm_tip_start_both_second = None

    score = 0
    # right arm extended out too much
    if user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.20):
        arm_tip_start_right_first = 'Dominant arm is extended out significantly too much during the starting position.  Tuck your arm in a large amount to minimize the time it takes to start the takeback.'
        arm_tip_start_right_second = 'Dominant arm is extended out notably too much during the starting position. Tuck your arm in a huge amount to minimize the time it takes to start the takeback.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.10):
        arm_tip_start_right_first = 'Dominant arm is extended out too much during the starting position.  Tuck your arm in more to minimize the time it takes to start the takeback.'
        arm_tip_start_right_second = 'The dominant arm does not need to be extended out that much during the starting position. Tuck your arm in to minimize the time it takes to start the takeback.'
        score += 4
    elif user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.05):
        arm_tip_start_right_first = 'Dominant arm is extended out slightly too much during the starting position.  Tuck your arm in a bit more to slightly minimize the time it takes to start the takeback.'
        arm_tip_start_right_second = 'The dominant arm is slightly over-extended during the starting position. Tuck your arm in a bit to minimize the time it takes to start the takeback.'
        score += 2
    # right arm tucked in too much
    elif user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.80):
        arm_tip_start_right_first = 'Dominant arm is tucked in significantly too much during the starting position.  Extend your arm out a large amout to to increase momentum going into the takeback.'
        arm_tip_start_right_second = 'Your momentum going into the takeback could increase significantly if your dominant arm is tucked in remarkably more during the starting position.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.90):
        arm_tip_start_right_first = 'Dominant arm is tucked in too much during the starting position.  Extend your arm out more to to increase momentum going into the takeback.'
        arm_tip_start_right_second = 'Your momentum going into the takeback could increase if your dominant arm is tucked in more during the starting position.'
        score += 4
    elif user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.95):
        arm_tip_start_right_first = 'Dominant arm is tucked in slightly too much during the starting position.  Extend your arm out a bit more to to increase momentum going into the takeback.'
        arm_tip_start_right_second = 'Your momentum going into the takeback could slightly increase if your dominant arm is tucked in a bit more during the starting position.'
        score += 2
    else:
        arm_tip_start_right_first = 'Great works, your racquet seems to be starting in the right spot based on your right arm position!'
        arm_tip_start_right_second = 'Your momentum going into the takeback could slightly increase if your dominant arm is tucked in a bit more during the starting position.'

    
    # arms not aligned 
    if user.get_min_data('shoulder2wrist_left')[0] > (playerleft_arm.get_min_data()[0] * 1.20) and user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.80):
        arm_tip_start_both_first = 'Arms are significantly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        arm_tip_start_both_second = 'Arms are significantly unaligned during starting position.  Your arms need to copy each other more closely by bending your left and/or retracting your right.'
        score += 7
    elif user.get_min_data('shoulder2wrist_left')[0] > (playerleft_arm.get_min_data()[0] * 1.10) and user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.90):
        arm_tip_start_both_first = 'Arms are not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        arm_tip_start_both_second = 'Arms are unaligned during starting position.  Your arms need to copy each other more closely by bending your left and/or retracting your right.'
        score += 4
    elif user.get_min_data('shoulder2wrist_left')[0] > (playerleft_arm.get_min_data()[0] * 1.05) and user.get_min_data('shoulder2wrist_right')[0] < (playerright_arm.get_min_data()[0] * 0.95):
        arm_tip_start_both_first = 'Arms are slightly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your left and/or retracting your right.'
        arm_tip_start_both_second = 'Arms are slightly unaligned during starting position.  Your arms need to copy each other more closely by bending your left and/or retracting your right.'
        score += 2
    elif user.get_min_data('shoulder2wrist_left')[0] < (playerleft_arm.get_min_data()[0] * 0.80) and user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.20):
        arm_tip_start_both_first = 'Arms are significantly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        arm_tip_start_both_second = 'Arms are significantly unaligned during starting position.  Your arms need to copy each other more closely by bending your right and/or retracting your left.'
        score += 7
    elif user.get_min_data('shoulder2wrist_left')[0] < (playerleft_arm.get_min_data()[0] * 0.90) and user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.10):
        arm_tip_start_both_first = 'Arms are not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        arm_tip_start_both_second = 'Arms are unaligned during starting position.  Your arms need to copy each other more closely by bending your right and/or retracting your left.'
        score += 4
    elif user.get_min_data('shoulder2wrist_left')[0] < (playerleft_arm.get_min_data()[0] * 0.95) and user.get_min_data('shoulder2wrist_right')[0] > (playerright_arm.get_min_data()[0] * 1.05):
        arm_tip_start_both_first = 'Arms are slightly not aligned enough during starting position.  Your arms should mirror each other more closely by bending your right arm and/or retracting your left arm.'
        arm_tip_start_both_second = 'Arms are slightly unaligned during starting position.  Your arms need to copy each other more closely by bending your right and/or retracting your left.'
        score += 2
    else:
        arm_tip_start_both_first = 'Overall, arms are aligned well during the starting position!'
        arm_tip_start_both_second = 'Goodjob, arms are aligned well during the starting position!'

    pick_from_this_right = [arm_tip_start_right_first, arm_tip_start_right_second]
    pick_from_this_both = [arm_tip_start_both_first, arm_tip_start_both_second]
    arm_tip_start_right = random.choice(pick_from_this_right)
    arm_tip_start_both = random.choice(pick_from_this_both)
    arm_tips_start = [arm_tip_start_right, arm_tip_start_both, score]
    return arm_tips_start

def arms_tips_load(user, playerright_arm, playerleft_arm):
    arm_tip_load_right_first = None
    arm_tip_load_right_second = None
    arm_tip_load_left_first = None
    arm_tip_load_left_second = None
    score = 0
    # bending arm too much 
    if user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.80):
        arm_tip_load_right_first = 'You are bending your dominant arm significantly too much on the loadup.  Extend your arm a lot more for more power.'
        arm_tip_load_right_second= 'To increase power by a large amount, you should extend your dominant arm much more because you are bending it significantly too much on the loadup.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.90):
        arm_tip_load_right_first = 'You are bending your dominant arm too much on the loadup.  Extend your arm to a comfortable position for more power.'
        arm_tip_load_right_second= 'To increase power, you should extend your dominant arm more because you are bending it too much on the loadup.'
        score += 4
    elif user.get_min_data('shoulder2wrist_right')[1] < (playerright_arm.get_min_data()[1] * 0.95):
        arm_tip_load_right_first = 'You are bending your dominant arm slightyl too much on the loadup.  Extend your arm a bit to a comfortable position for more power.'
        arm_tip_load_right_second= 'To slightly increase power, you should extend your dominant arm a bit more because you are bending it fractionally too much on the loadup.'
        score += 2
    # not enough arm bend
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.20):
        arm_tip_load_right_first = 'You are significantly under retracting your dominant arm in the loadup.  Bend your arm a lot more to a comfortable position for more power.'
        arm_tip_load_right_second= 'You are is extended significantly too much on your dominant arm in the loadup.  Bend your arm a lot more to a comfortable position for more power.'
        score += 7
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.10):
        arm_tip_load_right_first = 'You are not bending your dominant arm enough on the loadup.  Bend your arm to a comfortable position for more power.'
        arm_tip_load_right_second= 'You are is extended too much on your dominant arm in the loadup.  Bend your arm a lot more to a comfortable position for more power.'

        score += 4
    elif user.get_min_data('shoulder2wrist_right')[1] > (playerright_arm.get_min_data()[1] * 1.05):
        arm_tip_load_right_first = 'You are not bending your dominant arm slightly enough on the loadup.  Bend your arm a bit to a comfortable position for more power.'
        arm_tip_load_right_second= 'You are is extended slightly too much on your dominant arm in the loadup.  Bend your arm a lot more to a comfortable position for more power.'
        score += 2
    else: 
        arm_tip_load_right_first = 'Great work, your dominant arm is optimzed for power in the loadup!'
        arm_tip_load_right_second= 'Good job, your dominant arm does not need any changes in the loadup at the moment because it is optimized for power!'
    # arm extension during toss
    if user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.80):
        arm_tip_load_left_first = 'Weak arm extention throughout the toss is significantly inconsistent.  Try to keep your left arm a lot straighter on the takeback and load.'
        arm_tip_load_left_second = 'the extension of your weak arm throughout the toss is significantly inconsistent.  Try to keep your left arm a lot straighter on the takeback and load.'
        score += 7
    elif user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.90):
        arm_tip_load_left_first = 'Weak arm extention throughout the toss is inconsistent.  Try to keep your left arm straighter on the takeback and load.'
        arm_tip_load_left_second = 'the extension of your weak arm throughout the toss is inconsistent.  Try to keep your left arm a lot straighter on the takeback and load.'
        score += 4
    elif user.get_average_data('shoulder2wrist_left')[1] < (playerleft_arm.get_average_data()[1] * 0.95):
        arm_tip_load_left_first = 'Weak arm extention throughout the toss is slightly inconsistent.  Try to keep your left arm a bit straighter on the takeback and load.'
        arm_tip_load_left_second = 'the extension of your weak arm throughout the toss is slightly inconsistent.  Try to keep your left arm a lot straighter on the takeback and load.'
        score += 2
    else:
        arm_tip_load_left_first = 'Your tossing arm looks very fluid and consistent!'
        arm_tip_load_left_second = 'Great work on the tossing arm in the load! it looks very fluid and consistent'

    pick_from_this_right = [arm_tip_load_right_first, arm_tip_load_right_second]
    pick_from_this_left = [arm_tip_load_left_first, arm_tip_load_left_second]
    arm_tip_load_right = random.choice(pick_from_this_right)
    arm_tip_load_left = random.choice(pick_from_this_left)
    arm_tips_load = [arm_tip_load_right, arm_tip_load_left, score]
    return arm_tips_load


def arms_tips_extend(user, playerright_arm):
    arm_tip_extend_right_first = None
    arm_tip_extend_right_second = None

    score = 0
    if user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.80):
        arm_tip_extend_right_first = 'Dominant arm is significantly not extending enough during contact. Make sure to either toss the ball a lot higher and/or make contact at its apex.'
        arm_tip_extend_right_second = 'When you make contact at the ball flights apex, make sure that your arm is extended out signficantly more.'
        score += 7
    elif user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.90):
        arm_tip_extend_right_first = 'Dominant arm is not extending enough during contact. Make sure to either toss the ball higher and/or make contact at its apex.'
        arm_tip_extend_right_second = 'When you make contact at the ball flights apex, make sure that your arm is extended out more.'
        score += 4
    elif user.get_max_data('shoulder2wrist_right')[2] < (playerright_arm.get_max_data()[2] * 0.95):
        arm_tip_extend_right_first = 'Dominant arm is slightly not extending enough during contact. Make sure to either toss the ball a bit higher and/or make contact at its apex.'
        arm_tip_extend_right_second = 'When you make contact at the ball flights apex, make sure that your arm is extended out slightly more.'
        score += 2
    else:
        arm_tip_extend_right_first = 'Good job, your dominant arm is optimally extended on contact!'
        arm_tip_extend_right_second = 'Nice, your dominant arm is extended the perfect amout!'

    pick_from_this_right = [arm_tip_extend_right_first, arm_tip_extend_right_second]
    arm_tip_extend_right = random.choice(pick_from_this_right)
    arm_tips_extend = [arm_tip_extend_right, score]
    return arm_tips_extend

def arms_tips_finish(user, playerleft_arm):
    arm_tip_finish_left_first = None
    arm_tip_finish_left_second = None
    score = 0
    if user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.20):
        arm_tip_finish_left_first = 'Your weak arm should be significantly closer to your body in preparation for an easier recovery of the racquet.'
        arm_tip_finish_left_second = 'Recovery is much easier if your weak arm is closer to your body. Try brining your weak arm significantly closer to your body on the finish.'
        score += 7
    elif user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.10):
        arm_tip_finish_left_first = 'Your weak arm should be closer to your body in preparation for an easier recovery of the racquet.'
        arm_tip_finish_left_second = 'Recovery is much easier if your weak arm is closer to your body. Try brining your weak arm closer to your body on the finish.'

        score += 4
    elif user.get_min_data('shoulder2wrist_left')[3] > (playerleft_arm.get_min_data()[3] * 1.05):
        arm_tip_finish_left_first = 'Your weak arm should be slightly closer to your body in preparation for an easier recovery of the racquet.'
        arm_tip_finish_left_second = 'Recovery is much easier if your weak arm is closer to your body. Try brining your weak arm slightly closer to your body on the finish.'
        score += 2
    else:
        arm_tip_finish_left_first = 'Nice, your arms seem to be positioned correctly on the finish!  Racquet recovery is much easier with optimal arm placement.'
        arm_tip_finish_left_second = 'Good job, your arms seem to be positioned correctly on the finish!  Racquet recovery is much easier with optimal arm placement.'
    pick_from_this_left = [arm_tip_finish_left_first, arm_tip_finish_left_second]
    arm_tip_finish_left = random.choice(pick_from_this_left)
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
    body_tip_start_first = None
    body_tip_start_second = None

    score_lost = 0
    # less than the pro angles
    if user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.80):
        body_tip_start_first = 'Your dominant arm is hanging significantly too low on the starting position.  Try raising your are by a large amount.'
        body_tip_start_second = 'Raise your dominant arm by a significant amount because it is hanging too low on the starting position'
        score_lost += 7
    elif user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.90):
        body_tip_start_first = 'Your dominant arm is hanging too low on the starting position.  Try raising your amount.'
        body_tip_start_second = 'Raise your dominant arm because it is hanging too low on the starting position'
        score_lost += 4
    elif user.get_min_data('elbow2hip_right')[0] < (playerright_body.get_min_data()[0] * 0.95):
        body_tip_start_first = 'Your dominant arm is hanging slightly too low on the starting position.  Try raising your are by a small amount.'
        body_tip_start_second = 'Raise your dominant arm by a slight amount because it is hanging too low on the starting position'
        score_lost += 2
    # grater than the pro angles
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.20):
        body_tip_start_first = 'Your dominant arm is raised significantly too high on the starting position.  Try lowering your are by a large amount.'
        body_tip_start_second = 'Lower your dominant arm by a large amount because it is hanging significantly too high on the starting position'
        score_lost += 7
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.10):
        body_tip_start_first = 'Your dominant arm is raised too high on the starting position.  Try lowering your amount.'
        body_tip_start_second = 'Lower your dominant arm because it is hanging too high on the starting position'
        score_lost += 4
    elif user.get_min_data('elbow2hip_right')[0] > (playerright_body.get_max_data()[0] * 1.05):
        body_tip_start_first = 'Your dominant arm is raised slightly too high on the starting position.  Try lowering your are by a small amount.'
        body_tip_start_second = 'Lower your dominant arm by a small amount because it is hanging slightly too high on the starting position'
        score_lost += 2
    else:
        body_tip_start_first = 'Your upper arms are the perfect distance from your body!'
        body_tip_start_second = 'Nice job, Your upper arms are the perfect distance from your body!'
    pick_from_this_body = [body_tip_start_first, body_tip_start_second]
    body_tip_start = random.choice(pick_from_this_body)
    return [body_tip_start, score_lost]

def body_tips_load(user, playerleft_body):
    score_lost = 0
    body_tip_load_left_first = None
    body_tip_load_left_second = None

    if  user.get_max_data('elbow2hip_left')[1] < (playerleft_body.get_max_data()[1] * 0.80):
        body_tip_load_left_first = 'The tossing side of your body is significantly under stretching during the load. Try to reach up with your tossing arm a lot more.'
        body_tip_load_left_second = 'Make sure to reach up with your tossing arm a lot more during the load because your tossing side of the body is significantly under stretching.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_left')[1] < (playerleft_body.get_min_data()[1] * 0.90):
        body_tip_load_left_first = 'The tossing side of your body is under stretching during the load. Try to reach up with your tossing arm more.'
        body_tip_load_left_second = 'Make sure to reach up with your tossing arm more during the load because your tossing side of the body is under stretching.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_left')[1] < (playerleft_body.get_min_data()[1] * 0.95):
        body_tip_load_left_first = 'The tossing side of your body is slighly under stretching during the load. Try to reach up with your tossing arm a bit more.'
        body_tip_load_left_second = 'Make sure to reach up with your tossing arm a bit more during the load because your tossing side of the body is slightly under stretching.'
        score_lost += 2
    elif  user.get_max_data('elbow2hip_left')[1] > (playerleft_body.get_max_data()[1] * 1.20):
        body_tip_load_left_first = 'The tossing side of your body is stretching significantly too much during the load. Try to align your tossing arm with the side of your body a lot more.'
        body_tip_load_left_second = 'Make sure align your tossing arm with the side of your body a lot more during the load because your tossing side of the body is stretching significantly too much.'
        score_lost += 7
    elif user.get_min_data('elbow2hip_left')[1] > (playerleft_body.get_min_data()[1] * 1.10):
        body_tip_load_left_first = 'The tossing side of your body is stretching too much during the load. Try to align your tossing arm with the side of your body more.'
        body_tip_load_left_second = 'Make sure align your tossing arm with the side of your body more during the load because your tossing side of the body is stretching too much.'
        score_lost += 4
    elif user.get_min_data('elbow2hip_left')[1] > (playerleft_body.get_min_data()[1] * 1.05):
        body_tip_load_left_first = 'The tossing side of your body is stretching slightly too much during the load. Try to align your tossing arm with the side of your body slightly more.'
        body_tip_load_left_second = 'Make sure align your tossing arm with the side of your body a bit more during the load because your tossing side of the body is stretching slightly too much.'
        score_lost += 2
    else:
        body_tip_load_left_first = 'Your tossing arm and subsequent extension of your side look perfect on the toss!'
        body_tip_load_left_second = "Nice, work your tossing arm and side extension don't need any work at the moment!"

    pick_from_this_body = [body_tip_load_left_first, body_tip_load_left_second]
    body_tip_load = random.choice(pick_from_this_body)
    return [body_tip_load, score_lost]

def body_tips_extend(user, playerright_body):
    score_lost = 0
    body_tip_extend = None
    # not extending enough during contact
    if user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.60):
        body_tip_extend = 'Your elbow on the dominant arm is significantly too low relative to your shoulder during the extension before contact.  Try strongly adjusting your toss or your body position during extension'
        score_lost += 7
    elif user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.80):
        body_tip_extend = 'Your elbow on the dominant arm is too low relative to your shoulder during the extension before contact.  Try adjusting your toss or your body position during extension'
        score_lost += 4
    elif user.get_max_data('elbow2hip_right')[2] < (playerright_body.get_max_data()[2] * 0.90):
        body_tip_extend = 'Your elbow on the dominant arm is slightly too low relative to your shoulder during the extension before contact.  Try partially adjusting your toss or your body position during extension'
        score_lost += 2
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 1.20):
        body_tip_extend = 'Your elbow on the dominant arm is significantly too high relative to your shoulder during the extension before contact.  Try strongly adjusting your toss or your body position during extension'
        score_lost += 7
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 1.10):
        body_tip_extend = 'Your elbow on the dominant arm is too high relative to your shoulder during the extension before contact.  Try adjusting your toss or your body position during extension'
        score_lost += 4
    elif user.get_max_data('elbow2hip_right')[2] > (playerright_body.get_max_data()[2] * 1.05):
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












