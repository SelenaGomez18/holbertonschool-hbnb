from hbnb.app.models.base_model import BaseModel
import re

class User(BaseModel):

    EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

    def __init__(self, first_name, last_name, email, is_admin=False, **kwargs):
        super().__init__(**kwargs)

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be <= 50 characters")

        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")

        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
