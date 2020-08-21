from sqlalchemy import String, Column

from app.database import db


class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = Column(String, unique=True, nullable=False)
    thumbnail_path = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    format = Column(String, nullable=False)
    dimensions = Column(String, nullable=False)
