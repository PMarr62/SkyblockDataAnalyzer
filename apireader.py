import requests

class APIReader:
    hypixel_api_url = r"https://api.hypixel.net/v2/skyblock/bazaar"
    refresh_tag = "lastUpdated"
    products = "products"

    def __init__(self):
        self.last_updated = 0
        self.json_response = {}

    def update_response(self):
        try:
            response = requests.get(APIReader.hypixel_api_url)
            if response.ok:
                jsonified = response.json()
                self.last_updated = jsonified.get(APIReader.refresh_tag)
                self.json_response = jsonified.get(APIReader.products)
            return response.status_code
        except requests.exceptions.ConnectionError as e:
            print("Connection failed:\n", e)
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException as e:
            print("Request failed:\n", e)

    def okay(self):
        return bool(self.last_updated)
