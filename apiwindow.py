from tkinter import ttk
import tkinter as tk

from data_analyzer import NewDataAnalyzer
import pandas as pd

"""
With a menubar, we can introduce options such as:
File -> Export data as csv, xlsx, etc.
View -> Set theme (light/dark), reset column width, etc.

todo:
1) Add sorting functionality by column click (or in menubar)
2) Add functionality to exporting data and setting a theme, resetting column
3) Add a help function that goes to a to-be FAQ on github.

"""

class APIWindow(tk.Tk):
    COIN_INPUT_HINT = "Enter a coin value..."
    SEARCH_INPUT_HINT = "Enter an item name..."
    WINDOW_TITLE = "Skyblock Data Analyzer"
    WINDOW_SIZE = "800x300"

    ERROR_COIN_INPUT = "Please enter a valid integer!"
    INVALID_SEARCH_INPUT = "Please fetch prices before searching!"

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

        # Window setup
        self.create_window()

    def start(self):
        self.mainloop()

    def entry_focus_in(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == hint:
            input_box.delete(0, tk.END)

    def entry_focus_out(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == "":
            input_box.insert(0, hint)

    def set_row_in_treeview(self, row: pd.Series):
        elements = list(row)[1:] #truncates index column
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

        popup_message = tk.Label(popup_window, text=message)
        popup_message.pack(padx=10, pady=10)

        close_button = ttk.Button(popup_window, text="OK", command=popup_window.destroy)
        close_button.pack(padx=10)

        self.wait_window(popup_window)
        

    def create_window(self):
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
        self.treeview = ttk.Treeview(treeview_frame, selectmode="browse")
        self.coin_input_box = ttk.Entry(upper_left_frame, textvariable=self.coin_input_var) 
        self.coin_input_btn = tk.Button(upper_left_frame, text="→")
        self.search_box = ttk.Entry(upper_right_frame, textvariable=self.search_var)
        self.search_btn = tk.Button(upper_right_frame, text="→")
        self.exit_search_btn = tk.Button(upper_right_frame, text="X")

        # pack widgets
        self.coin_input_box.pack(side="left")
        self.coin_input_btn.pack(side="left")
        self.search_btn.pack(side="right")
        self.search_box.pack(side="right")
        self.treeview.pack(fill="both", expand=True)

        # setup event watches for text boxes
        self.coin_input_box.bind("<FocusIn>", lambda e: self.entry_focus_in(e, APIWindow.COIN_INPUT_HINT, self.coin_input_box))
        self.coin_input_box.bind("<FocusOut>", lambda e: self.entry_focus_out(e, APIWindow.COIN_INPUT_HINT, self.coin_input_box))
        self.search_box.bind("<FocusIn>", lambda e: self.entry_focus_in(e, APIWindow.SEARCH_INPUT_HINT, self.search_box))
        self.search_box.bind("<FocusOut>", lambda e: self.entry_focus_out(e, APIWindow.SEARCH_INPUT_HINT, self.search_box))

        # set default entry box text
        self.coin_input_var.set(APIWindow.COIN_INPUT_HINT)
        self.search_var.set(APIWindow.SEARCH_INPUT_HINT)

        # setup treeview
        self.treeview["columns"] = NewDataAnalyzer.COL_NAMES
        self.treeview["show"] = "headings"
        
        for col in NewDataAnalyzer.COL_NAMES:
            self.treeview.column(col, anchor="center", width=75, minwidth=50)
            self.treeview.heading(col, text=col)

        # setup menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        file_menubar = tk.Menu(self.menubar, tearoff=False)
        view_menubar = tk.Menu(self.menubar, tearoff=False)

        self.menubar.add_cascade(label="File", menu=file_menubar,)
        self.menubar.add_cascade(label="View", menu=view_menubar)

        file_menubar.add_command(label="Export data as...")
        file_menubar.add_separator()
        file_menubar.add_command(label="Exit", command=self.destroy)

        view_menubar.add_command(label="Set theme...")
        view_menubar.add_command(label="Reset column width")


if __name__ == "__main__":
    window = APIWindow()
    window.start()
        
