from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = user(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user.id)
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        return user

    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")
        
        amenity = Amenity(name=amenity_data["name"])

        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None
        
        if "name" in amenity_data and amenity_data["name"]:
            amenity.name = amenity_data["name"]

        self.amenity_repo.update(amenity_id, amenity)


        return amenity
    
    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass