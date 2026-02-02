#!/usr/bin/python3
"""
This module defines the User class for the HBnB project.
It now includes password handling for security.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import bcrypt
import re


class User(BaseModel):
    EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
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

        if password:
            self.set_password(password)

    def set_password(self, password):
        """
        Hash and store the password securely.
        """
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """
        Verify a password against the stored hash.
        """
        return bcrypt.check_password_hash(self.password, password)

    def verify_password(self, password):
        """
        Alias used by auth/login
        """
        return self.check_password(password)

    def to_dict(self):
        """
        Return dict representation without exposing password.
        """
        data = super().to_dict()
        data.pop("password", None)
        return data
