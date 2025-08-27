from apiwindow import APIWindow
from data_analyzer import DataAnalyzer
from datacleaner import DataCleaner

from tkinter.filedialog import asksaveasfilename
from threading import Event, Thread

import pandas as pd
from typing import Callable
from thefuzz import process

class DataAnalyzerController:

    def __init__(self, data_cleaner: DataCleaner, data_analyzer: DataAnalyzer, window: APIWindow):
        self.data_cleaner = data_cleaner
        self.data_analyzer = data_analyzer
        self.window = window

        # we swap active and inactive when we search, saving time when we exit a search.
        self.active_df = pd.DataFrame()
        self.inactive_df = pd.DataFrame()
        self.sort_bool = False
        self.is_searching = False

        # command configs to tkinter widgets
        self.window.coin_input_btn.config(command=lambda: self._button_threading(self._on_coin_input_btn))
        self.window.search_btn.config(command=lambda: self._button_threading(self._on_search_btn))
        self.window.exit_search_btn.config(command=lambda: self._button_threading(self._on_exit_search_btn))
        self.window.treeview.bind("<Button-1>", self._on_treeview_click)

        # monitors when boxes are typed into (dealing with placeholder text)
        self.window.coin_input_box.bind("<Key>", lambda e: self._on_type_box(e, APIWindow.COIN_INPUT_VAR, self._on_coin_input_btn))
        self.window.search_box.bind("<Key>", lambda e: self._on_type_box(e, APIWindow.SEARCH_VAR, self._on_search_btn))

    def start(self):
        # we setup the menubar outside of apiwindow since we need dataframe data to export.
        # otherwise we would have to circular import apiwindow and self
        self.window.setup_menu_bar(self._export_dataframe)
        self.window.start()

    def _on_type_box(self, event, entry_var: str, search_func: Callable):
        if event.keysym == "Return":
            search_func()
            return
        check_len = len(getattr(self.window, entry_var).get())
        setattr(self.window, APIWindow.VAR_BOOL_MAPPING[entry_var], check_len > 0)

    def _on_coin_input_btn(self):
        # get coin count.
        coin_count: int
        try:
            # We should force exit search before querying API.
            self._on_exit_before_clear()
            self._disable_while_querying()
            coin_count = int(self.window.coin_input_var.get())
            self.window.clear_treeview()
            result_df = self.data_analyzer.compute_profit(coin_count)
            self.active_df = self.data_cleaner.run_clean(result_df)
            self._populate_treeview(self.active_df)
        except ValueError as e:
            self.window.create_popup(self.window.ERROR_COIN_INPUT)
        finally:
            self._enable_after_querying()

    def _disable_while_querying(self):
        self.window.treeview.configure(displaycolumns=()) # hide columns
        self.window.coin_input_btn.config(state="disabled")
        self.window.coin_input_box.state(["readonly"])

        self.window.search_btn.config(state="disabled")
        self.window.search_box.state(["readonly"])

    def _enable_after_querying(self):
        self.window.coin_input_btn.config(state="normal")
        self.window.coin_input_box.state(["!readonly"])

        self.window.search_btn.config(state="normal")
        self.window.search_box.state(["!readonly"])
        self.window.treeview.configure(displaycolumns=DataAnalyzer.COL_NAMES) #show columns

    def _on_search_btn(self):
        if self.active_df.empty and not self.is_searching:
            self.window.create_popup(self.window.INVALID_SEARCH_INPUT)
            return
        search_query = self.window.search_var.get()
        blank_search = len(search_query.strip()) == 0
        have_not_typed = search_query == APIWindow.SEARCH_INPUT_HINT and not self.window.search_var_has_typed
        if blank_search or have_not_typed:
            self.window.create_popup(self.window.SPACES_IN_SEARCH_INPUT)
            return
        if not self.is_searching:
            self.is_searching = True
            self._swap_dataframes() # swaps active and inactive
        threshold_match = 80 # match to return a row
        choices = self.inactive_df['Item Name']
        matches = process.extract(search_query, choices, limit=len(choices))
        # without this check, timing errors cause two buttons to periodically appear.
        if not self.window.exit_search_btn_is_packed:
            self.window.exit_search_btn_is_packed = True # update tracking variable
            self.window.exit_search_btn.pack(side="right")
        to_show = []
        for match in matches:
            if match[1] >= threshold_match:
                # appends the row index stored at match[2]
                to_show.append(self.inactive_df.loc[match[2]])
        self.active_df = pd.DataFrame(to_show, columns=DataAnalyzer.COL_NAMES)
        self.window.clear_treeview()
        self._populate_treeview(self.active_df)

    def _on_exit_before_clear(self):
        self.is_searching = False # exits search
        self.window.exit_search_btn_is_packed = False # reset exit button tracking variable
        self.window.search_var_has_typed = False # resets typing from search
        self.window.exit_search_btn.forget()
        self.window.treeview.focus_set() # focus away from search bar
        self.window.search_var.set(APIWindow.SEARCH_INPUT_HINT) # reset search bar
        
    def _on_exit_search_btn(self):
        self._disable_while_querying()
        self._on_exit_before_clear()
        self.window.clear_treeview()
        self._swap_dataframes()
        self._populate_treeview(self.active_df)
        self._enable_after_querying()

    def _on_treeview_click(self, event):
        clicked_region = self.window.treeview.identify_region(event.x, event.y)
        # the second check ensures columns arent sorted while data is still populating
        if clicked_region == "heading" and self.window.coin_input_btn["state"] == "normal" and not self.active_df.empty:
            clicked_col = self.window.treeview.identify_column(event.x)
            col_name = self._get_column_name(clicked_col)
            # we have the column name, now sort active 
            # we have the potential of sorting strings, ints, or floats.

            # treat columns as int/float, sort, transform back into strings
            if col_name in DataCleaner.FLOAT_COLS:
                self.active_df[col_name] = self.active_df[col_name].str.replace(",", "").str.replace("%", "").astype(float)
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)
                self.active_df = self.data_cleaner.format_float_column(col_name, self.active_df)
            elif col_name in DataCleaner.INT_COLS:
                self.active_df[col_name] = self.active_df[col_name].str.replace(",", "").astype(int)
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)
                self.active_df = self.data_cleaner.format_int_column(col_name, self.active_df)
            else:
                self.active_df = self.active_df.sort_values(col_name, ascending=self.sort_bool)

            self.sort_bool = not self.sort_bool
            self.window.clear_treeview()
            self._populate_treeview(self.active_df)

    def _button_threading(self, work_func: Callable):
        thread = Thread(target=work_func)
        thread.start()

    def _export_dataframe(self):
        try:
            if self.active_df.empty:
                self.window.create_popup(APIWindow.EXPORT_ERROR)
            else:
                path_to_save = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="sda_data.csv")
                self.active_df.to_csv(path_to_save, index=False)
                confirm_message = f"Export saved to {path_to_save}."
                self.window.create_popup(confirm_message)
        except FileNotFoundError:
            # This would only happen with a dialog popup if the user cancels.
            # We can safely ignore this.
            return

    def _populate_treeview(self, dataframe: pd.DataFrame):
        for _, row in dataframe.iterrows():
            self.window.set_row_in_treeview(row)

    def _swap_dataframes(self):
        # swaps the active and inactive dataframes
        self.active_df, self.inactive_df = self.inactive_df, self.active_df

    def _get_column_name(self, clicked_col) -> str:
        # turns a "#n" into the respective column name
        col_index = int(clicked_col.replace("#", "")) - 1
        return DataAnalyzer.COL_NAMES[col_index]