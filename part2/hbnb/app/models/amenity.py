
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity"""

    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters")

        self.name = name
