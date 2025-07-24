from apireader import APIReader

class DataAnalyzer:
    def __init__(self, coins=0):
        self.api_reader = APIReader()
        self.coins = coins

    