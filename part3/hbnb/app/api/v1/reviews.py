from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True)
})

update_model = api.model('ReviewUpdate', {
    'text': fields.String,
    'rating': fields.Integer
})

@api.route('/')
class ReviewList(Resource):

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Invalid data')
    def post(self):
        current_user_id = get_jwt_identity()
        data = api.payload

        place = facade.get_place(data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place."}, 400

        existing_reviews = facade.get_reviews_by_place(place.id)
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {"error": "You have already reviewed this place"}, 400

        data['user_id'] = current_user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved')
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review retrieved')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {}, 204
