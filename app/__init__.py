from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_type='dev'):
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_type])

    db.init_app(app)

    from .v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app
