import requests
from typing import Callable

class APIReader:
    hypixel_api_url = r"https://api.hypixel.net/v2/skyblock/bazaar"
    BAD_PRICE = -1

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

    """
    Ensure the item exists. Then, ensure there is at least one buy order price. If not, return quick status. Ensure quick status is not 0.
    If it is, attempt to return sell offer price of original item. If not, return quick status. If nothing exists, return a bad value.
    """

    def _search_price(self, item_id: str, type_of_search: str, min_max: Callable):
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:   
            return self.BAD_PRICE
        top_order = valid_item_search.get(f"{type_of_search}_summary")
        if not top_order:
            # Logic works because buy price > sell price
            quick_status_get = valid_item_search.get("quick_status")
            check_for_no_movement = min_max(quick_status_get.get("buyPrice"), quick_status_get.get("sellPrice"))
            if not check_for_no_movement:
                return self.BAD_PRICE
            return check_for_no_movement
        return top_order[0].get("pricePerUnit")

    # def _search_price(self, item_id: str, type_of_search: str):
    #     valid_item_search = self._search_item_id(item_id)
    #     if not valid_item_search:
    #         return -1
    #     top_order = valid_item_search.get(f"{type_of_search}_summary")
    #     if not top_order:
    #         return valid_item_search.get("quick_status").get(f"{type_of_search}Price")
    #     return top_order[0].get("pricePerUnit")
    
    def search_buy_order_price(self, item_id: str) -> int:
        return self._search_price(item_id, "sell", min)

    def search_sell_offer_price(self, item_id: str) -> int:
        return self._search_price(item_id, "buy", max)

    def search_quick_status(self, item_id: str) -> dict:
        valid_item_search = self._search_item_id(item_id)
        if not valid_item_search:
            return {}
        return valid_item_search.get("quick_status")

