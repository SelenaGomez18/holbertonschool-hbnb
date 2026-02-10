from hbnb.app.extensions import db
from hbnb.app.persistence.repository import Repository


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return obj

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key) and key not in ["id", "created_at"]:
                setattr(obj, key, value)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            return obj
        return None

    def get_by_attribute(self, attr_name, attr_value):
        column = getattr(self.model, attr_name, None)
        if not column:
            return None

        return self.model.query.filter(column == attr_value).first()
