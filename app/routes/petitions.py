from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required

petitions_bp = Blueprint("petitions", __name__)

@petitions_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    from ..services.json_parser import main_parser
    from .forms.petition_upload import JsonUploadForm
    form = JsonUploadForm()

    if form.validate_on_submit():
        file = form.json_file.data

        raw_json = file.read().decode("utf-8")

        parsedData = main_parser(raw_json)
        session['petition_data'] = parsedData # stores the JSON data in a session so that it can be accessed by visualise route
        petition_id = parsedData['metadata']['id']

        return redirect(url_for('petitions.visualise', petition_id=petition_id))

    return render_template('petitions/base.html', option="upload", form=form)

@petitions_bp.route('/visualise')
def visualise():
    data = session.get('petition_data')
    
    if not data:
        return redirect(url_for('petitions.upload'))
        
    return render_template('petitions/base.html', option="visualise", data=data)

# @petitions_bp.route('/save')
# @login_required
# def save():
#     pass