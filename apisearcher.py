import pandas as pd
import numpy as np

class APISearcher:
    SELL = "sell_summary"
    BUY = "buy_summary"
    QUICK = "quick_status"

    VALUE_ERRORMSG = "Count argument must be at least 1."
    SUBMTD_ERRORMSG = "Submethod invalid or not specified. Use BUY/SELL."

    DEFAULT_SEARCH = {"amount": np.nan, "pricePerUnit": np.nan, "orders": np.nan}

    def __init__(self, api={}):
        self.set_api(api)

    def set_api(self, api: dict):
        self.api = api

    # returns entire subdictionary related to a specific item
    def _search_by_id(self, item_id):
        return self.api.get(item_id)
    
    def _search_top_n(self, item_id, submethod="", count=1):
        if submethod not in [APISearcher.SELL, APISearcher.BUY]:
            raise ValueError(APISearcher.SUBMTD_ERRORMSG)
        if count < 1:
            raise ValueError(APISearcher.VALUE_ERRORMSG)
        
        stored_results = []
        pre_search = self._search_by_id(item_id)
        if not pre_search:
            return None
        search_result = pre_search.get(submethod)

        # Ensuring we iterate over nonempty values
        count = len(search_result) if len(search_result) < count else count

        for i in range(count):
            stored_results.append(search_result[i])
        if count == 0:
            # fills blanks df with default values
            stored_results.append(APISearcher.DEFAULT_SEARCH)
        return pd.DataFrame(stored_results)
    
    def search_top_buy(self, item_id, count=1):
        return self._search_top_n(item_id, APISearcher.BUY, count)
    
    def search_top_sell(self, item_id, count=1):
        return self._search_top_n(item_id, APISearcher.SELL, count)
    
    def search_quick_status(self, item_id):
        valid_search = self._search_by_id(item_id)
        if valid_search:
            return valid_search.get(APISearcher.QUICK)
        return {}

        