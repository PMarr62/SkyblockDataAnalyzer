from apireader import APIReader
import json

class DataAnalyzer:
    def __init__(self, coins=0):
        self.api_reader: APIReader = APIReader()
        self.coins: int = coins
        self.recipes: dict = {}

    def read_recipe_json(self, recipe_path):
        with open(recipe_path, 'r') as f:
            self.recipes = json.load(f)

    def buy_order(self):
        self.api_reader.update_response()
        api_results = self.api_reader.get_json_response()
        if not api_results:
            return ()
        # We should think of what kind of headers we may want to include in our final product table.
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        # Additionally, a window should be made when clicking on an item in the table.
        # It should redirect to more information regarding the product (such as what is required to craft it).
        pass

    def sell_offer(self):
        pass

    def print_results(self):
        pass

    

    

    