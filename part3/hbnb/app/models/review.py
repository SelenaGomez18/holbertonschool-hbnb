#!/usr/bin/python3
"""
Review SQLAlchemy model for HBnB.
Mapped with relationships to User and Place.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ---------- Foreign Keys ----------
    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id"),
        nullable=False
    )

    place_id = db.Column(
        db.String,
        db.ForeignKey("places.id"),
        nullable=False
    )
