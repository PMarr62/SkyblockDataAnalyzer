from apireader import APIReader
import json

class DataAnalyzer:
    def __init__(self, coins=0):
        self.api_reader: APIReader = APIReader()
        self.coins: int = coins
        self.recipes: dict = {}
        self.computed_results = []

    def read_recipe_json(self, recipe_path):
        with open(recipe_path, 'r') as f:
            self.recipes = json.load(f)

    def _compute_craft_cost(self, recipe):
        cost = 0
        for item, quantity in recipe.items():
            cost += self.api_reader.search_buy_order_price(item) * quantity
        return cost
    
    def _compute_craft_wait_time(self, recipe):
        wait_time = 0
        for item, quantity in recipe.items():
            wait_time += (self.api_reader.search_quick_status(item).get("sellMovingWeek", 0) / 168) * quantity
        return wait_time

    def compute_profit(self):
        # What would we need to compute a profit?
        self.api_reader.update_response()
        if not self.api_reader.json_response:
            return
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        for item_to_be_crafted, recipe in self.recipes.items():
            cost_to_craft = self._compute_craft_cost(recipe)
            buy_wait_time = self._compute_craft_wait_time(recipe)
            maximum_to_be_crafted = min(71680, int(self.coins / cost_to_craft))
            total_cost = cost_to_craft * maximum_to_be_crafted
            # =======
            total_sell_price = self.api_reader.search_sell_offer_price(item_to_be_crafted) * maximum_to_be_crafted
            sell_wait_time = (self.api_reader.search_quick_status(item_to_be_crafted).get("buyMovingWeek", 0) / 168) * maximum_to_be_crafted
            self.computed_results.append((item_to_be_crafted, total_cost, total_sell_price, total_sell_price-total_cost, maximum_to_be_crafted, buy_wait_time+sell_wait_time))

    

    

    