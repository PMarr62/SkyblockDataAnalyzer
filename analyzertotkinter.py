from data_analyzer import DataAnalyzer
from tkinterwindow import DataAnalyzerWindow
from queue import Queue, Empty
from threading import Event, Thread

class DataAnalyzerController:
    def __init__(self):
        self.data_analyzer = DataAnalyzer(100000000)
        self.data_analyzer.read_recipe_json(r".resources\recipes.json")
        self.data_analyzer_window = DataAnalyzerWindow()
        self.gui_queue = Queue()
        self.data_analyzer_window.root.bind("<<ProcessQueue>>", self.process_gui_queue)

    def start_window(self):
        self.data_analyzer_window.root.after(100, self.compute_profits)
        self.data_analyzer_window.start()

    def _worker_thread(self):
        results = self.data_analyzer.compute_profit()
        for profit in results:
            self.gui_queue.put((self.data_analyzer_window.insert_into_treev, (profit, ), {}))
        self.data_analyzer_window.root.event_generate("<<ProcessQueue>>", when="tail")

    def compute_profits(self):
        compute_thread = Thread(target=self._worker_thread, daemon=True)
        compute_thread.start()

    def process_gui_queue(self, event):
        try:
            while True:
                function, args, kwargs = self.gui_queue.get_nowait()
                function(*args, **kwargs)
        except Empty:
            pass

if __name__ == "__main__":
    dac = DataAnalyzerController()
    dac.start_window()
    dac.compute_profits()