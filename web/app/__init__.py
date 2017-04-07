from flask import Flask
from app.response import JSONResponse
from config import config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
sentry = Sentry()


def create_app(config_name):
    """Application factory, see docs."""
    app = Flask(__name__)
    app.response_class = JSONResponse
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    sentry.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
