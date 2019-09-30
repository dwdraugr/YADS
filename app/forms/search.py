from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, SubmitField, \
    StringField
from wtforms.validators import DataRequired, Optional, NumberRange


class Search(FlaskForm):
    min_age = IntegerField('From-years', validators=[Optional(), NumberRange(0, 1000, 'Too big or too small number')])
    max_age = IntegerField('To-years', validators=[Optional(), NumberRange(0, 1000, 'Too big or too small number')])
    sort_age = SelectField('Sort by...', choices=[
        ('False', 'Ascending age'),
        ('True', 'Descending age')
    ])
    min_rating = IntegerField('From-rating', validators=[Optional()])
    max_rating = IntegerField('To-rating', validators=[Optional()])
    sort_rating = SelectField('Sort by...', choices=[
        ('True', 'Descending rating'),
        ('False', 'Ascending rating')
    ])
    city = StringField('City', validators=[Optional()])
    region = StringField('Region', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    sex_pref = SelectField('Sexual Preference', choices=[
        ('Bisexual', 'Bisexual'),
        ('Male', 'Male'),
        ('Female', 'Female')
    ], validators=[Optional()])
    tags = SelectMultipleField('Tags', choices=[
        ('Hunting', 'Hunting'),
        ('Fishing', 'Fishing'),
        ('Singing', 'Singing'),
        ('Fuck porcupine', 'Fuck porcupine'),
        ('Watching "Разведопрос"', 'Watching "Разведопрос"')
    ], validators=[Optional()])
    submit = SubmitField('Submit', [DataRequired()])
