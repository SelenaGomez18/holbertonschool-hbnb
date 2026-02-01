from hbnb.app.persistence.repository  import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

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

        place = Place(owner=owner, **clean_data)

        place.amenities = amenities
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
       place = self.get_place(place_id)

       if not place:
           return None

       for key, value in place_data.items():
           setattr(place, key, value)


       return place

    def create_review(self, review_data):
        rating = review_data.get("rating")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        user = self.repository.get(User, review_data["user_id"])
        if not user:
            raise ValueError("User not found")

        place = self.repository.get(Place, review_data["place_id"])
        if not place:
            raise ValueError("Place not found")

        review = Review(**review_data)
        self.repository.add(review)

        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.repository.get(Review, review_id)

    def get_all_reviews(self):
        return self.repository.get_all(Review)

    def get_reviews_by_place(self, place_id):
        place = self.repository.get(Place, place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.repository.get(Review, review_id)
        if not review:
            return None

        if "text" in review_data:
            review.text = review_data["text"]

        if "rating" in review_data:
            if review_data["rating"] < 1 or review_data["rating"] > 5:
                raise ValueError("Rating must be between 1 and 5")
            review.rating = review_data["rating"]

        return review

    def delete_review(self, review_id):
        review = self.repository.get(Review, review_id)
        if not review:
            return False

        place = self.repository.get(Place, review.place_id)
        if place:
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.repository.delete(review)
        return True

facade = HBnBFacade()
