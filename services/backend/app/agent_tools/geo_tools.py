from utils import make_http_get_request
from models.geocode_response import GeocodeResponse
from models.openmeteo_response import OpenMeteoResponse
from configs.config import get_config

def get_geocode_data(location_name: str, count: int = 10, language: str = 'en', format: str = 'json'):
    """
    Fetches geocode data for a given location name.
    """
    url = get_config().geocode_url
    query_params = {
        'name': location_name,
        'count': count,
        'language': language,
        'format': format
    }

    response_data = make_http_get_request(url, query_params)

    geocode_response_list = []
    for item in response_data.get('results', []):
        geocode_response = GeocodeResponse.model_validate(item)
        geocode_response_list.append(geocode_response)

    return geocode_response_list

def get_weather_data(latitude: float, longitude: float, hourly: str | None = None):
    """
    Fetches weather data for given latitude and longitude.
    """
    if hourly is None:
        hourly = "temperature_2m"
        
    url = get_config().openmeteo_url
    query_params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': hourly,
    }

    response_data = make_http_get_request(url, query_params)

    print(f"Weather data response: {response_data}")  # Debugging line to print the response data

    openmeteo_response = OpenMeteoResponse.model_validate(response_data)
    return openmeteo_response

def get_route_data(start_latitude: float, start_longitude: float, end_latitude: float, end_longitude: float, route_type: str = 'driving'):
    """
    Fetches route data between two geographical points.
    """
    url = get_config().route_url
    url += f"/{route_type}/{start_longitude},{start_latitude};{end_longitude},{end_latitude}"
    query_params = {
        'steps': 'true'
    }

    response_data = make_http_get_request(url, query_params)

    print(f"Route data response: {response_data}")  # Debugging line to print the response data

    return response_data