from apireader import APIReader
from apisearcher import APISearcher
from resources.newrecipes import CRAFTING_RECIPES

import pandas as pd
import numpy as np
        
class DataAnalyzer:
    WEEKLY_MOVED = "MovingWeek"
    PPU = "pricePerUnit"
    BUY_ORDER = "sell"
    SELL_OFFER = "buy"

    COL_NAMES = ["Item Name", "Buy Price", "Sell Price", "Quantity", "Profit", "ROI", "Leftover", "Buy Wait", "Sell Wait", "Total Wait"]

    MAX_QUANTITY = 71680
    HOURS_PER_WEEK = 168

    def __init__(self, api_searcher: APISearcher):
        self.api_searcher = api_searcher
        self.recipes: dict = CRAFTING_RECIPES

    def compute_profit(self, user_coins: int) -> pd.DataFrame:
        computed_results = []
        if self.api_searcher.api_reader.last_updated == 0:
            return pd.DataFrame()
        
        for result_item, info in self.recipes.items():
            result_quantity = info.get("QUANTITY")
            recipe = info.get("RECIPE")

            craft_cost = self._compute_craft_cost(recipe)
            buy_wait_time = self._compute_wait_time(recipe, DataAnalyzer.BUY_ORDER)
            craft_quantity = min(DataAnalyzer.MAX_QUANTITY,
                           user_coins // craft_cost)
            total_quantity = craft_quantity * result_quantity
            buy_cost = craft_cost*craft_quantity
            
            
            craft_sell = self.api_searcher.search_top_sell(result_item).loc[0, DataAnalyzer.PPU] * total_quantity
            sell_wait_time = self._compute_wait_time({result_item: total_quantity}, DataAnalyzer.SELL_OFFER)

            profit = craft_sell - buy_cost
            total_wait_time = buy_wait_time + sell_wait_time

            leftover = user_coins - buy_cost
            
            # handling numpy's nan scalar divide warning
            with np.errstate(invalid="ignore", divide="ignore"):
                roi = (profit / buy_cost) * 100

            agg_info = [result_item, buy_cost, craft_sell, craft_quantity, profit, roi, leftover, buy_wait_time, sell_wait_time, total_wait_time]
            computed_results.append(agg_info)
        return pd.DataFrame(computed_results, columns=DataAnalyzer.COL_NAMES)

    def _compute_craft_cost(self, recipe):
        cost = 0
        for item, quantity in recipe.items():
            # returns a df, we find the first price index and multiply it by quantity
            valid_search = self.api_searcher.search_top_sell(item)
            if valid_search is not None and len(valid_search) > 0:
                cost += valid_search.loc[0, DataAnalyzer.PPU] * quantity
        if cost == 0:
            return np.nan
        return cost
    
    def _compute_wait_time(self, recipe, type_of_wait):
        if type_of_wait not in ["buy", "sell"]:
            return -1
        wait_time = 0
        for item, quantity in recipe.items():
            quick_status = self.api_searcher.search_quick_status(item)
                    # quick status reports items sold/bought in a week, we convert to hourly.
            items_per_week = quick_status.get(f"{type_of_wait}{DataAnalyzer.WEEKLY_MOVED}")
            if items_per_week:
                wait_time += (quantity * DataAnalyzer.HOURS_PER_WEEK) / items_per_week
        return wait_time
