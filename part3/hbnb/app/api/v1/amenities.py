from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from hbnb.app.services.facade import facade
from hbnb.app.utils.decorators import admin_required

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

@api.route('/')
class AmenityList(Resource):

    @api.response(200, 'Amenities retrieved successfully')
    def get(self):
        """Get list of amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200

    @jwt_required()
    @admin_required
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            amenity = facade.create_amenity(api.payload)
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @api.response(200, 'Amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @jwt_required()
    @admin_required
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update amenity (admin only)"""
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
