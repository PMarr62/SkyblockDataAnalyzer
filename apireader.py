import requests

class APIReader:
    hypixel_api_url = r"https://api.hypixel.net/v2/skyblock/bazaar"

    def __init__(self):
        self.json_response: dict = {}

    def update_response(self) -> int:
        response = requests.get(self.hypixel_api_url)
        if response.ok:
            self.json_response = response.json().get("products")
        return response.status_code
    
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

    def _search_item_id(self, item_id: str):
        return self.json_response.get(item_id)
    
    """
    Ensure the item exist. Once it does, first try to return the buy order price. If none, lookup from quick status.
    """

    def _search_price(self, item_id: str, type_of_search: str):
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return -1
        top_order = valid_item_search.get(f"{type_of_search}_summary")[0].get("pricePerUnit")
        if not top_order:
            return valid_item_search.get("quick_status").get(f"{type_of_search}Price")
        return top_order
    
    def search_buy_order_price(self, item_id: str) -> int:
        return self._search_price(item_id, "sell")

    def search_sell_offer_price(self, item_id: str) -> int:
        return self._search_price(item_id, "buy")

    def search_quick_status(self, item_id: str) -> dict:
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return {}
        return valid_item_search.get("quick_status")

