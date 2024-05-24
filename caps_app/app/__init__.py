from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name='testing'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
   
    db.init_app(app)

    # models and views initialized after db is initialized
    from . import models
    from .main import views

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
