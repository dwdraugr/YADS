from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class SettingsPasswordForm(FlaskForm):
    old_password = StringField('Old password')
    new_password = StringField('New password', [InputRequired(), Length(min=7),
                                                EqualTo('rep_password', message='Passwords do not match')])
    rep_password = StringField('Repeat new password', [InputRequired()])
    submit = SubmitField('Submit', [InputRequired()])


class SettingsEmailForm(FlaskForm):
    email = StringField('New email', [InputRequired()])
    submit = SubmitField('Submit', [InputRequired()])
