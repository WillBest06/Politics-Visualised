from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_required
from app.models import db, SavedPetition
import json

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

    from .forms.favourite.FavouritePetitionForm import FavouritePetitionForm
    form = FavouritePetitionForm()

    petition_id = data['metadata']['id']

    is_saved = False 
    if current_user.is_authenticated:
        is_saved = db.session.execute(
            db.select(SavedPetition).filter_by(user_id=current_user.id, petition_id=petition_id)
        ).scalar() is not None
        
    return render_template('petitions/base.html', 
                           option="visualise", 
                           data=data, 
                           form=form, 
                           is_saved=is_saved)

@petitions_bp.route('/visualise/<int:petition_id>')
@login_required
def visualise_saved(petition_id):
    from app.models import db, SavedPetition
    import json

    petition = db.session.execute(
        db.select(SavedPetition).filter_by(user_id=current_user.id, petition_id=petition_id)
    ).scalar()
    
    if not petition:
        flash("Petition not found in your saved list.", "danger")
        return redirect(url_for('favourites.petitions'))
    
    data = json.loads(petition.details)

    from .forms.favourite.FavouritePetitionForm import FavouritePetitionForm
    form = FavouritePetitionForm()

    # always true as route can only be accessed via saved petitions
    is_saved = True
    return render_template('petitions/base.html', 
                           option="visualise", 
                           data=data, 
                           form=form, 
                           is_saved=is_saved)

@petitions_bp.route('/save', methods=['POST'])
@login_required
def save():
    from .forms.favourite.FavouritePetitionForm import FavouritePetitionForm 

    form = FavouritePetitionForm()
    data = session.get('petition_data')
    
    if not data:
        flash("No data found to save.", "danger")
        return redirect(url_for('petitions.upload'))

    if form.validate_on_submit():
        petition_number = data['metadata']['id'] # eg 700750


        already_saved = db.session.execute(
            db.select(SavedPetition).filter_by(user_id=current_user.id, petition_id=petition_number)
        ).scalar()

        if already_saved:
            db.session.delete(already_saved)
            db.session.commit()
            flash('Removed from saved list.', "info")
        else:
            new_saved = SavedPetition(
                petition_id=petition_number, 
                title=data['metadata']['title'],
                details=json.dumps(data), 
                user_id=current_user.id
            )
            db.session.add(new_saved)
            db.session.commit()
            flash('Petition saved!', "success")

    return redirect(request.referrer or url_for('petitions.visualise'))