
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
    stroke_type = SelectField('Stroke Type', validators=[DataRequired()], choices = [('serve', 'Serve'), ('choice2', 'Forehand return'), ('choice3', 'backhand return'), ('choice4', 'Volley')])
    pro_comparison = SelectField('Professional Comparison', choices = [('djok', 'Novak Djokavic'), ('choice2', 'Roger Federer'), ('choice3', 'Rafael Nadal'), ('choice4', 'Serena Williams')], validators = [DataRequired()])
    stroke_upload = FileField('Upload', validators=[DataRequired()])
    submit = SubmitField('Submit')