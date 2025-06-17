from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config  # Import the Config class

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions
   
    CORS(app, resources={r"/*": {"origins": "http://192.168.8.202:5155"}})



    db.init_app(app)

    # Import and register blueprints
    from . import routes
    app.register_blueprint(routes.api_blueprint)

    # Create tables
    with app.app_context():
        db.create_all()

    return app