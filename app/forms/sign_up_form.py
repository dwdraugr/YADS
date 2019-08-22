from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Email


class SignUpForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(max=30)])
    email = StringField('Email', [InputRequired(),
                                  Email(message='Email is bad')])
    password = PasswordField('Password', [InputRequired(), Length(min=7),
                                          EqualTo('confirm',
                                                  message='Password must be '
                                                          'equal')])
    confirm = PasswordField('Confirm Password',
                            [InputRequired()])
    accept_rules = BooleanField('I agree that my ass goes into slavery to '
                                'the owner of the site',
                                [InputRequired()])
    submit = SubmitField('Submit', [InputRequired()])
