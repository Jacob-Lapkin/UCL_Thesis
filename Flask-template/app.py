
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, 
                    RadioField, SelectField, TextField, TextAreaField)
from wtforms.validators import DataRequired

app = Flask(__name__)

#############a##############
#####form configuration#####
############################
app.config['SECTRET_KEY'] = 'mykey'



##############################################
########### datbase configuration #############
##############################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

Migrate(app, db)



##############################################
######## Routes, render template, etc ########
##############################################
@app.route('/regwfask', methods=['GET', 'POST'])
def regwflask(): 
    form = SimpleForm()
    if form.validate_on_submit():
        return redirect(url_for('/'))

    return render_template('regwflask.html', form=form)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/point')
def point():
    return render_template('point.html')


@app.route('/register', methods=['GET', 'POST'])
def register(): 
    return render_template('register.html')

@app.route('/register/success')
def success():
    first = request.args.get('first')
    last = request.args.get('last')
    email = request.args.get('email')
    
    return render_template('after_register.html')


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
    