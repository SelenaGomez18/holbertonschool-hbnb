from hbnb.app import create_app
from hbnb.app.services.facade import facade

app = create_app()

with app.app_context():
    user = facade.create_user({
        "first_name": "Admin",
        "last_name": "Root",
        "email": "admin@mail.com",
        "password": "admin123",
        "is_admin": True
    })

    print("Admin creado:", user.email)
