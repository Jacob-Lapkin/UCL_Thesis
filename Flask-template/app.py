
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask import app, db, bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, 
                    RadioField, SelectField, TextField, TextAreaField, PasswordField)
from wtforms.validators import DataRequired, Email, Length
from forms import newform


app = Flask(__name__)



#############a##############
#####form configuration#####
############################
app.config['SECRET_KEY'] = 'mykey'



##############################################
########### datbase configuration #############
##############################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)




##############################################
######## Routes, render template, etc ########
##############################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/point')
def point():
    return render_template('point.html')

@app.route('/login', methods=["GET", "POST"])
def login(): 
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = newform()
    return render_template('register.html', form=form)



@app.route('/home')
def home():
    # counting strokes 
    name = "Jacob"
    strokes = ["b", "f", "b", "s", "v", "v", "b", "f", "s", "b"]
    backhand = strokes.count("b")

    return render_template('home.html', name=name ,strokes=strokes, backhand=backhand)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    