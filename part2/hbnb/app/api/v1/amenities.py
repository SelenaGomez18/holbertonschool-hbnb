from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return current_app.repository.list('Amenity')

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.json
        amenity = Amenity(name=data['name'])
        current_app.repository.save(amenity)
        return amenity, 201

    def delete(self, amenity_id):
        current_app.repository.delete('Amenity', amenity_id)
        return {'message': 'Amenity deleted'}
