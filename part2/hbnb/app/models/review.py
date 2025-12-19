
from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.place import Place
from hbnb.app.models.user import User

class Review(BaseModel):
    """Review entity with validation"""

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")

        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        place.add_review(self)
