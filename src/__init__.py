"""Initialize Flask app."""
from flask import Flask
from flask_apscheduler import APScheduler as APScheduler
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

from src.config import Config
from src.external_calls import get_token

# Database setup
db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
scheduler = APScheduler()


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    cache.init_app(app)

    # configure app using the Config class defined in src/config.py
    app.config.from_object(Config)
    from src.models import Answer
    db.init_app(app)  # initialise the database for the app
    from src.scheduled_tasks import get_records_scheduled, post_statistics_scheduled
    scheduler.init_app(app)  # initialize scheduler
    scheduler.start()
    with app.app_context():
        db.create_all()

    with app.app_context():
        from src.api import api_bp
        app.register_blueprint(api_bp)

        return app
