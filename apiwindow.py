"""
File Name: apiwindow.py

Class to display the interactive window on-screen. Note that much of the functionality,
such as button clicks, event watching, etc. is handled by the Data Analyzer Controller
class, which works in conjunction with the Data Analyzer class.
"""

from tkinter import ttk
import tkinter as tk

from data_analyzer import DataAnalyzer
import pandas as pd
from typing import Callable

import webbrowser

class APIWindow(tk.Tk):
    COIN_INPUT_HINT = "Enter a coin value..."
    SEARCH_INPUT_HINT = "Enter an item name..."
    WINDOW_TITLE = "Skyblock Data Analyzer"
    WINDOW_SIZE = "800x300"

    ERROR_COIN_INPUT = "Please enter a valid integer!"
    INVALID_SEARCH_INPUT = "Please fetch prices before searching!"
    SPACES_IN_SEARCH_INPUT = "Please enter a non-blank input when searching!"
    EXPORT_ERROR = "Please fetch prices before exporting!"

    TREEVIEW_BODY = "Treeview"
    TREEVIEW_HEADER = "Treeview.Heading"
    ENTRY_STYLE = "TEntry"

    COIN_INPUT_VAR = "coin_input_var"
    SEARCH_VAR = "search_var"

    VAR_BOOL_MAPPING = {
        COIN_INPUT_VAR: "coin_input_var_has_typed",
        SEARCH_VAR: "search_var_has_typed"
    }
    VAR_HINT_MAPPING = {
        COIN_INPUT_VAR: COIN_INPUT_HINT,
        SEARCH_VAR: SEARCH_INPUT_HINT
    }

    LIGHT_MODE_STYLING = {
        "FG": "black",
        "BG": "white"
    }

    DARK_MODE_STYLING = {
        "FG": "white",
        "BG": "gray10"
    }

    GITHUB_REPO_URL = "https://github.com/PMarr62/SkyblockDataAnalyzer/blob/main/FAQ.md"

    def __init__(self):
        super().__init__()
        self.title(APIWindow.WINDOW_TITLE)
        self.geometry(APIWindow.WINDOW_SIZE)

        # Widgets
        self.treeview: ttk.Treeview
        self.coin_input_box: ttk.Entry
        self.search_box: ttk.Entry

        self.coin_input_btn: tk.Button
        self.search_btn: tk.Button
        self.exit_search_btn: tk.Button

        # race conditions can occur with disappearing elements, this stops it
        self.exit_search_btn_is_packed = False

        # Menu Bar
        self.menubar: tk.Menu

        # Text Tracking
        self.coin_input_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Used to track if a user has a typed value in an entry
        self.coin_input_var_has_typed = False
        self.search_var_has_typed = False

        # Responsible for popup details
        self.popup: tk.Toplevel
        self.popup_label: tk.Label
        self.popup_close: tk.Button

        # Window setup
        self._create_window()

        # Styling
        self.style = ttk.Style()
        self.style.theme_use("alt")

        # Enable light theme 
        self.active_is_light = False
        self._set_light_mode()
        self.active_is_light = True

    # run app
    def start(self):
        self.mainloop()

    # sets up context bar (File, View, Help)
    def setup_menu_bar(self, export_comm: Callable):
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)

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
        
        file_menubar.add_command(label="Export data to .csv...", command=export_comm)
        file_menubar.add_separator()
        file_menubar.add_command(label="Exit", command=self.destroy)

        help_menubar.add_command(label="Go to GitHub FAQ...", command=lambda:webbrowser.open(APIWindow.GITHUB_REPO_URL))

    # Adds a row to the treeview table
    def set_row_in_treeview(self, row: pd.Series):
        elements = list(row) #truncates index column
        self.treeview.insert("", "end", values=elements)
            
    # Clears the treeview table
    def clear_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

    # Creates a popup with a given message
    def create_popup(self, message: str):
        self.popup = tk.Toplevel(self)
        self.popup.title(APIWindow.WINDOW_TITLE)
        self.popup.transient(self)
        self.popup.grab_set()
        self._set_popup_geometry()

        self.popup_label = tk.Label(self.popup, text=message, wraplength=280, justify="left")
        self.popup_label.pack(padx=10, pady=10)

        self.popup_close = tk.Button(self.popup, text="OK", width=10, command=self.popup.destroy)
        self.popup_close.pack(padx=10)

        style_sheet = self._get_style_sheet()
        self._set_popup(style_sheet["FG"], style_sheet["BG"])

        self.wait_window(self.popup)

    # Defines the coordinates on-screen where a popup will occur
    def _set_popup_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        popup_width = 300
        popup_height = 100
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2
        self.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}".format(screen_width, screen_height))

    # Resets the treeview's column width if users changed it
    def _reset_col_width(self):
        for col in DataAnalyzer.COL_NAMES:
            self.treeview.column(col, width=75, minwidth=50)

    # Gets the current theme's corresponding style sheet
    def _get_style_sheet(self) -> dict:
        if self.active_is_light:
            return APIWindow.LIGHT_MODE_STYLING
        return APIWindow.DARK_MODE_STYLING

    # Sets a theme from the passed style sheet
    def _set_theme(self, style_sheet: dict):
        fg = style_sheet["FG"]
        bg = style_sheet["BG"]
        self._set_frames(self, bg)
        self._set_treeview(fg, bg)
        self._set_entries(fg, bg)
        self._set_buttons(fg, bg)

    # Sets light mode for the app
    def _set_light_mode(self):
        if not self.active_is_light:
            self._set_theme(APIWindow.LIGHT_MODE_STYLING)
            self.active_is_light = True

    # Sets dark mode for the app
    def _set_dark_mode(self):
        if self.active_is_light:
            self._set_theme(APIWindow.DARK_MODE_STYLING)
            self.active_is_light = False

    # Changes the color of all frames in the app
    def _set_frames(self, widget, bg_color: str):
        if isinstance(widget, tk.Frame):
            widget.configure(background=bg_color)
        for child in widget.winfo_children():
            self._set_frames(child, bg_color)

    # Changes the color of the treeview in the app
    def _set_treeview(self, fg: str, bg: str):
        self.style.configure(APIWindow.TREEVIEW_BODY, fieldbackground=bg, foreground=fg, background=bg)
        self.style.configure(APIWindow.TREEVIEW_HEADER, foreground=fg, background=bg)

    # Changes the color of the entry text boxes in the app
    def _set_entries(self, fg: str, bg: str):
        self.style.configure(APIWindow.ENTRY_STYLE, fieldbackground=bg, foreground=fg)

    # Changes the color of all buttons in the app
    def _set_buttons(self, fg: str, bg: str):
        # we have to set buttons individually (tk objects, not a ttk object)
        self.coin_input_btn.configure(foreground=fg, background=bg)
        self.search_btn.configure(foreground=fg, background=bg)
        self.exit_search_btn.configure(foreground=fg, background=bg)

    # Changes the color of any incoming popups to be displayed
    def _set_popup(self, fg: str, bg: str):
        # we have to set the frame background, text, and buttons
        self.popup.configure(background=bg)
        self.popup_label.configure(foreground=fg, background=bg)
        self.popup_close.configure(foreground=fg, activeforeground=fg, background=bg, activebackground=bg)

    # Event to watch when a text box is clicked into
    def _entry_focus_in(self, event: tk.Event, entry_var: str):
        matches_hint = getattr(self, entry_var).get() == APIWindow.VAR_HINT_MAPPING[entry_var]
        has_typed = getattr(self, APIWindow.VAR_BOOL_MAPPING[entry_var])
        if matches_hint and not has_typed:
            getattr(self, entry_var).set("")

    # Event to watch when a text box is clicked out of
    def _entry_focus_out(self, event: tk.Event, entry_var: str):
        var = getattr(self, entry_var)
        if var.get() == "":
            var.set(APIWindow.VAR_HINT_MAPPING[entry_var])
            setattr(self, APIWindow.VAR_BOOL_MAPPING[entry_var], False)

    # Creates a tkinter button
    def _create_button(self, frame: tk.Frame, symbol: str) -> tk.Button:
        return tk.Button(frame, text=symbol, width=2, height=1)
    
    # Creates a tkinter entry
    def _create_entry(self, frame: tk.Frame, text_var: tk.StringVar) -> ttk.Entry:
        return ttk.Entry(frame, textvariable=text_var, style=APIWindow.ENTRY_STYLE)
    
    # Creates all necessary widgets for app functionality
    def _create_widgets(self, treeview_frame: tk.Frame, coin_input_frame: tk.Frame, search_frame: tk.Frame):
        # step 1: define widgets used
        self.treeview = ttk.Treeview(treeview_frame, selectmode="browse", style=APIWindow.TREEVIEW_BODY)
        self.coin_input_box = self._create_entry(coin_input_frame, self.coin_input_var) 
        self.coin_input_btn = self._create_button(coin_input_frame, "→")
        self.search_box = self._create_entry(search_frame, self.search_var)
        self.search_btn = self._create_button(search_frame, "→")
        self.exit_search_btn = self._create_button(search_frame, "X")
        
        # step 2: define stringvars for text boxes
        self.coin_input_var.set(APIWindow.COIN_INPUT_HINT)
        self.search_var.set(APIWindow.SEARCH_INPUT_HINT)

        # step 3: pack widgets
        self.coin_input_box.pack(side="left")
        self.coin_input_btn.pack(side="left")
        self.search_btn.pack(side="right")
        self.search_box.pack(side="right")
        self.treeview.pack(fill="both", expand=True)

    # Binds all necessary events to search boxes
    def _bind_events(self):
        self.coin_input_box.bind("<FocusIn>", lambda e: self._entry_focus_in(e, APIWindow.COIN_INPUT_VAR))
        self.coin_input_box.bind("<FocusOut>", lambda e: self._entry_focus_out(e, APIWindow.COIN_INPUT_VAR))
        self.search_box.bind("<FocusIn>", lambda e: self._entry_focus_in(e, APIWindow.SEARCH_VAR))
        self.search_box.bind("<FocusOut>", lambda e: self._entry_focus_out(e, APIWindow.SEARCH_VAR))

    # Sets up the treeview table
    def _setup_treeview(self):
        self.treeview["columns"] = DataAnalyzer.COL_NAMES
        self.treeview["show"] = "headings"
        
        for col in DataAnalyzer.COL_NAMES:
            self.treeview.column(col, anchor="center", width=60, minwidth=40)
            self.treeview.heading(col, text=col)
        
    # Creates the application window
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

        # create and pack widgets
        self._create_widgets(treeview_frame, upper_left_frame, upper_right_frame)

        # setup event watches for text boxes
        self._bind_events()

        # setup treeview
        self._setup_treeview()
