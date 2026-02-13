#!/usr/bin/python3
"""
Amenity SQLAlchemy model for HBnB.
Only core attributes mapped — no relationships yet.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)
