from flask import Blueprint, render_template, redirect, url_for, session, request
import requests
import math

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
        r = requests.get(api_url)
        
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