#!/usr/bin/python3
"""
This module defines the User class for the HBnB project.
It now includes password handling for security.
"""


from hbnb.app.models.base_model import BaseModel
import bcrypt

class User(BaseModel):
    """
    User class that stores personal information and login credentials.
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        # Initialize the base model features.
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # Hash the password immediately for safety.
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        """
        Transforms a plain password into a secure, unreadable string.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password):
        """
        Checks if the provided password matches the secure stored one.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
