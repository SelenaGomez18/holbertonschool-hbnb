from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from hbnb.app.services.facade import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})


review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})
#-----------------------------------------

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})


# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),

    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
})
#---------------------------------
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()

        data = api.payload
        data['owner_id'] = current_user_id
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [p.to_dict_basic() for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        api.payload.pop('owner_id', None)

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in reviews], 200
