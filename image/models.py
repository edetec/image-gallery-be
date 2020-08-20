from sqlalchemy import String, Column

from app.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = Column(String, unique=True, nullable=False)
    thumbnail_name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    format = Column(String, nullable=False)
    dimensions = Column(String, nullable=False)
