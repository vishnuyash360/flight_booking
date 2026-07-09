from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class FlightSearchForm(FlaskForm):
    # These will be populated dynamically in the route
    departure = StringField('From', validators=[DataRequired()])
    destination = StringField('To', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=datetime.now)
    submit = SubmitField('Search Flights')
