from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, SubmitField, \
    StringField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    min_age = IntegerField('From-years')
    max_age = IntegerField('To-years')
    min_rating = IntegerField('From-rating')
    max_rating = IntegerField('To-rating')
    city = StringField('City')
    region = StringField('Region')
    country = StringField('Country')
    sex_pref = SelectField('Sexual Preference', choices=[
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
    submit = SubmitField('Submit', [DataRequired()])
