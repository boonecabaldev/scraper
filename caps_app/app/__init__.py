from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
#from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
