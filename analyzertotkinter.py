from data_analyzer import DataAnalyzer
from tkinterwindow import DataAnalyzerWindow
from tkinter.filedialog import asksaveasfilename
from queue import Queue, Empty
from threading import Event, Thread

from resources.newrecipes import CRAFTING_RECIPES
from apiwindow import APIWindow
from data_analyzer import NewDataAnalyzer, NewDataCleaner
import pandas as pd
import numpy as np
from typing import Callable
from thefuzz import process

class NewDataAnalyzerController:
    def __init__(self):
        self.data_analyzer = NewDataAnalyzer()
        self.data_cleaner = NewDataCleaner()
        self.data_analyzer.link_read_search() # updates api and allows for search
        self.window = APIWindow()
        # main dataframe, and a subset of df known as search_df

        self.active_df = pd.DataFrame()
        self.inactive_df = pd.DataFrame()
        self.sort_bool = False

        # self.df: pd.DataFrame
        # self.search_df: pd.DataFrame

        self.window.coin_input_btn.config(command=lambda: self._button_threading(self._on_coin_input_btn))
        self.window.search_btn.config(command=lambda: self._button_threading(self._on_search_btn))
        self.window.exit_search_btn.config(command=lambda: self._button_threading(self._on_exit_search_btn))
        self.window.treeview.bind("<Button-1>", self._on_treeview_click)

    def start(self):
        self.window.setup_menu_bar(self.export_dataframe)
        self.window.start()

    def export_dataframe(self):
        if self.active_df.empty:
            self.window.create_popup(APIWindow.EXPORT_ERROR)
        else:
            path_to_save = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="sda_data.csv")
            self.active_df.to_csv(path_to_save, index=False)
            confirm_message = f"Export saved to {path_to_save}."
            self.window.create_popup(confirm_message)

    def populate_treeview(self, dataframe: pd.DataFrame):
        for _, row in dataframe.iterrows():
            self.window.set_row_in_treeview(row)

    def _swap_dataframes(self):
        # swaps the active and inactive dataframes
        self.active_df, self.inactive_df = self.inactive_df, self.active_df

    def _button_threading(self, work_func: Callable):
        thread = Thread(target=work_func)
        thread.start()

    def _on_coin_input_btn(self):
        # get coin count.
        coin_count: int
        try:
            coin_count = int(self.window.coin_input_var.get())    
            self.window.clear_treeview()
            self.window.coin_input_btn.config(state="disabled")
            result_df = self.data_analyzer.compute_profit(coin_count)
            self.active_df = self.data_cleaner.run_clean(result_df)
            self.populate_treeview(self.active_df)
            self.window.coin_input_btn.config(state="normal")
        except ValueError:
            self.window.create_popup(self.window.ERROR_COIN_INPUT)

    def _on_search_btn(self):
        try:
            search_query = self.window.search_var.get()
            threshold_match = 80 # match to return a row
            choices = self.active_df['Item Name']
            matches = process.extract(search_query, choices, limit=len(choices))
            self.window.exit_search_btn.pack(side="right") #enables exit button
            to_show = []
            for match in matches:
                if match[1] >= threshold_match:
                    # appends the row at index match[2]
                    to_show.append(self.active_df.loc[match[2]])
            self.inactive_df = pd.DataFrame(to_show, columns=NewDataAnalyzer.COL_NAMES)
            self.window.clear_treeview()
            self._swap_dataframes()
            self.populate_treeview(self.active_df)
        except AttributeError:
            self.window.create_popup(self.window.INVALID_SEARCH_INPUT)

    def get_column_name(self, clicked_col) -> str:
        # turns a "#n" into the respective column name
        col_index = int(clicked_col.replace("#", "")) - 1
        return NewDataAnalyzer.COL_NAMES[col_index]



    def _on_treeview_click(self, event):
        clicked_region = self.window.treeview.identify_region(event.x, event.y)
        # the second check ensures columns arent sorted while data is still populating
        if clicked_region == "heading" and self.window.coin_input_btn["state"] == "normal" and not self.active_df.empty:
            clicked_col = self.window.treeview.identify_column(event.x)
            col_name = self.get_column_name(clicked_col)
            # we have the column name, now sort active 
            # we have the potential of sorting strings, ints, or floats.

            # treat columns as int/float, sort, transform back into strings
            if col_name in NewDataCleaner.FLOAT_COLS:
                self.active_df[col_name] = self.active_df[col_name].str.replace(",", "").astype(float)
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)
                self.active_df = self.data_cleaner.format_float_column(col_name, self.active_df)
            elif col_name in NewDataCleaner.INT_COLS:
                self.active_df[col_name] = self.active_df[col_name].str.replace(",", "").astype(int)
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)
                self.active_df = self.data_cleaner.format_int_column(col_name, self.active_df)
            else:
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)

            self.sort_bool = not self.sort_bool
            self.window.clear_treeview()
            self.populate_treeview(self.active_df)

        

    def _on_exit_search_btn(self):
        self.window.exit_search_btn.forget()
        self.window.treeview.focus_set() # focus away from search bar
        self.window.search_var.set(APIWindow.SEARCH_INPUT_HINT) # reset search bar
        self.window.clear_treeview()
        self._swap_dataframes()
        self.populate_treeview(self.active_df)
        

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
    dac = NewDataAnalyzerController()
    dac.start()
    # dac.compute_profits()