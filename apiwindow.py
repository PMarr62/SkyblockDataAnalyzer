from tkinter import ttk
import tkinter as tk

from data_analyzer import DataAnalyzer
import pandas as pd
from typing import Callable

import webbrowser

"""
TODO:
*-------------
Current Issues:
- Entering any number throws:
  Cannot convert non-finite values (NA or inf) to integer
    - This might happen due to a failed api connection
- Closing the current search after immediately searching brings the user
  back to the table of the original search, no way to get back to the
  main table.
*-------------
"""

"""
active: entire df
inactive: none

ON_SEARCH:
if we are not in a search, swap the dataframes.
active is now inactive, and inactive is now vice versa.
we read inactive and find matches.
these matches are added to active and table is populated.

ON_EXIT:
swap active and inactive.
clearing inactive isn't necessary, but we can still do it.h.

TODO: Swaps fail from this above approach.
After searching again, the table does not modify itself.
Then, after leaving search, the true searched table shows, leaving us in the same state as before.


"""

"""


* Consider ensuring popups adhere to light/dark mode.
*** Disable search functionality while data is populating.
* Ensure program is runnable from main
* Remove/Rename Old/New Classes
* Remove files unneeded
* Rewrite README for release
* Update requirements.txt

* Structurally:
* Ensure classes are neat
* Ensure all classes are separated by its own file
* Ensure all classes and methods are documented
* Ensure un-needed methods are private
"""

class APIWindow(tk.Tk):
    COIN_INPUT_HINT = "Enter a coin value..."
    SEARCH_INPUT_HINT = "Enter an item name..."
    WINDOW_TITLE = "Skyblock Data Analyzer"
    WINDOW_SIZE = "800x300"

    ERROR_COIN_INPUT = "Please enter a valid integer!"
    INVALID_SEARCH_INPUT = "Please fetch prices before searching!"
    EXPORT_ERROR = "Please fetch prices before exporting!"

    TREEVIEW_BODY = "Treeview"
    ENTRY_STYLE = "TEntry"

    GITHUB_REPO_URL = "https://github.com/PMarr62/SkyblockDataAnalyzer"

    def __init__(self):
        super().__init__()
        self.title(APIWindow.WINDOW_TITLE)
        self.geometry(APIWindow.WINDOW_SIZE)

        # Widgets
        self.treeview: ttk.Treeview
        self.coin_input_box: ttk.Entry
        self.search_box: ttk.Entry

        # Buttons
        self.coin_input_btn: tk.Button
        self.search_btn: tk.Button
        self.exit_search_btn: tk.Button

        # Menu Bar
        self.menubar: tk.Menu

        # Text Tracking
        self.coin_input_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.active_is_light = True
        self._set_light_mode()

        # Window setup
        self._create_window()

    def start(self):
        self.mainloop()

    def setup_menu_bar(self, export_comm: Callable):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        file_menubar = tk.Menu(self.menubar, tearoff=0)
        view_menubar = tk.Menu(self.menubar, tearoff=0)
        help_menubar = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="File", menu=file_menubar)
        self.menubar.add_cascade(label="View", menu=view_menubar)
        self.menubar.add_cascade(label="Help", menu=help_menubar)

        set_theme = tk.Menu(view_menubar, tearoff=0)

        view_menubar.add_cascade(label="Set theme...", menu=set_theme)
        view_menubar.add_command(label="Reset column width", command=self._reset_col_width)

        set_theme.add_command(label="Light mode", command=self._set_light_mode)
        set_theme.add_command(label="Dark mode", command=self._set_dark_mode)
        
        file_menubar.add_command(label="Export data to csv...", command=export_comm)
        file_menubar.add_separator()
        file_menubar.add_command(label="Exit", command=self.destroy)

        help_menubar.add_command(label="Go to GitHub repository...", command=lambda:webbrowser.open(APIWindow.GITHUB_REPO_URL))

    def set_row_in_treeview(self, row: pd.Series) -> None:
        elements = list(row) #truncates index column
        self.treeview.insert("", "end", values=elements)
            
    def clear_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

    def create_popup(self, message):
        popup_window = tk.Toplevel(self)
        popup_window.title(APIWindow.WINDOW_TITLE)
        popup_window.transient(self)
        popup_window.grab_set()

        # get screen width/height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # define popup width/height
        popup_width = 300
        popup_height = 100
        # define coordinates given screen/popup width/height
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2

        popup_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}".format(screen_width, screen_height))

        popup_message = tk.Label(popup_window, text=message, wraplength=280, justify="left")
        popup_message.pack(padx=10, pady=10)

        close_button = ttk.Button(popup_window, text="OK", command=popup_window.destroy)
        close_button.pack(padx=10)

        self.wait_window(popup_window)

    def _reset_col_width(self):
        for col in DataAnalyzer.COL_NAMES:
            self.treeview.column(col, width=75, minwidth=50)

    def _set_light_mode(self):
        if not self.active_is_light:
            self._set_frames(self, "white")
            self._set_treeview("white", "black", "white")
            self._set_entries("white", "black")
            self._set_buttons("black", "white")
            self.active_is_light = True

    def _set_dark_mode(self):
        if self.active_is_light:
            self._set_frames(self, "gray10")
            self._set_treeview("gray10", "white", "gray10")
            self._set_entries("gray20", "white")
            self._set_buttons("white", "gray20")
            self.active_is_light = False

    def _set_frames(self, widget, bg_color):
        if isinstance(widget, tk.Frame):
            widget.configure(background=bg_color)
        for child in widget.winfo_children():
            self._set_frames(child, bg_color)

    def _set_treeview(self, fieldbg, fg, bg):
        self.style.configure(APIWindow.TREEVIEW_BODY, fieldbackground=fieldbg, foreground=fg, background=bg)

    def _set_entries(self, fieldbg, fg):
        self.style.configure(APIWindow.ENTRY_STYLE, fieldbackground=fieldbg, foreground=fg)

    def _set_buttons(self, fg, bg):
        # we have to set buttons individually (tk objects, not a ttk object)
        self.coin_input_btn.config(foreground=fg, background=bg)
        self.search_btn.config(foreground=fg, background=bg)
        self.exit_search_btn.config(foreground=fg, background=bg)

    def _entry_focus_in(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == hint:
            input_box.delete(0, tk.END)

    def _entry_focus_out(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == "":
            input_box.insert(0, hint)
        
    def _create_window(self):
        main_frame = tk.Frame(self) # Will hold everything
        content_frame = tk.Frame(main_frame, padx=50, pady=20) # Padding
        upper_frame = tk.Frame(content_frame, height=50)
        upper_left_frame = tk.Frame(upper_frame)
        upper_right_frame = tk.Frame(upper_frame)
        treeview_frame = tk.Frame(content_frame)

        # pack frames
        main_frame.pack(fill="both", expand=True)
        content_frame.pack(fill="both", expand=True)
        upper_frame.pack(side="top", fill="x")
        upper_left_frame.pack(side="left", fill="both", expand=True)
        upper_right_frame.pack(side="left", fill="both", expand=True)
        treeview_frame.pack(fill="both", expand=True)

        # create widgets
        self.treeview = ttk.Treeview(treeview_frame, selectmode="browse", style=APIWindow.TREEVIEW_BODY)
        self.coin_input_box = ttk.Entry(upper_left_frame, textvariable=self.coin_input_var, style=APIWindow.ENTRY_STYLE) 
        self.coin_input_btn = tk.Button(upper_left_frame, text="→")
        self.search_box = ttk.Entry(upper_right_frame, textvariable=self.search_var, style=APIWindow.ENTRY_STYLE)
        self.search_btn = tk.Button(upper_right_frame, text="→")
        self.exit_search_btn = tk.Button(upper_right_frame, text="X")

        # pack widgets
        self.coin_input_box.pack(side="left")
        self.coin_input_btn.pack(side="left")
        self.search_btn.pack(side="right")
        self.search_box.pack(side="right")
        self.treeview.pack(fill="both", expand=True)

        # setup event watches for text boxes
        self.coin_input_box.bind("<FocusIn>", lambda e: self._entry_focus_in(e, APIWindow.COIN_INPUT_HINT, self.coin_input_box))
        self.coin_input_box.bind("<FocusOut>", lambda e: self._entry_focus_out(e, APIWindow.COIN_INPUT_HINT, self.coin_input_box))
        self.search_box.bind("<FocusIn>", lambda e: self._entry_focus_in(e, APIWindow.SEARCH_INPUT_HINT, self.search_box))
        self.search_box.bind("<FocusOut>", lambda e: self._entry_focus_out(e, APIWindow.SEARCH_INPUT_HINT, self.search_box))

        # set default entry box text
        self.coin_input_var.set(APIWindow.COIN_INPUT_HINT)
        self.search_var.set(APIWindow.SEARCH_INPUT_HINT)

        # setup treeview
        self.treeview["columns"] = DataAnalyzer.COL_NAMES
        self.treeview["show"] = "headings"
        
        for col in DataAnalyzer.COL_NAMES:
            self.treeview.column(col, anchor="center", width=75, minwidth=50)
            self.treeview.heading(col, text=col)


if __name__ == "__main__":
    window = APIWindow()
    window.start()
        
