from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class InputInfoForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(), Length(max=40)])
    last_name = StringField('Last Name', [DataRequired(), Length(max=45)])
    gender = SelectField('gender', choices=[
        ('ub', 'Undefined'),
        ('male', 'Male'),
        ('fem', 'Female'),
        ('chopper', 'Attack Chopper')
    ])
    sex_pref = SelectField('Sexual Preference',
                           choices=[
                               ('bi', 'Bisexual'),
                               ('getero', 'Geterosexual'),
                               ('gomo', 'Gomosexual'),
                               ('heli', 'Helisexual')
    ])
    age = IntegerField('Age', [DataRequired()])
    biography = TextAreaField('Enter you biography', [DataRequired(),
                                                      Length(max=1000)])
    submit = SubmitField('Submit', [DataRequired()])
