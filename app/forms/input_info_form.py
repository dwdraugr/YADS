from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    IntegerField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class InputInfoForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(), Length(max=40)])
    last_name = StringField('Last Name', [DataRequired(), Length(max=45)])
    gender = SelectField('gender', choices=[
        ('Undefined', 'Undefined'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Attack Chopper', 'Attack Chopper')
    ])
    sex_pref = SelectField('Sexual Preference',
                           choices=[
                               ('Bisexual', 'Bisexual'),
                               ('Geterosexual', 'Geterosexual'),
                               ('Gomosexual', 'Gomosexual'),
                               ('Helisexual', 'Helisexual')
    ])
    tags = SelectMultipleField('Tags', choices=[
        ('Hunting', 'Hunting'),
        ('Fishing', 'Fishing'),
        ('Singing', 'Singing'),
        ('Fuck porcupine', 'Fuck porcupine'),
        ('Watching "Разведопрос"', 'Watching "Разведопрос"')
    ])
    age = IntegerField('Age', [DataRequired()])
    biography = TextAreaField('Enter you biography', [DataRequired(),
                                                      Length(max=1000)])
    submit = SubmitField('Submit', [DataRequired()])
