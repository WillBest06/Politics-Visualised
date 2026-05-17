from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import db, FavouriteMP, SavedPetition
import concurrent.futures
import requests

http_session = requests.Session()

favourites_bp = Blueprint("favourites", __name__)

@login_required
@favourites_bp.route('/petitions')
def petitions():
    from app.models import db, SavedPetition
    # list of all saved petition objects
    saved_list = db.session.execute(
        db.select(SavedPetition).filter_by(user_id=current_user.id)
    ).scalars().all()

    from ..routes.forms.favourite.FavouritePetitionForm import FavouritePetitionForm 
    form = FavouritePetitionForm()

    return render_template('favourites/petitions.html', petitions=saved_list, form=form)

@favourites_bp.route('/members')
@login_required
def members():
    # gets id of every favourite member for current user
    favourite_member_records = db.session.execute(
        db.select(FavouriteMP).filter_by(user_id=current_user.id)
    ).scalars().all()
    
    favourite_member_ids = [mp.member_id for mp in favourite_member_records]

    # sends call to Members API
    def fetch_member_data(member_id):
        url = f'https://members-api.parliament.uk/api/Members/{member_id}'
        try:
            return http_session.get(url, timeout=5).json()
        except:
            return None

    # parrallel fetching of Member data
    favourite_members_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_member_data, favourite_member_ids)
        
        for r in results:
            if r:
                member_data = r.get('value', r) 
                
                if 'latestParty' not in member_data:
                    member_data['latestParty'] = member_data.get('latestHouseMembership', {}).get('latestParty', {'name': 'N/A'})

                favourite_members_list.append({"value": member_data})

    numberOfFavourites = len(favourite_members_list)

    return render_template('favourites/members.html', members=favourite_members_list, numberOfFavourites=numberOfFavourites)