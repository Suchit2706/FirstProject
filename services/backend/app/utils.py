import requests

def make_http_get_request(url, params):
    response = requests.get(url, params=params)
    return response.json()