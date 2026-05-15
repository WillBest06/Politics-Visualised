from flask_wtf import FlaskForm
from wtforms import SubmitField

class FavouriteMPForm(FlaskForm):
    submit = SubmitField('Favourite')