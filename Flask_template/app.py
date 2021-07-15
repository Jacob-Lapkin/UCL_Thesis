
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
#from myproject.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextField, SubmitField, PasswordField,
                     SubmitField, BooleanField, DateField, RadioField, FileField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo 
from wtforms import ValidationError

from datetime import datetime

from forms import point, Stroke

# importing data FIX THIS PATH
import sys
sys.path.append('/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose')
from canvas_data import Player_data, User_data
from converting import converter, make_dir

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
    return render_template('home.html')

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
    playerright = Player_data(f'pose/data/{stroke}_data/{professional}servelegs.csv', 'hip2ankle_right', f'{professional}')
    playerleft = Player_data(f'pose/data/{stroke}_data/{professional}servelegs.csv', 'hip2ankle_left', f'{professional}')
    # getting data from that player
    dataright = playerright.get_data()
    dataleft = playerleft.get_data()
    # getting labels from that player
    label = playerright.labels()
    # getting shot breakdown
    doughnut_data = playerright.doughnut()
    # getting name of player
    player_name = playerright.name
    # getting the body part that is analyzed
    if playerright.angle == 'hip2ankle_right':
        body = 'legs'
#######################################################################
    # uncommen the below to convert video
    #converter('pose/videos/serve/jake.mov', 'Jacob', str(current_user.id))

    # CREATING INSTANCE FOR USER 
    user = User_data('pose/videos/serve/jake.mov', 'Jacob')
    # Getting user data for right and left
    User_data_r = list(user.get_data('hip2ankle_right'))
    User_data_l = list(user.get_data('hip2ankle_left'))
    User_data_r_arm = list(user.get_data('shoulder2wrist_right'))
    User_data_l_arm = list(user.get_data('shoulder2wrist_left'))


    # Getting user labels 
    User_label = user.labels()
    # Getting user's name
    User_name = user.name

    User_doughnut = User_data.doughnut('Jacob', str(current_user.id), str(current_user.id))
#######################################################################


    return render_template('graphs.html', data=dataright, datatwo=dataleft, label=label, doughnut_data=doughnut_data, name=player_name,
    user_right=User_data_r, user_left=User_data_l, user_left_arm=User_data_l_arm, user_right_arm=User_data_r_arm,
    user_label = User_label, user_name =User_name, user_doughnut = User_doughnut, body=body)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    