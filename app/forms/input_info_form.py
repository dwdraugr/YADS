from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    IntegerField, TextAreaField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length


class InputInfoForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(), Length(max=40)])
    last_name = StringField('Last Name', [DataRequired(), Length(max=45)])
    gender = SelectField('gender', choices=[
        ('Male', 'Male'),
        ('Female', 'Female')
    ])
    sex_pref = SelectField('Sexual Preference',
                           choices=[
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
    age = DateField('Age (in YYYY-MM-DD)', validators=[DataRequired()],
                    format='%Y-%m-%d')
    biography = TextAreaField('Enter you biography', [DataRequired(),
                                                      Length(max=1000)])
    submit = SubmitField('Submit', [DataRequired()])
