from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # ---------- USERS ----------

    def create_user(self, user_data):
        password = user_data.pop("password", None)
        user = User(**user_data)

        if password:
            user.set_password(password)

        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        data_to_update = {}

        if "first_name" in user_data:
            data_to_update["first_name"] = user_data["first_name"]

        if "last_name" in user_data:
            data_to_update["last_name"] = user_data["last_name"]

        if "email" in user_data:
            if not is_admin:
                raise ValueError("Only admins can update email")
            data_to_update["email"] = user_data["email"]

        if "password" in user_data:
            if not is_admin:
                raise ValueError("Only admins can update password")
            user.set_password(user_data["password"])

        return self.user_repo.update(user_id, data_to_update)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ---------- AMENITIES ----------

    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")

        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # ---------- PLACES ---------

    def create_place(self, place_data):
        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        clean_data = place_data.copy()
        clean_data.pop("owner_id", None)
        clean_data.pop("amenities", None)

        place = Place(owner_id=owner.id, **clean_data)
        place.amenities = amenities

        return self.place_repo.add(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # ---------- REVIEWS ----------

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews


facade = HBnBFacade()
