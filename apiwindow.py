from tkinter import ttk
import tkinter as tk

class APIWindow(tk.Tk):
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

    def create_window(self):
        main_frame = tk.Frame(self) # Will hold everything
        content_frame = tk.Frame(main_frame) # Padding
        upper_frame = tk.Frame(content_frame, height=50)
        upper_left_frame = tk.Frame(upper_frame)
        upper_right_frame = tk.Frame(upper_frame)
        treeview_frame = tk.Frame(content_frame)

        # pack frames
        main_frame.pack()
        content_frame.pack(padx=20, pady=20)
        upper_frame.pack(side="top", fill="x")
        upper_left_frame.pack(side="left", fill="both", expand=True)
        upper_right_frame.pack(side="left", fill="both", expand=True)
        treeview_frame.pack(fill="both", expand=True)

        # create elements
        self.treeview = ttk.Treeview(treeview_frame, selectmode="browse")
        self.coin_input_box = ttk.Entry(upper_left_frame)
        
