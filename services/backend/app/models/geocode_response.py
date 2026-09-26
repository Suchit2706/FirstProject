import json
from pydantic import BaseModel

class GeocodeResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: float
    country_code: str
    admin1: str = None
    admin2: str = None
    admin3: str = None

    model_config = {
        "extra": "ignore"
    }
