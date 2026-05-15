from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import db, FavouriteMP
import concurrent.futures
import requests

http_session = requests.Session()

favourites_bp = Blueprint("favourites", __name__)

@login_required
@favourites_bp.route('/petitions')
def petitions():
    return render_template('favourites/petitions.html')

@favourites_bp.route('/members')
@login_required
def members():
    # gets id of every favourite member for current user
    favourite_records = db.session.execute(
        db.select(FavouriteMP).filter_by(user_id=current_user.id)
    ).scalars().all()
    
    favourite_ids = [mp.member_id for mp in favourite_records]

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
        results = executor.map(fetch_member_data, favourite_ids)
        favourite_members_list = [r for r in results if r]

    numberOfFavourites = len(favourite_members_list)

    return render_template('favourites/members.html', members=favourite_members_list, numberOfFavourites=numberOfFavourites)