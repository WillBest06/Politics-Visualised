from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Regexp

class MemberSearchForm(FlaskForm):
    t = RadioField(
    'Choose a search type', 
    choices=[('name','MP name'),('location','Location/Post code')], 
    default='name',
    validators=[DataRequired()]
)

    q = StringField('', validators=[DataRequired() ,Regexp(r"^[a-zA-Z0-9\s.'!-]*$",
        message="Search must only contain letters, numbers, spaces, or valid punctuation e.g. (.'-!)")], )
    submit = SubmitField('Search')