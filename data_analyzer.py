from apireader import APIReader
from apisearcher import APISearcher
from resources.newrecipes import CRAFTING_RECIPES

import pandas as pd
import numpy as np

class NewDataCleaner:
    def run_clean(self, df):
        #Remove NAN rows
        df.dropna(subset='Buy Price', inplace=True)

        #Remove <= 0 Rows
        df.drop(df[df['Profit'] <= 0].index, inplace=True)

        #Converting capital underscore items to human-readable
        df['Item Name'] = df['Item Name'].str.replace("_", " ").str.title()
        #Converting coin-based columns to type int
        int_based_cols = ["Buy Price", "Sell Price", "Quantity", "Profit", "Leftover"]
        float_based_cols = ["Buy Wait", "Sell Wait", "Total Wait"]

        
        # formatting numbers with commas
        for int_column in int_based_cols:
            df[int_column] = df[int_column].astype('int') # convert to int
            df[int_column] = df[int_column].astype('object')
            df[int_column] = df[int_column].apply(lambda x: f"{x:,}")
        for float_column in float_based_cols:
            df[float_column] = df[float_column].apply(lambda x: f"{x:,.1f}")
        return df
        


class NewDataAnalyzer:
    WEEKLY_MOVED = "MovingWeek"
    PPU = "pricePerUnit"
    BUY_ORDER = "sell"
    SELL_OFFER = "buy"

    COL_NAMES = ["Item Name", "Buy Price", "Sell Price", "Quantity", "Profit", "Leftover", "Buy Wait", "Sell Wait", "Total Wait"]

    MAX_QUANTITY = 71680
    HOURS_PER_WEEK = 168
    def __init__(self):
        self.api_reader: APIReader = APIReader()
        self.api_searcher: APISearcher = APISearcher()
        self.recipes: dict = CRAFTING_RECIPES

    def link_read_search(self):
        self.api_reader.update_response()
        self.api_searcher.set_api(self.api_reader.json_response)

    def _compute_craft_cost(self, recipe):
        cost = 0
        for item, quantity in recipe.items():
            # returns a df, we find the first price index and multiply it by quantity
            valid_search = self.api_searcher.search_top_sell(item)
            if valid_search is not None and len(valid_search) > 0:
                cost += valid_search.loc[0, NewDataAnalyzer.PPU] * quantity
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
            items_per_week = quick_status.get(f"{type_of_wait}{NewDataAnalyzer.WEEKLY_MOVED}")
            if items_per_week:
                wait_time += (quantity * NewDataAnalyzer.HOURS_PER_WEEK) / items_per_week
        return wait_time


    def compute_profit(self, user_coins):
        computed_results = []
        self.api_reader.update_response()
        if not self.api_reader.json_response:
            return computed_results
        
        for result_item, info in self.recipes.items():
            result_quantity = info.get("QUANTITY")
            recipe = info.get("RECIPE")

            craft_cost = self._compute_craft_cost(recipe)
            buy_wait_time = self._compute_wait_time(recipe, NewDataAnalyzer.BUY_ORDER)
            craft_quantity = min(NewDataAnalyzer.MAX_QUANTITY,
                           user_coins // craft_cost)
            total_quantity = craft_quantity * result_quantity
            buy_cost = craft_cost*craft_quantity
            
            
            craft_sell = self.api_searcher.search_top_sell(result_item).loc[0, NewDataAnalyzer.PPU] * total_quantity
            sell_wait_time = self._compute_wait_time({result_item: total_quantity}, NewDataAnalyzer.SELL_OFFER)

            profit = craft_sell - buy_cost
            total_wait_time = buy_wait_time + sell_wait_time

            leftover = user_coins - buy_cost

            agg_info = [result_item, buy_cost, craft_sell, craft_quantity, profit, leftover, buy_wait_time, sell_wait_time, total_wait_time]
            computed_results.append(agg_info)
        return pd.DataFrame(computed_results, columns=NewDataAnalyzer.COL_NAMES)
            

class DataAnalyzer:
    def __init__(self):
        self.api_reader: APIReader = APIReader()
        self.recipes: dict = {}
        
    def _fix_string(self, item_id: str):
        return item_id.replace("_", " ").title()
    
    def _fix_float(self, value: float):
        return f"{value:,.1f}"

    def read_recipe_json(self, recipe_path):
        with open(recipe_path, 'r') as f:
            self.recipes = json.load(f)

    def _compute_craft_cost(self, recipe):
        cost = 0
        for item, quantity in recipe.items():
            cost += self.api_reader.search_buy_order_price(item) * quantity
        return cost
    
    def _compute_wait_time(self, recipe, type_of_wait):
        wait_time = 0
        for item, quantity in recipe.items():
            per_hour = self.api_reader.search_quick_status(item).get(f"{type_of_wait}MovingWeek", 0) / 168
            if per_hour: # ignores if a non-bazaar item is in a recipe
                wait_time += quantity / per_hour
        return wait_time

    def compute_profit(self, coins, no_expensive=False, no_negative=False):
        computed_results = []
        self.api_reader.update_response()
        if not self.api_reader.json_response:
            return computed_results
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        for item_to_be_crafted, recipe in self.recipes.items():
            cost_to_craft = self._compute_craft_cost(recipe)
            buy_wait_time = self._compute_wait_time(recipe, "sell")

            maximum_to_be_crafted = min(71680, int(coins / cost_to_craft))
            if no_expensive and not maximum_to_be_crafted:
                continue

            total_cost = cost_to_craft * maximum_to_be_crafted
            
            total_sell_price = self.api_reader.search_sell_offer_price(item_to_be_crafted) * maximum_to_be_crafted
            sell_wait_time = self._compute_wait_time(recipe, "buy")
            item_to_be_crafted = item_to_be_crafted.replace("_", " ").title()

            total_profit = total_sell_price-total_cost
            if no_negative and total_profit < 0:
                continue

            total_wait_time = buy_wait_time+sell_wait_time

            item_to_be_crafted = self._fix_string(item_to_be_crafted)
            fixed_total_cost = self._fix_float(total_cost)
            fixed_total_sell_price = self._fix_float(total_sell_price)
            fixed_total_profit = self._fix_float(total_profit)
            fixed_total_wait_time = self._fix_float(total_wait_time)

            to_be_appended = (item_to_be_crafted, fixed_total_cost, fixed_total_sell_price, fixed_total_profit, maximum_to_be_crafted, fixed_total_wait_time) 
            computed_results.append(to_be_appended)
        return computed_results

if __name__ == "__main__":
    # pd.set_option('display.max_rows', None)
    nda = NewDataAnalyzer()
    nda.link_read_search()
    df = nda.compute_profit(100_000_000)
    cleaner = NewDataCleaner()
    cleaned_df = cleaner.run_clean(df)
    print(cleaned_df)
    

    

    

    