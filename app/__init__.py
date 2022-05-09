from flask import Flask

from app.config import Config, ProductionConfig
from .extensions import db, migrate, api
from app.main import aquarium_bp


def create_app(settings=Config):
    app = Flask(__name__)
    app.config.from_object(settings)

    initialize_blueprints(app)
    initialize_extensions(app)
    return app


def initialize_blueprints(app):
    app.register_blueprint(aquarium_bp)
    return None


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    api.init_app(app)
    return None
