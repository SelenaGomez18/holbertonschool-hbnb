#!/usr/bin/python3
"""
Place model for HBnB project.
Description field is optional.
"""

from hbnb.app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner_id,
        description=None,
        amenities=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 chars")

        if price is None or price < 0:
            raise ValueError("Price must be a positive number")

        if latitude is None or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if longitude is None or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.description = description
        self.amenities = amenities 
