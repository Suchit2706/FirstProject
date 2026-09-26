import yaml

class Config:
    geocode_url: str
    openmeteo_url: str
    route_url: str

    def __str__(self):
        return f"Config(geocode_url={self.geocode_url}, openmeteo_url={self.openmeteo_url}, route_url={self.route_url})"

def get_config():
    with open(".\\configs\\properties.yaml", 'r') as file:
        loaded_data = yaml.safe_load(file)

    config = Config()
    config.geocode_url = loaded_data.get('geocode_url')
    config.openmeteo_url = loaded_data.get('openmeteo_url')
    config.route_url = loaded_data.get('route_url')

    return config