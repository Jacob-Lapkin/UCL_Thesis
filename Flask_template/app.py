
import time
from datetime import datetime
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
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

from datetime import datetime

from forms import point, Stroke

# importing data FIX THIS PATH
import sys
sys.path.append('/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose')
from canvas_data import (Player_data, User_data, legs_tips_start, legs_tips_load, legs_tips_extend, legs_tips_finish,
                            arm_tip_summary, leg_score, body_score, total_score)
from converting import converter, make_dir, delete_frames

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
    email = StringField("Email Address", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    passconfirm = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        exisitng_user_email = User.query.filter_by(email=email.data).first()
        if exisitng_user_email:
            raise ValidationError('Email already registered')

#####################
###### CONFIRG ######
#####################

app = Flask(__name__)
db = SQLAlchemy((app))

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mykey'

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
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Log in success')
            return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash('You logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = newform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data,
                    first=form.first.data,
                    last=form.last.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/home')
@login_required
def home(): 
    make_dir(current_user.id)  
    
    # finding the most recent and getting data from the scores
    scores_query = Score.query.filter_by(player_id = current_user.id).all()
    all_data = []
    min_date = []
    average_score = []
    recent = None
    score = None
    name = None
    for i in scores_query:
        adding = [i.score, i.date, i.pro_compare]
        date_data = i.date
        scores = i.score
        all_data.append(adding)
        min_date.append(date_data)
        average_score.append(scores)
    for i in all_data:
        if i[1] == max(min_date):
            score = i[0]
            recent = i[1]
            name = i[2]

    # converting date from unix to yy//mm//dd
    arranged_date = datetime.utcfromtimestamp(recent).strftime('%Y-%m-%d %H:%M')

    # finding the average score for a user
    average = int(round(sum(average_score) / len(average_score)))
    return render_template('home.html', recent=arranged_date, name=name, score=score, average=average)

@app.route('/stroke', methods=["GET", "POST"])
@login_required
def stroke():
    if request.method == 'POST':
        session['Stroke'] = request.form['stroke']
        session['Professional'] = request.form['player']
        return redirect(url_for('results'))
    return render_template('stroke.html')

@app.route('/results',  methods=["GET", "POST"])
@login_required
def results():

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
    # getting the body part that is analyzed
#######################################################################
    # uncommen the below to convert video
    converter('pose/videos/serve/jacob.mp4', 'Jacob', str(current_user.id))

    # CREATING INSTANCE FOR USER 
    user = User_data('pose/videos/serve/jacob.mp4', 'Jacob', str(current_user.id), str(current_user.id))
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
#######################################################################
    # SHOWING RECOMMENDATIONS
    leg_tips = leg_score(user, playerright_arm, playerleft_arm)
    arm_tips = arm_tip_summary(user, playerright_arm, playerleft_arm)
    body_tips = body_score(user, playerright_body, playerleft_body)
    score = total_score(user, playerright_leg, playerleft_leg, playerright_arm, playerleft_arm, playerright_body, playerleft_body)

########################################################################
    #Delete frames from folder
    delete_frames(str(current_user.id))

    # getting current unix timestamp
    current_time = time.time()

    # assigning pro name
    name = None
    if player_name == 'djok':
        name = 'Djokovic'
    # adding the score to the database
    insert_score = Score(score = score,
                         player_id= current_user.id,
                         pro_compare = name,
                         date = current_time)
    db.session.add(insert_score)
    db.session.commit()
    
    return render_template('graphs.html', data=dataright, datatwo=dataleft, label=label, data_r_arm=dataright_arm,data_l_arm=dataleft_arm,label_arm=label_arm,
    dataright_body=dataright_body, dataleft_body=dataleft_body, label_body=label_body, doughnut_data=doughnut_data, name=player_name,
    user_right=User_data_r, user_left=User_data_l, user_left_arm=User_data_l_arm, user_right_arm=User_data_r_arm,
    User_data_r_body=User_data_r_body, User_data_l_body=User_data_l_body, user_label = User_label, user_name =User_name, user_doughnut = User_doughnut, 
    arm_tips=arm_tips, leg_tips=leg_tips,body_tips=body_tips, score=score)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    