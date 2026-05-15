from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

# initialises extensions
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'local-dev-only-key'),
        
        SQLALCHEMY_DATABASE_URI="sqlite:///politics_visualised.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='filesystem',
        SESSION_FILE_DIR=os.path.join(app.root_path, 'flask_session_data'),
        SESSION_PERMANENT=False,

        MAX_CONTENT_LENGTH=5 * 1024 * 1024
    )

    if test_config:
        app.config.update(test_config)

    # initialises the db
    from .models import db
    db.init_app(app)

    # initialises csrf security
    csrf.init_app(app)

    # creates tables for SQLite DB
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'auth.signin'
    login_manager.login_message_category = "danger"

    from .routes.auth import auth_bp
    from .routes.petitions import petitions_bp
    from .routes.home import home_bp
    from .routes.members import members_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(petitions_bp, url_prefix='/petitions')
    app.register_blueprint(home_bp)
    app.register_blueprint(members_bp, url_prefix='/members')

    return app