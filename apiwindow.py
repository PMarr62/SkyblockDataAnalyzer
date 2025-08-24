from tkinter import ttk
import tkinter as tk

from data_analyzer import NewDataAnalyzer

"""
With a menubar, we can introduce options such as:
File -> Export data as csv, xlsx, etc.
View -> Set theme (light/dark), reset column width, etc.
"""

class APIWindow(tk.Tk):
    COIN_INPUT_HINT = "Enter a coin value..."
    SEARCH_INPUT_HINT = "Enter an item name..."
    def __init__(self):
        super().__init__()
        self.title = "Skyblock Data Analyzer"
        self.geometry("800x300")

        # Widgets
        self.treeview: ttk.Treeview
        self.coin_input_box: ttk.Entry
        self.search_box: ttk.Entry

        # Buttons
        self.coin_input_btn: tk.Button
        self.search_btn: tk.Button

        # Text Tracking
        self.coin_input_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.create_window()

    def start(self):
        self.mainloop()

    def entry_focus_in(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == hint:
            input_box.delete(0, tk.END)

    def entry_focus_out(self, event, hint: str, input_box: ttk.Entry):
        if input_box.get() == "":
            input_box.insert(0, hint)

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
            self.treeview.column(col, anchor="center", width=100, minwidth=50)
            self.treeview.heading(col, text=col)


if __name__ == "__main__":
    window = APIWindow()
    window.start()
        
