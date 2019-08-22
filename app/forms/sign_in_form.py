from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class SignInForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=30)])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Submit', [DataRequired()])
