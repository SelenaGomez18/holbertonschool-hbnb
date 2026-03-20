import os
from flask import Flask
from hbnb.app.api.v1 import blueprint as api_v1_blueprint
from hbnb.app.extensions import bcrypt, jwt, db


def create_app(config_class="config.DevelopmentConfig"):

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, "part4", "base_files"),
        static_url_path=""
    )

    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_v1_blueprint)

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app
