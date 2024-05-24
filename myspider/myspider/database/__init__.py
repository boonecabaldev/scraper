from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Database connection string
DATABASE_URL = "sqlite:///mydatabase.db"  # replace with your actual connection string

Base = declarative_base()

def db_connect():
    """
    Performs database connection using the database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return create_engine(DATABASE_URL)

def create_table(engine):
    """
    Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
    """
    Base.metadata.create_all(engine)

def reset_database():
    #
    # Recreate all tables in the database
    #
    from ..models import HatComponent, HatLeaf

    from sqlalchemy import MetaData

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
