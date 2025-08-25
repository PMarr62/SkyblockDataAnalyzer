"""
This is the main file for SkyblockDataAnalyzer.
"""

from apireader import APIReader
from apisearcher import APISearcher
from apiwindow import APIWindow
from data_analyzer import DataAnalyzer
from datacleaner import DataCleaner
from data_analyzer_controller import DataAnalyzerController

def main():
    # creating necessary objects
    api_reader = APIReader()
    api_searcher = APISearcher(api_reader)
    api_window = APIWindow()

    data_analyzer = DataAnalyzer(api_searcher)
    data_cleaner = DataCleaner()

    data_analyzer_controller = DataAnalyzerController(data_cleaner, data_analyzer, api_window)

    # pre-methods
    status_code = api_reader.update_response()

    data_analyzer_controller.start()
    

if __name__ == "__main__":
    main()

