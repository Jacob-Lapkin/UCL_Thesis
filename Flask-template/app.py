
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
#from myproject.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextField, SubmitField, PasswordField,
                     SubmitField, BooleanField, DateField, RadioField, FileField)
from wtforms.validators import DataRequired, Length, Email, EqualTo 
from wtforms import ValidationError


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

###########################
######### FORMS #############
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
    
class point(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    title = StringField('Upload title', validators=[DataRequired()])
    description = TextField("Description", validators=[DataRequired()])
    point_type = RadioField('Point Type', validators=[DataRequired()], choices=[('choice1', 'practice'), ('choice2', 'match')])
    point_upload = FileField('Upload', validators=[DataRequired()])

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    