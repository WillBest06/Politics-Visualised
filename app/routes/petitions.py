# logo idea politics is an old serif font and visualised is a modern sans serif font

from flask import Blueprint, render_template

petitions_bp = Blueprint("petitions", __name__)

@petitions_bp.route('/petitions')
def petition_options():
    return render_template('petitions.html')

# @petitions_bp.route('/petitions/save')
# @login_required
# def save():
#     pass