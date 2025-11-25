from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise database
    db.init_app(app)

    # Register blueprints
    from .main.routes import main
    app.register_blueprint(main)
    
    from .admin.routes import admin
    app.register_blueprint(admin, url_prefix="/admin")


    return app