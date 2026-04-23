from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class JsonUploadForm(FlaskForm):
    json_file = FileField('Upload Petition JSON file', validators=[
        FileRequired(),
        FileAllowed(['json'], 'JSON files only!')
    ])
    submit = SubmitField('Upload')