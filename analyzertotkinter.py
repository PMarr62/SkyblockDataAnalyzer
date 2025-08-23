from data_analyzer import DataAnalyzer
from tkinterwindow import DataAnalyzerWindow
from queue import Queue, Empty
from threading import Event, Thread

class DataAnalyzerController:
    def __init__(self):
        self.data_analyzer = DataAnalyzer()
        self.data_analyzer.read_recipe_json(r"resources\recipes.json")
        self.data_analyzer_window = DataAnalyzerWindow()
        self.data_analyzer_window.send_to_calculate_button.config(command=self.on_send_press)
        self.gui_queue = Queue()
        self.data_analyzer_window.root.bind("<<ProcessQueue>>", self.process_gui_queue)

    # features to add:
    # checkbox that ignores items that cannot be bought
    # checkbox that ignores negative profit
    # sorting by column on click

    def start_window(self):
        self.data_analyzer_window.start()

    def load_results_in_treeview(self, results):
        for profit in results:
            self.gui_queue.put((self.data_analyzer_window.insert_into_treev, (profit, ), {}))
        self.data_analyzer_window.root.event_generate("<<ProcessQueue>>", when="tail")


    def on_send_press(self):
        coin_count: int
        try:
            coin_count = int(self.data_analyzer_window.coin_input_box.get())
            self.data_analyzer_window.clear_treeview()
            self.data_analyzer_window.send_to_calculate_button.config(state="disabled")
            # get checkbox info
            ignore_expensive = self.data_analyzer_window.ignore_expensive_var.get()
            ignore_negative = self.data_analyzer_window.ignore_negative_var.get()
            results = self.data_analyzer.compute_profit(coin_count, ignore_expensive, ignore_negative)
            self.load_results_in_treeview(results)
            self.data_analyzer_window.send_to_calculate_button.config(state="normal")
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