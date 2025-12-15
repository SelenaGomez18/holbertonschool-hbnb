from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from app.models.place import Place


api = Namespace('places', description='Place operations')


place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        return current_app.repository.list('Place')


    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.json
        owner = current_app.repository.get('User', data['owner_id'])
        place = Place(
            title=data['title'],
            description=data.get('description'),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner
        )
        current_app.repository.save(place)
        return place, 201

@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        return current_app.repository.get('Place', place_id)


@api.expect(place_model)
@api.marshal_with(place_model)
def put(self, place_id):
    repo = current_app.repository
    place = repo.get('Place', place_id)
    data = request.json

    if 'owner_id' in data:
        data['owner'] = repo.get('User', data['owner_id'])
        del data['owner_id']


    place.update(data)
    repo.save(place)
    return place

def delete(self, place_id):
    current_app.repository.delete('Place', place_id)
    return {'message': 'Place deleted'}
