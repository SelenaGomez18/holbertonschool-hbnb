from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

update_model = api.model('ReviewUpdate', {
    'text': fields.String,
    'rating': fields.Integer
})

@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Invalid data')
    def post(self):
        try:
            review = facade.create_review(request.json)
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

    def put(self, review_id):
        try:
            review = facade.update_review(review_id, request.json)
            if not review:
                return {"error": "Review not found"}, 404
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    def delete(self, review_id):
        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
