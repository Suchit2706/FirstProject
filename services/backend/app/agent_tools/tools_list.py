from agent_tools.geo_tools import get_geocode_data, get_weather_data, get_route_data

def get_tools_list():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_geocode_data",
                "description": "Fetches geocode data for a given location name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location_name": {"type": "string"},
                        "count": {"type": "integer", "default": 10},
                        "language": {"type": "string", "default": 'en'},
                        "format": {"type": "string", "default": 'json'}
                    },
                    "required": ["location_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather_data",
                "description": "Fetches weather data for given latitude and longitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                        "hourly": {"type": "string", "description": "List of hourly weather parameters to fetch. They should be comma-separated and no spaces. Types:temperature_2m,rain,snowfall,cloudcover,windspeed_10m,windgusts_10m,uv_index"}
                    },
                    "required": ["latitude", "longitude", "hourly"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_route_data",
                "description": "Fetches route data between two geographical points.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_latitude": {"type": "number"},
                        "start_longitude": {"type": "number"},
                        "end_latitude": {"type": "number"},
                        "end_longitude": {"type": "number"},
                        "route_type": {"type": "string", "description": "The type of route to fetch. Types:driving,walking,cycling"}
                    },
                    "required": ["start_latitude", "start_longitude", "end_latitude", "end_longitude", "route_type"]
                }
            }
        }
    ]
    return tools

def get_functions_dict():
    return {
        "get_geocode_data": get_geocode_data,
        "get_weather_data": get_weather_data,
        "get_route_data": get_route_data
    }