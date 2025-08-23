import requests

class APIReader:
    hypixel_api_url = r"https://api.hypixel.net/v2/skyblock/bazaar"
    BAD_VALUE = -1
    refresh_tag = "lastUpdated"
    products = "products"

    def __init__(self):
        self.last_updated = 0
        self.json_response = {}

    def update_response(self):
        response = requests.get(APIReader.hypixel_api_url)
        if response.ok:
            jsonified = response.json()
            self.last_updated = jsonified.get(APIReader.refresh_tag)
            self.json_response = jsonified.get(APIReader.products)
        return response.status_code
