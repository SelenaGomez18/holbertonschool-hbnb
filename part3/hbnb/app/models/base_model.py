import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dictionary representation of the object"""
        data = self.__dict__.copy()

        # Convert datetime objects to ISO format
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()

        # Handle owner (Place)
        if 'owner' in data and data['owner']:
            data['owner_id'] = data['owner'].id
            del data['owner']

        # Handle amenities (Place)
        if 'amenities' in data and data['amenities']:
            data['amenities'] = [amenity.id for amenity in data['amenities']]
        else:
            data['amenities'] = []

        return data
    