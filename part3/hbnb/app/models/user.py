#!/usr/bin/python3
"""
User SQLAlchemy model for HBnB.
"""

import re
from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db, bcrypt


class User(BaseModel):
    __tablename__ = "users"

    EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ---------- Password handling ----------

    def set_password(self, password):
        if not password:
            raise ValueError("Password required")

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def verify_password(self, password):
        return self.check_password(password)

    # ---------- Serialization ----------

    def to_dict(self):
        data = super().to_dict()
        data.pop("password", None)
        return data
