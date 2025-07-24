import requests

class APIReader:
    hypixel_api_url = r"https://api.hypixel.net/v2/skyblock/bazaar"

    def __init__(self):
        self.response: requests.Response | None = None

    def update_response(self) -> None:
        self.response = requests.get(self.hypixel_api_url)

    def get_json_response(self) -> dict:
        if self.response:
            return self.response.json()
        return {}