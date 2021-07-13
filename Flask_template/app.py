
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
#from myproject.models import User
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


from datetime import datetime

from forms import Login, newform, point, Stroke

# importing data FIX THIS PATH
import sys
sys.path.append('/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose')
from canvas_data import Player_data, User_data

from converting import converter


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
    playerright = Player_data(f'pose/data/{stroke}_data/{professional}serve45.csv', 'hip2ankle_right', f'{professional}')
    playerleft = Player_data(f'pose/data/{stroke}_data/{professional}serve45.csv', 'hip2ankle_left', f'{professional}')
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
    # converter('pose/videos/serve/jake.mov', 'Jacob')

    # CREATING INSTANCE FOR USER 
    user = User_data('pose/videos/serve/jake.mov', 'Jacob')
    # Getting user data for right and left
    User_data_r = list(user.get_data('hip2ankle_right'))
    User_data_l = list(user.get_data('hip2ankle_left'))
    # Getting user labels 
    User_label = user.labels()
    # Getting user's name
    User_name = user.name

    User_doughnut = User_data.doughnut('Jacob', 'User_test', 'User_test')
#######################################################################


    return render_template('graphs.html', data=dataright, datatwo=dataleft, label=label, doughnut_data=doughnut_data, name=player_name,
    user_right=User_data_r, user_left=User_data_l, user_label = User_label, user_name =User_name, user_doughnut = User_doughnut, body=body)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    