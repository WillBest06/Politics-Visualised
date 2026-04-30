from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    from .routes.petitions import petitions_bp
    app.register_blueprint(petitions_bp)

    return app