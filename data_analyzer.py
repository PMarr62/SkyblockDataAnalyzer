from apireader import APIReader
import json

class DataAnalyzer:
    def __init__(self, coins=0):
        self.api_reader: APIReader = APIReader()
        self.coins: int = coins
        self.recipes: dict = {}
        
    def _fix_string(self, item_id: str):
        return item_id.replace("_", " ").title()

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

    def compute_profit(self):
        computed_results = []
        self.api_reader.update_response()
        if not self.api_reader.json_response:
            return computed_results
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        for item_to_be_crafted, recipe in self.recipes.items():

            cost_to_craft = self._compute_craft_cost(recipe)
            buy_wait_time = self._compute_wait_time(recipe, "sell")

            maximum_to_be_crafted = min(71680, int(self.coins / cost_to_craft))
            total_cost = cost_to_craft * maximum_to_be_crafted
            
            total_sell_price = self.api_reader.search_sell_offer_price(item_to_be_crafted) * maximum_to_be_crafted
            sell_wait_time = self._compute_wait_time(recipe, "buy")
            item_to_be_crafted = item_to_be_crafted.replace("_", " ").title()

            total_profit = total_sell_price-total_cost
            total_wait_time = buy_wait_time+sell_wait_time

            item_to_be_crafted = self._fix_string(item_to_be_crafted)

            round(total_cost)
            round(total_sell_price)
            round(total_profit)
            round(total_wait_time, 2)

            to_be_appended = (item_to_be_crafted, total_cost, total_sell_price, total_profit, maximum_to_be_crafted, total_wait_time) 
            computed_results.append(to_be_appended)
        return computed_results

if __name__ == "__main__":
    da = DataAnalyzer(100000000)
    da.read_recipe_json(r".resources\recipes.json")
    da.compute_profit()

    

    

    