from flask import Blueprint, render_template, redirect, url_for, session, request
import requests
import math
import time
import concurrent.futures
import requests_cache

# caches get requests for 24hrs
requests_cache.install_cache('parliament_api_cache', expire_after=86400)

http_session = requests.Session()

members_bp = Blueprint("members", __name__)

@members_bp.route('/search', methods=['GET'])
def search():
    from .forms.member_search import MemberSearchForm
    form = MemberSearchForm(request.args)
    
    search_type = request.args.get('t') 
    query = request.args.get('q')
    
    page = request.args.get('page', 1, type=int)

    if query:
        query = query.strip()
        take = 10  
        skip = (page - 1) * take 
        
        api_url = f'https://members-api.parliament.uk/api/Members/Search?{search_type}={query}&skip={skip}&take={take}'
        r = http_session.get(api_url)
        
        if r.status_code == 200:
            data = r.json()
            members_data = data.get('items', [])
            total_results = data.get('totalResults', 0)
            
            total_pages = math.ceil(total_results / take)
            
            return render_template('members/results.html', 
                                   form=form, 
                                   members=members_data, 
                                   totalResults=total_results,
                                   current_page=page,
                                   total_pages=total_pages)

    return render_template('members/search.html', form=form)

@members_bp.route('/profile/<int:member_id>', methods=['GET'])
def profile(member_id):
    api_url = f'https://members-api.parliament.uk/api/Members/{member_id}'

    def fetch_json(url):
        try:
            return http_session.get(url, timeout=5).json()
        except requests.exceptions.RequestException as e:
            print(f"Could not fetch {url}: {e}")
            return {}

    # start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_member = executor.submit(fetch_json, api_url)
        future_synopsis = executor.submit(fetch_json, api_url + "/Synopsis")
        future_portrait = executor.submit(fetch_json, api_url + "/PortraitUrl")
        future_contact = executor.submit(fetch_json, api_url + "/Contact")
        future_bio = executor.submit(fetch_json, api_url + "/Biography")

        member_data = future_member.result()
        synopsis = future_synopsis.result()
        portrait = future_portrait.result()
        contact_info = future_contact.result()
        biography = future_bio.result()

        # end_time = time.time()
        # print(f"Fetched all JSON in {end_time - start_time:.2f} seconds")
    
    return render_template('members/profile.html', member=member_data, contactInfo=contact_info, biography=biography, portrait=portrait, synopsis=synopsis)