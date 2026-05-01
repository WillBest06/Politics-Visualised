from flask import Blueprint, render_template, redirect, url_for, session, request
import requests

members_bp = Blueprint("members", __name__)

@members_bp.route('/')
def options():

    return render_template('members.html')

@members_bp.route('/search', methods=['GET', 'POST'])
def search():
    from .forms.member_search import MemberSearchForm
    form = MemberSearchForm()

    if form.validate_on_submit():
        search_type = form.search_type.data
        query = form.search_field.data

        return redirect(url_for('members.results', 
                                search_type=search_type, 
                                query=query))

    return render_template('members/search.html', option="search", form=form)


@members_bp.route('/search/results')
def results():
    search_type = request.args.get('search_type')
    query = request.args.get('query')

    r = requests.get(
        f'https://members-api.parliament.uk/api/Members/Search?{search_type}={query}&skip=0&take=20',
        auth=('user', 'pass')
    )
    results = r.json()
    print(results)

    return render_template('members/results.html', results=results)