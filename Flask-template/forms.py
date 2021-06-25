from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class newform(FlaskForm):
    first = StringField(("First Name"))
    last = StringField(("Last Name"))
    email = StringField(("Email Address"))
    password = PasswordField(("Password"))
    passconfirm = PasswordField('Confirm Password')


    

