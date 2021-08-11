
import time
from datetime import datetime
import random
import string
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask.scaffold import F
#from myproject.models import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from werkzeug import datastructures
from wtforms import (Form, StringField, TextField, SubmitField, PasswordField,
                     SubmitField, BooleanField, DateField, RadioField, FileField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo 
from wtforms import ValidationError


from forms import point, Stroke

import os

# importing data FIX THIS PATH
from pose.canvas_data import (Player_data, User_data, legs_tips_start, legs_tips_load, legs_tips_extend, legs_tips_finish,
                            arm_tip_summary, leg_score, body_score, total_score, leg_score_left_handers, body_score_left_handers, total_score_left_handers, arm_tip_summary_left_handers)
from pose.converting import converter, make_frame_dir, delete_frames, make_video_dir, delete_user_video, is_empty

###########################
######### LOGIN/REGISTER FORMS #############
###########################
class Login(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Passsword", validators=[DataRequired()])
    submit = SubmitField("Log in")

class newform(FlaskForm):
    first = StringField("First Name", validators = [DataRequired()])
    last = StringField("Last Name", validators = [DataRequired()])
    dominant = RadioField('Dominant Arm', validators = [DataRequired()], choices=[('right','right'),('left','left')])
    email = StringField("Email Address", validators = [DataRequired(), Email(message='Email must include @ and/or .com', allow_empty_local=False)])
    password = PasswordField("Password", validators = [DataRequired()])
    passconfirm = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        exisitng_user_email = User.query.filter_by(email=email.data).first()
        if exisitng_user_email:
            flash('Email already registered', 'danger')
            raise ValidationError('Email already registered')

#####################
###### CONFIRG ######
#####################

app = Flask(__name__)
db = SQLAlchemy((app))

bcrypt = Bcrypt(app)
#old sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mykey'

#new sql db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Lizzy1641@127.0.0.1/tennis'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_user(user_id):
    return User.query.get(int(user_id))


#################################
######## MODELS #################
#################################
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(20), nullable=False)
    last = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(), nullable=False)
    dominant = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    scores = db.relationship('Score', backref='player')

class Score(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pro_compare = db.Column(db.String(), nullable=False)
    date = db.Column(db.Integer, nullable=False)



##############################################
######## VIEWS ########
##############################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/point')
def point():
    return render_template('point.html')


@app.route('/login', methods=["GET", "POST"])
def login(): 
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        all_users = list(User.query.filter_by(email=form.email.data).all())
        if user not in all_users:
            flash('email does not exist', 'danger')
            return redirect(url_for('login'))
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Log in success', 'success')
            return redirect(url_for('home'))
        else:
            flash('email or password is incorrect', 'danger')
            return redirect(url_for('login'))


    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash('You logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = newform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data,
                    first=form.first.data,
                    last=form.last.data,
                    dominant=form.dominant.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Register successful', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/home')
@login_required
def home(): 
    make_frame_dir(current_user.id)
    make_video_dir(current_user.id)
    
    # finding the most recent and getting data from the scores
    scores_query = Score.query.filter_by(player_id = current_user.id).all()
    all_data = []
    min_date = []
    average_score = []
    recent = 'none'
    score = 0
    name = 'none'
    second_most_recent = 'none'
    second_highest_score = 0
    difference = 'none'
    arranged_date = 'none'
    average = 'none'
    diff_symbol = 'none'
    for i in scores_query:
        adding = [i.score, i.date, i.pro_compare]
        date_data = i.date
        scores = i.score
        all_data.append(adding)
        min_date.append(date_data)
        average_score.append(scores)
    sort_date = min_date
    if len(sort_date) > 1:
        second_most_recent = sort_date[-2]

    for i in all_data:
        if i[1] == second_most_recent:
            second_highest_score = i[0]
    for i in all_data:
        if len(all_data) > 0:
            if i[1] == max(min_date):
                score = i[0]
                recent = i[1]
                name = i[2]
                
                arranged_date = datetime.utcfromtimestamp(recent).strftime('%Y-%m-%d %H:%M')
                average = int(round(sum(average_score) / len(average_score)))

    difference = score - second_highest_score
    
    if difference > 0:
        diff_symbol = '+'
    elif difference < 0:
        diff_symbol = '-'
    # converting date from unix to yy//mm//dd
    

    # finding the average score for a user
    
    return render_template('home.html', recent=arranged_date, name=name, score=score, average=average, difference=diff_symbol)

@app.route('/stroke', methods=["GET", "POST"])
@login_required
def stroke():
    if request.method == 'POST':
        video_upload = request.files["user_video"]
        filename = video_upload.filename
        path = f'/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/user_serves/{current_user.id}'
        session['File_name'] = filename
        session['Stroke'] = request.form['stroke']
        session['Professional'] = request.form['player']
        video_upload.save(os.path.join(path, filename))

        return redirect(url_for('results', filename=filename))
    return render_template('stroke.html')

@app.route('/results',  methods=["GET", "POST"])
@login_required
def results():

    if is_empty(current_user.id) != True:

        professional = session.get('Professional')
        stroke = session.get('Stroke')
    #######################################################################         
        # CREATING INSTANCE FOR PROFESSIONAL PLAYER
        playerright_leg = Player_data(f'pose/data/{stroke}_data/{professional}servelegs.csv', 'hip2ankle_right', f'{professional}')
        playerleft_leg = Player_data(f'pose/data/{stroke}_data/{professional}servelegs.csv', 'hip2ankle_left', f'{professional}')
        playerright_arm = Player_data(f'pose/data/{stroke}_data/{professional}servearm.csv', 'shoulder2wrist_right', f'{professional}')
        playerleft_arm = Player_data(f'pose/data/{stroke}_data/{professional}servearm.csv', 'shoulder2wrist_left', f'{professional}')
        playerright_body = Player_data(f'pose/data/{stroke}_data/{professional}servebody.csv', 'elbow2hip_right', f'{professional}')
        playerleft_body = Player_data(f'pose/data/{stroke}_data/{professional}servebody.csv', 'elbow2hip_left', f'{professional}')
        # getting data from that player
        dataright = playerright_leg.get_data()
        dataleft = playerleft_leg.get_data()
        dataright_arm = playerright_arm.get_data()
        dataleft_arm = playerleft_arm.get_data()
        dataright_body = playerright_body.get_data()
        dataleft_body = playerleft_body.get_data()

        # getting labels from that player
        label = playerright_leg.labels()
        label_arm = playerright_arm.labels()
        label_body = playerright_body.labels()
        # getting shot breakdown
        doughnut_data = playerright_leg.doughnut()
        # getting name of player
        player_name = playerright_leg.name

        #copying to create lists for vertical lines
        vertical_start_before = dataright.copy()
        vertical_load_before = dataright.copy()
        vertical_extend_before = dataright.copy()
        vertical_finish_before = dataright.copy()

        # vertical starting line
        vertical_start = [0 for i in vertical_start_before]
        for ind, value in enumerate(dataright):
            if ind == round(doughnut_data[0] / (100/len(dataright))):
                vertical_start[1:(ind-1)] = [200 for i in range(1,(ind-1))]
        
        # vertical loading line
        vertical_load = [0 for i in vertical_load_before]
        first = 0
        second = 0
        first_extend = 0
        second_extend = 0
        first_finish = 0
        for ind, value in enumerate(dataright):
            if ind == round(doughnut_data[0] / (100/len(dataright))):
                first = ind
            if ind == round((doughnut_data[0] /(100/len(dataright))) +  (doughnut_data[1] / (100/len(dataright)))):
                second = (ind - 1)
            vertical_load[first:second] = [200 for i in range(first,second)]

        # vertical extend line
        vertical_extend = [0 for i in vertical_extend_before]
        for ind, value in enumerate(dataright):
            if ind == round((doughnut_data[0] /(100/len(dataright))) +  (doughnut_data[1] / (100/len(dataright)))):
                first_extend = ind
            if ind == round((doughnut_data[0] /(100/len(dataright))) +  (doughnut_data[1] / (100/len(dataright))) + (doughnut_data[2] / (100/len(dataright)))):
                second_extend = (ind -1)
            vertical_extend[first_extend:second_extend] = [200 for i in range(first_extend,second_extend)]

        # vertical finish line
        vertical_finish = [0 for i in vertical_finish_before]
        for ind, value in enumerate(dataright):
            if ind == round((doughnut_data[0] /(100/len(dataright))) +  (doughnut_data[1] / (100/len(dataright))) + (doughnut_data[2] / (100/len(dataright)))):
                first_finish = ind
            vertical_finish[first_finish:-1] = [200 for i in range(first_finish,len(dataright))]
        # zero  line
        zero_line = [0 for i in range(len(dataright))]
                
    #######################################################################
        # uncommen the below to convert video
        converter(f'pose/user_serves/{current_user.id}/{session.get("File_name")}', 'Jacob', str(current_user.id))

        # CREATING INSTANCE FOR USER 
        user = User_data(f'pose/user_serves/{current_user.id}/{session.get("File_name")}', 'Jacob', str(current_user.id), str(current_user.id))
        # Getting user data for right and left
        User_data_r = list(user.get_data('hip2ankle_right'))
        User_data_l = list(user.get_data('hip2ankle_left'))
        User_data_r_arm = list(user.get_data('shoulder2wrist_right'))
        User_data_l_arm = list(user.get_data('shoulder2wrist_left'))
        User_data_r_body = list(user.get_data('elbow2hip_right'))
        User_data_l_body = list(user.get_data('elbow2hip_left'))

        # Getting user labels 
        User_label = user.labels()
        # Getting user's name
        User_name = user.name

        User_doughnut = user.doughnut()

        #copying to create lists for vertical lines for user
        vertical_start_before_user = User_data_r.copy()
        vertical_load_before_user = User_data_r.copy()
        vertical_extend_before_user = User_data_r.copy()
        vertical_finish_before_user = User_data_r.copy()

        # vertical starting line for user
        vertical_start_user = [0 for i in vertical_start_before_user]
        for ind, value in enumerate(User_data_r):
            if ind == round(User_doughnut[0] / (100/len(User_data_r))):
                vertical_start_user[1:(ind-1)] = [200 for i in range(1,(ind-1))]
        
        # vertical loading line
        vertical_load_user = [0 for i in vertical_load_before_user]
        first_user = 0
        second_user = 0
        first_extend_user = 0
        second_extend_user = 0
        first_finish_user = 0
        for ind, value in enumerate(User_data_r):
            if ind == round(User_doughnut[0] / (100/len(User_data_r))):
                first_user = ind
            if ind == round((User_doughnut[0] /(100/len(User_data_r))) +  (User_doughnut[1] / (100/len(User_data_r)))):
                second_user = (ind - 1)
            vertical_load_user[first_user:second_user] = [200 for i in range(first_user,second_user)]

        # vertical extend line
        vertical_extend_user = [0 for i in vertical_extend_before_user]
        for ind, value in enumerate(dataright):
            if ind == round((User_doughnut[0] /(100/len(User_data_r))) +  (User_doughnut[1] / (100/len(User_data_r)))):
                first_extend_user = ind
            if ind == round((User_doughnut[0] /(100/len(User_data_r))) +  (User_doughnut[1] / (100/len(User_data_r))) + (User_doughnut[2] / (100/len(User_data_r)))):
                second_extend_user = (ind -1)
            vertical_extend_user[first_extend_user:second_extend_user] = [200 for i in range(first_extend_user,second_extend_user)]

        # vertical finish line
        vertical_finish_user = [0 for i in vertical_finish_before_user]
        for ind, value in enumerate(User_data_r):
            if ind == round((User_doughnut[0] /(100/len(User_data_r))) +  (User_doughnut[1] / (100/len(User_data_r))) + (User_doughnut[2] / (100/len(User_data_r)))):
                first_finish_user = ind
            vertical_finish_user[first_finish_user:-1] = [200 for i in range(first_finish_user,len(User_data_r))]
        # zero  line
        zero_line_user = [0 for i in range(len(User_data_r))]
                
    #######################################################################
        # SHOWING RECOMMENDATIONS
        if current_user.dominant == 'right' and (player_name == 'djok' or player_name == 'federer' or player_name == 'serena'):
            leg_tips = leg_score(user, playerright_arm, playerleft_arm)
            arm_tips = arm_tip_summary(user, playerright_arm, playerleft_arm)
            body_tips = body_score(user, playerright_body, playerleft_body)
            score = total_score(user, playerright_leg, playerleft_leg, playerright_arm, playerleft_arm, playerright_body, playerleft_body)

        if current_user.dominant == 'left' and (player_name == 'djok' or player_name == 'federer' or player_name == 'serena'):
            leg_tips = leg_score_left_handers(user, playerright_arm, playerleft_arm)
            arm_tips = arm_tip_summary_left_handers(user, playerright_arm, playerleft_arm)
            body_tips = body_score_left_handers(user, playerright_body, playerleft_body)
            score = total_score_left_handers(user, playerright_leg, playerleft_leg, playerright_arm, playerleft_arm, playerright_body, playerleft_body)
    ########################################################################
        #Delete frames from folder
        delete_frames(str(current_user.id))
        delete_user_video(str(current_user.id))

        # getting current unix timestamp
        current_time = time.time()

        # assigning pro name
        name = None
        if player_name == 'djok':
            name = 'Djokovic'
        elif player_name == 'rog':
            name = 'Federer'
        elif player_name == 'nadal':
            name = 'Nadal'
        elif player_name == 'serena':
            name = "Serena"
        # adding the score to the database
        insert_score = Score(score = score,
                            player_id= current_user.id,
                            pro_compare = name,
                            date = current_time)
        db.session.add(insert_score)
        db.session.commit()
    else:
        return redirect(url_for('home'))

    return render_template('graphs.html', data=dataright, datatwo=dataleft, label=label, data_r_arm=dataright_arm,data_l_arm=dataleft_arm,label_arm=label_arm,
    dataright_body=dataright_body, dataleft_body=dataleft_body, label_body=label_body, doughnut_data=doughnut_data, name=name,
    user_right=User_data_r, user_left=User_data_l, user_left_arm=User_data_l_arm, user_right_arm=User_data_r_arm,
    User_data_r_body=User_data_r_body, User_data_l_body=User_data_l_body, user_label = User_label, user_name =User_name, user_doughnut = User_doughnut, 
    arm_tips=arm_tips, leg_tips=leg_tips,body_tips=body_tips, score=score, vertical_start=vertical_start, vertical_load=vertical_load, vertical_extend=vertical_extend
    ,vertical_finish=vertical_finish, zero_line=zero_line, vertical_start_user=vertical_start_user, vertical_load_user=vertical_load_user, vertical_extend_user=vertical_extend_user,
     vertical_finish_user=vertical_finish_user, zero_line_user=zero_line_user)

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    all_score_data = []
    scores_query = Score.query.filter_by(player_id = current_user.id).all()
    for i in scores_query:
        arranged_date = datetime.utcfromtimestamp(i.date).strftime('%Y-%m-%d')
        all_score_data.append([i.score, arranged_date, i.pro_compare])
    return render_template('history.html',all_score_data=all_score_data )

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    return render_template('gallery.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    dominant_hand = current_user.dominant
    delete_string = None
    delete_w_email = current_user.email
    if request.method == 'POST':
        account_info = User.query.get(current_user.id)
        if 'first' in request.form:
            first = request.form['first']
            first_clean = first.replace(' ', '')
            if len(first_clean) > 0:
                account_info.first = first_clean
                db.session.commit()
        if 'last' in request.form:
            last = request.form['last']
            last_clean = last.replace(' ', '')
            if len(last_clean) > 0:
                account_info.last = last_clean
                db.session.commit()
        if 'email' in request.form:
            email = request.form['email']
            email_clean = email.replace(' ', '')
            if len(email_clean) > 0:
                account_info.email = email_clean
                db.session.commit()
        if 'dominant' in request.form:
            dominant = request.form['dominant']
            dominant_clean = dominant.replace(' ', '')
            if len(dominant_clean) > 0:
                account_info.dominant = dominant_clean
                db.session.commit()
        if 'first' in request.form and 'last' in request.form and 'email' in request.form and 'dominant' in request.form:
            first = request.form['first']
            first_clean = first.replace(' ', '')
            last = request.form['last']
            last_clean = last.replace(' ', '')
            email = request.form['email']
            email_clean = email.replace(' ', '')
            dominant = request.form['dominant']
            dominant_clean = dominant.replace(' ', '')
            if len(first_clean) > 0 or len(last_clean) > 0 or len(email_clean) > 0 or len(dominant_clean) > 0:
                flash('Changed details successfully', 'success')
   
        if 'text' in request.form:
            delete_string = request.form['text']
            if delete_string == delete_w_email:
                Score.query.filter_by(player_id = current_user.id).delete()
                User.query.filter_by(id=current_user.id).delete()
                db.session.commit()
                logout_user()
                flash('You have successfully deleted your account', 'success')
                return redirect(url_for('login'))
            else:
                flash('Text did not match', 'danger')


        

    return render_template('account.html', dominant_hand=dominant_hand, delete_w_email=delete_w_email)

@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    