from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, \
    SelectMultipleField, IntegerField, TextAreaField, DateField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, Optional


class SettingsPasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField('New password', [InputRequired(), Length(min=7),
                                                EqualTo('rep_password', message='Passwords do not match')])
    rep_password = PasswordField('Repeat new password', [InputRequired()])
    submit = SubmitField('Submit', [InputRequired()])


class SettingsEmailForm(FlaskForm):
    new_email = StringField('New email', [InputRequired()])
    submit = SubmitField('Submit', [InputRequired()])


class SettingGeneralForm(FlaskForm):
    first_name = StringField('First Name', [Length(max=40)])
    last_name = StringField('Last Name', [Length(max=45)])
    gender = SelectField('gender', choices=[
        ('', 'Not change'),
        ('Male', 'Male'),
        ('Female', 'Female')
    ])
    sex_pref = SelectField('Sexual Preference',
                           choices=[
                               ('', 'Not change'),
                               ('Bisexual', 'Bisexual'),
                               ('Male', 'Male'),
                               ('Female', 'Female')
    ])
    tags = SelectMultipleField('Tags', choices=[
        ('Hunting', 'Hunting'),
        ('Fishing', 'Fishing'),
        ('Singing', 'Singing'),
        ('Fuck porcupine', 'Fuck porcupine'),
        ('Watching "Разведопрос"', 'Watching "Разведопрос"')
    ])
    age = DateField('Age (in YYYY-MM-DD)', format='%Y-%m-%d',
                    validators=[Optional()])
    biography = TextAreaField('Enter you biography', [Length(max=1000)])
    submit = SubmitField('Submit')
