from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

"""
def is_year(form, field):
    if len(int(field.data)) != 4:
        raise ValidationError('Year must be 4 digits.')
"""

class MovieForm(FlaskForm):
	movie_name = StringField('movie_name',
		validators=[DataRequired()])
	movie_year = StringField('movie_year',
		validators=[DataRequired()])
	submit = SubmitField("Submit")

class MovieForm2(FlaskForm):
	movie_name = StringField('Movie Name',
		validators=[DataRequired()])
	submit = SubmitField("Submit")