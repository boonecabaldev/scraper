from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

# ... rest of your models.py file ...
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HatNode(Base):
    __tablename__ = 'hatnodes'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    local_file_path = Column(String)
    leaves = relationship("HatLeaf", backref="hatnode")

class HatLeaf(Base):
    __tablename__ = 'hatleafs'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    local_file_path = Column(String)
    node_id = Column(Integer, ForeignKey('hatnodes.id'))
    data_src = Column(String)
    data_origin_src = Column(String)
    data_path = Column(String)
    src = Column(String)