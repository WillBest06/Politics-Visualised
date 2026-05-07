from flask import Blueprint, render_template, redirect, url_for, session, request
import requests

members_bp = Blueprint("members", __name__)

@members_bp.route('/')
def options():
    return render_template('members.html')

@members_bp.route('/search', methods=['GET'])
def search():
    from .forms.member_search import MemberSearchForm
    form = MemberSearchForm(request.args)
    
    search_type = request.args.get('t') 
    query = request.args.get('q')

    if query:
        query = query.strip()
        api_url = f'https://members-api.parliament.uk/api/Members/Search?{search_type}={query}&skip=0&take=20'
        r = requests.get(api_url)
        
        if r.status_code == 200:
            data = r.json()
            members_data = data.get('items', [])
            total_results = data.get('totalResults', 0)
            result_context = data.get('resultContext', 0)
            
            return render_template('members/results.html', 
                                   form=form, 
                                   members=members_data, 
                                   totalResults=total_results,
                                   resultContext=result_context
                                   )

    return render_template('members/search.html', form=form)