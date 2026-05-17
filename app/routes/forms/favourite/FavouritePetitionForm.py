from flask_wtf import FlaskForm
from wtforms import SubmitField

class FavouritePetitionForm(FlaskForm):
    submit = SubmitField('Favourite Petition')