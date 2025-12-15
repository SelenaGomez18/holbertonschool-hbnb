from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from app.models.user import User


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        repo = current_app.repository
        return repo.list('User')


    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        user = User(**data)
        current_app.repository.save(user)
        return user, 201

@api.route('/<string:user_id>')
class UserDetail(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        return current_app.repository.get('User', user_id)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        repo = current_app.repository
        user = repo.get('User', user_id)
        user.update(request.json)
        repo.save(user)
        return user

    def delete(self, user_id):
        current_app.repository.delete('User', user_id)
        return {'message': 'User deleted'}
