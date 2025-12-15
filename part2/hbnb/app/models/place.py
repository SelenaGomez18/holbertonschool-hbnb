
from models.base_model import BaseModel
from models.user import User

class Place(BaseModel):
    """Place entity with relationships"""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters")

        if price <= 0:
            raise ValueError("Price must be a positive number")

        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")

        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")

        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Link a review to this place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Link an amenity to the place"""
        self.amenities.append(amenity)
