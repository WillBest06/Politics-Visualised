from flask import Flask
from flask_wtf.csrf import CSRFProtect

import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'local-dev-only-key'),
        
        SESSION_TYPE='filesystem',
        SESSION_FILE_DIR=os.path.join(app.root_path, 'flask_session_data'),
        SESSION_PERMANENT=False,

        MAX_CONTENT_LENGTH=5 * 1024 * 1024
    )

    csrf = CSRFProtect(app) 

    from .routes.petitions import petitions_bp
    from .routes.home import home_bp
    from .routes.members import members_bp
    app.register_blueprint(petitions_bp, url_prefix='/petitions')
    app.register_blueprint(home_bp)
    app.register_blueprint(members_bp, url_prefix='/members')

    return app