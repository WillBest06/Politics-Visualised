from flask import Flask
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    csrf = CSRFProtect(app) 

    from .routes.petitions import petitions_bp
    app.register_blueprint(petitions_bp)

    return app