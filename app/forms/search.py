from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    min_age = IntegerField('From-years')
    max_age = IntegerField('To-years')
    tags = SelectMultipleField('Tags', choices=[
        ('Hunting', 'Hunting'),
        ('Fishing', 'Fishing'),
        ('Singing', 'Singing'),
        ('Fuck porcupine', 'Fuck porcupine'),
        ('Watching "Разведопрос"', 'Watching "Разведопрос"')
    ])
    submit = SubmitField('Submit', [DataRequired()])
