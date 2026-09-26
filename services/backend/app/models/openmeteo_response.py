from pydantic import BaseModel
import json

class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    hourly_units: dict
    hourly: Hourly

    model_config = {
        "extra": "ignore"
    }

class Hourly(BaseModel):
    time: list[str] = []
    temperature_2m: list[float] = []
    relativehumidity_2m: list[float] = []
    apparent_temperature: list[float] = []
    precipitation: list[float] = []
    rain: list[float] = []
    snowfall: list[float] = []
    cloudcover: list[float] = []
    windspeed_10m: list[float] = []
    windgusts_10m: list[float] = []
    uv_index: list[float] = []