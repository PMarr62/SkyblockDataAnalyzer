from data_analyzer import DataAnalyzer
from tkinterwindow import DataAnalyzerWindow
from queue import Queue, Empty
from threading import Event, Thread

class DataAnalyzerController:
    def __init__(self):
        self.data_analyzer = DataAnalyzer()
        self.data_analyzer.read_recipe_json(r".resources\recipes.json")
        self.data_analyzer_window = DataAnalyzerWindow()
        self.data_analyzer_window.refresh_button.config(command=self.on_button_press)
        self.gui_queue = Queue()
        self.data_analyzer_window.root.bind("<<ProcessQueue>>", self.process_gui_queue)

    def start_window(self):
        self.data_analyzer_window.start()


    def on_button_press(self):
        coin_count: int
        try:
            coin_count = int(self.data_analyzer_window.coin_input_box.get())
            self.data_analyzer_window.clear_treeview()
            self.data_analyzer_window.refresh_button.config(state="disabled")
            results = self.data_analyzer.compute_profit(coin_count)
            for profit in results:
                self.gui_queue.put((self.data_analyzer_window.insert_into_treev, (profit, ), {}))
            self.data_analyzer_window.root.event_generate("<<ProcessQueue>>", when="tail")
            self.data_analyzer_window.refresh_button.config(state="normal")
        except ValueError:
            self.data_analyzer_window.create_popup()


    # def compute_profits(self):
    #     compute_thread = Thread(target=self._worker_thread, daemon=True)
    #     compute_thread.start()
    #     self.data_analyzer_window.loading_bar.stop()

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
    # dac.compute_profits()