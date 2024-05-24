from flask_sqlalchemy import SQLAlchemy

from . import db

class HatComposite(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    img_src = db.Column(db.String)
    img_file_path = db.Column(db.String)

class HatComponent(HatComposite):
    __tablename__ = 'hatcomponents'

    url = db.Column(db.String)

    leaves = db.Relationship("HatLeaf", backref="hatcomponent")

    text_id = ""

class HatLeaf(HatComposite):
    __tablename__ = 'hatleafs'

    node_id = db.Column(db.Integer, db.ForeignKey('hatcomponents.id'))
    h3_title = db.Column(db.String)
    date_string = db.Column(db.String)