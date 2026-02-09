from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.extensions import bcrypt
from hbnb.app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # USERS

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        data_to_update = {}

        if 'first_name' in user_data:
            data_to_update['first_name'] = user_data['first_name']

        if 'last_name' in user_data:
            data_to_update['last_name'] = user_data['last_name']

        if 'email' in user_data:
            if not is_admin:
                raise ValueError("Only admins can update email")
            data_to_update['email'] = user_data['email']

        if 'password' in user_data:
            if not is_admin:
                raise ValueError("Only admins can update password")
            data_to_update['password'] = bcrypt.generate_password_hash(
                user_data['password']
            ).decode('utf-8')

        return self.user_repo.update(user_id, data_to_update)

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)

    # AMENITIES

    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=amenity_data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if "name" in amenity_data:
            amenity.name = amenity_data["name"]

        return amenity

    # PLACES

    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        clean_data = place_data.copy()
        clean_data.pop('owner_id', None)
        clean_data.pop('amenities', None)

        if "description" not in clean_data:
            raise ValueError("Description is required")

        place = Place(owner_id=owner.id, **clean_data)
        place.amenities = amenities

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        for key, value in place_data.items():
            setattr(place, key, value)

        return place

    # REVIEWS

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews


facade = HBnBFacade()
