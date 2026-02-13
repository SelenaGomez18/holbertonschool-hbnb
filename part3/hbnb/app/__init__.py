from flask import Flask
from hbnb.app.api.v1 import blueprint as api_v1_blueprint
from hbnb.app.extensions import bcrypt, jwt, db

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_v1_blueprint)

    return app
