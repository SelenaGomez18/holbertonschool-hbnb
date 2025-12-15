from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from app.models.review import Review

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.String(required=True),
    'user_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        return current_app.repository.list('Review')

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        repo = current_app.repository
        data = request.json

        place = repo.get('Place', data['place_id'])
        user = repo.get('User', data['user_id'])


        review = Review(
            text=data['text'],
            rating=data['rating'],
            place=place,
            user=user
        )


        place.add_review(review)
        repo.save(review)
        repo.save(place)


        return review, 201

@api.route('/<string:review_id>')
class ReviewDetail(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        return current_app.repository.get('Review', review_id)

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        repo = current_app.repository
        review = repo.get('Review', review_id)
        data = request.json


        review.update(data)
        repo.save(review)
        return review


    def delete(self, review_id):
        current_app.repository.delete('Review', review_id)
        return {'message': 'Review deleted'}
