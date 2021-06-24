from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class register(FlaskForm):
    first = StringField("First Name: ")
    last = StringField("Last Name: ")