"""
File Name: apisearcher.py

Class to use search functionalities to find respective data in the APIReader object.
"""

import pandas as pd
import numpy as np

from apireader import APIReader

class APISearcher:
    SELL = "sell_summary"
    BUY = "buy_summary"
    QUICK = "quick_status"

    VALUE_ERRORMSG = "Count argument must be at least 1."
    SUBMTD_ERRORMSG = "Submethod invalid or not specified. Use BUY/SELL."
    
    DEFAULT_BUY_SELL_SEARCH = {"amount": np.nan, "pricePerUnit": np.nan, "orders": np.nan}
    DEFAULT_QUICK_SEARCH = {"productId": "", "sellPrice": np.nan, "sellVolume": np.nan,
                            "sellMovingWeek": np.nan, "sellOrders": np.nan, "buyPrice": np.nan,
                            "buyVolume": np.nan, "buyMovingWeek": np.nan, "buyOrders": np.nan}

    def __init__(self, api_reader: APIReader):
        self.set_api_reader(api_reader)

    # designates an APIReader object to this object.
    def set_api_reader(self, api_reader: APIReader):
        self.api_reader = api_reader

    # returns entire subdictionary from API related to a specific item
    def _search_by_id(self, item_id) -> dict:
        if self.api_reader.okay():
            return self.api_reader.json_response.get(item_id, {})
        return {}
    
    # returns n pricings of buy / sell orders of a specific item.
    def _search_top_n(self, item_id: str, submethod: str="", count: int=1) -> pd.DataFrame:
        default_df = pd.DataFrame(APISearcher.DEFAULT_BUY_SELL_SEARCH, index=[0])
        if not self.api_reader.okay():
            return default_df
        if submethod not in [APISearcher.SELL, APISearcher.BUY]:
            raise ValueError(APISearcher.SUBMTD_ERRORMSG)
        if count < 1:
            raise ValueError(APISearcher.VALUE_ERRORMSG)
        
        stored_results = []
        pre_search = self._search_by_id(item_id)
        if not pre_search:
            return default_df
        search_result = pre_search.get(submethod)

        # Ensuring we iterate over nonempty values
        if not search_result:
            return default_df
        count = len(search_result) if len(search_result) < count else count
        if count == 0:
            return default_df
        for i in range(count):
            stored_results.append(search_result[i])
        return pd.DataFrame(stored_results)
    
    # method to return the top n buy orders of an item.
    def search_top_buy(self, item_id: str, count: int=1) -> pd.DataFrame:
        return self._search_top_n(item_id, APISearcher.BUY, count)
    
    # method to return the top n sell offers of an item.
    def search_top_sell(self, item_id: str, count: int=1) -> pd.DataFrame:
        return self._search_top_n(item_id, APISearcher.SELL, count)
    
    # method to return quick status information of an item.
    def search_quick_status(self, item_id: str) -> dict:
        valid_search = self._search_by_id(item_id)
        if valid_search:
            return valid_search.get(APISearcher.QUICK, APISearcher.DEFAULT_QUICK_SEARCH)
        return APISearcher.DEFAULT_QUICK_SEARCH
