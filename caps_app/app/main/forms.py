from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, DateField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class NameForm(FlaskForm): 
   name = StringField('What is your name?', validators=[DataRequired()]) 
   submit = SubmitField('Submit')