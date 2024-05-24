from .database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class HatComposite(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    img_src = Column(String)
    img_file_path = Column(String)

class HatComponent(HatComposite):
    __tablename__ = 'hatcomponents'

    url = Column(String)

    leaves = relationship("HatLeaf", backref="hatcomponent")

class HatLeaf(HatComposite):
    __tablename__ = 'hatleafs'

    node_id = Column(Integer, ForeignKey('hatcomponents.id'))
    h3_title = Column(String)
    date_string = Column(String)