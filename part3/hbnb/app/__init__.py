from flask import Flask
from flask_restx import Api
from hbnb.app.extensions import bcrypt

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    return app
