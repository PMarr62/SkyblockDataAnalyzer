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
    
    """
    The following three functions define buy orders, sell offers, and quick statuses.
    On the Hypixel API, a "buy order" refers to the most expensive asking price of an item.
    Buy orders that are filled come from players who "insta-sell" items from the Bazaar.

    On the contrary, a "sell offer" refers to the cheapest buying price of an item.
    Sell offers that are filled come from players who "insta-buy" items from the Bazaar.

    This is to clear up any confusion as to when the "buy order" function searches for an 
    item's sell price, and when the "sell offer" function searchers for an item's buy price.

    A given item's quick status is a portion of an item's API which contains information
    such as weekly buy/sell values, a current market quantity of the item.
    """
    
    def search_buy_order_price(self, item_id: str):
        pass

    def search_sell_offer_price(self, item_id: str):
        pass

    def search_quick_status(self, item_id: str):
        pass

