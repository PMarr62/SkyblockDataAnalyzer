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
    
    def search_buy_order_price(self, item_id: str):
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return None
        top_buy_order = valid_item_search.get("sell_summary")[0].get("pricePerUnit")
        if not top_buy_order:
            return valid_item_search.get("quick_status").get("sellPrice")
        return top_buy_order

    def search_sell_offer_price(self, item_id: str):
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return None
        top_sell_offer = valid_item_search.get("buy_summary")[0].get("pricePerUnit")
        if not top_sell_offer:
            return valid_item_search.get("quick_status").get("buyPrice")
        return top_sell_offer

    def search_quick_status(self, item_id: str):
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return {}
        return valid_item_search.get("quick_status")

