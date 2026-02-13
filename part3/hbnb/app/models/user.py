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
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ---------- Relationships ----------
    places = db.relationship(
        "Place",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ---------- Email helpers ----------

    @staticmethod
    def normalize_email(email):
        return email.lower().strip()

    @classmethod
    def validate_email(cls, email):
        return re.match(cls.EMAIL_REGEX, email) is not None

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
