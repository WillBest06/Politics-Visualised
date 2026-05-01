from flask import Flask
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    csrf = CSRFProtect(app) 

    from .routes.petitions import petitions_bp
    from .routes.home import home_bp
    from .routes.members import members_bp
    app.register_blueprint(petitions_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(members_bp, url_prefix='/members')

    return app