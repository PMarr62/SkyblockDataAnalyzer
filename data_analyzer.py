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
        pass

    def sell_offer(self):
        pass

    def print_results(self):
        pass

    

    

    