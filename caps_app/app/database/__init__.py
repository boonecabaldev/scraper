import click
from flask_sqlalchemy import SQLAlchemy

from .. import config

# Database connection string
DATABASE_URL = config.get('SQLALCHEMY_DATABASE_URI')

def db_connect(app):
    """
    Performs database connection using the database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return SQLAlchemy(app)

def create_table(engine):
    """
    Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
    """
    engine.metadata.create_all(engine)

@click.command()
def reset_database():
    #
    # Recreate all tables in the database
    #
    from ..models import HatComponent, HatLeaf

    from sqlalchemy import MetaData
    from flask_sqlalchemy import MetaData

    engine = db_connect()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    try:
        # Delete all tables in the database
        metadata.drop_all(engine)
        # Recreate all tables in the database
        HatComponent.metadata.create_all(engine)
        HatLeaf.metadata.create_all(engine)
    except:
        raise
