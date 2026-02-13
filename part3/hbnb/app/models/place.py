#!/usr/bin/python3
"""
Place model for HBnB project.
Description field is optional.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db


# Association table for many-to-many Place ↔ Amenity
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String, db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String, db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # ---------- Foreign Keys ----------
    owner_id = db.Column(
        db.String,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ---------- Relationships ----------
    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",
        lazy="subquery"
    )
