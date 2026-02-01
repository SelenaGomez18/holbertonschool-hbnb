from flask import Blueprint
from flask_restx import Api
from hbnb.app.api.v1.auth import api as auth_ns
from hbnb.app.api.v1.users import api as users_ns

blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="HBnB API",
    version="1.0",
    description="HBnB Application API"
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(users_ns, path="/users")
