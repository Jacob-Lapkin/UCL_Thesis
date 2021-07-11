
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
#from myproject.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextField, SubmitField, PasswordField,
                     SubmitField, BooleanField, DateField, RadioField, FileField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo 
from wtforms import ValidationError

from datetime import datetime

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
    date = DateField('Date', format='%Y-%m-%d', default=datetime.now())
    title = StringField('Upload title', validators=[DataRequired()])
    description = TextField("Description", validators=[DataRequired()])
    point_type = RadioField('Point Type', validators=[DataRequired()], choices=[('choice1', 'practice'), ('choice2', 'match')])
    point_upload = FileField('Upload', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Stroke(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    title = StringField('Upload title', validators=[DataRequired()])
    stroke_type = SelectField('Stroke Type', validators=[DataRequired()], choices = [('choice1', 'Serve'), ('choice2', 'Forehand return'), ('choice3', 'backhand return'), ('choice4', 'Volley')])
    pro_comparison = SelectField('Professional Comparison', choices = [('choice1', 'Novak Djokavic'), ('choice2', 'Roger Federer'), ('choice3', 'Rafael Nadal'), ('choice4', 'Serena Williams')], validators = [DataRequired()])
    stroke_upload = FileField('Upload', validators=[DataRequired()])
    submit = SubmitField('Submit')