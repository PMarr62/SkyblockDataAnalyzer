"""
Class to be responsible for creating the GUI of Skyblock Data Analyzer.
Two screens are used: the main menu screen, and the flip screen.
"""

from tkinter import ttk
import tkinter as tk

class DataAnalyzerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skyblock Data Analyzer")
        self.root.geometry("600x300")

        # instance variables for the table, coin input, refresh, and loading bar for future reference
        self.treev: ttk.Treeview | None = None
        self.coin_input_box: ttk.Entry | None = None
        self.refresh_button: tk.Button | None = None
        self.loading_bar: ttk.Progressbar | None = None
        

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # self.frames["main"] = self.create_main_window(self.container)
        self.frames["flip"] = self.create_flip_window(self.container)

        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

        self.show_frame("flip")

    def show_frame(self, window_name: str):
        frame: tk.Frame = self.frames[window_name]
        frame.tkraise()

    def start(self):
        self.root.mainloop()
    
    def create_flip_window(self, parent):
        frame = tk.Frame(parent)

        top_bar = tk.Frame(frame)
        top_bar.pack(fill="x", padx=5, pady=5)

        # currently no capability, will be a refresh for API data
        # food for thought: the refresh button should be disabled when api data is loading.
        self.coin_input_box = ttk.Entry(top_bar, width=40)
        self.coin_input_box.pack(side="left", padx=5, pady=5)

        self.refresh_button = tk.Button(top_bar, text="→")
        self.refresh_button.pack(side="right", padx=5, pady=5)

        self.loading_bar = ttk.Progressbar(frame)
        self.loading_bar.pack(fill="x", padx=10, pady=5)

        self.treev = ttk.Treeview(frame, selectmode="browse")
        self.treev.pack(expand=True, fill="both")
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        self.treev["columns"] = ("1", "2", "3", "4", "5", "6")
        self.treev["show"] = "headings"

        self.treev.column("1", anchor="center", width=100)
        self.treev.column("2", anchor="se", width=100)
        self.treev.column("3", anchor="se", width=100)
        self.treev.column("4", anchor="se", width=100)
        self.treev.column("5", anchor="se", width=100)
        self.treev.column("6", anchor="se", width=100)

        self.treev.heading("1", text="Product Name")
        self.treev.heading("2", text="Total Buy Price")
        self.treev.heading("3", text="Total Sell Price")
        self.treev.heading("4", text="Profit")
        self.treev.heading("5", text="Quantity")
        self.treev.heading("6", text="Num. hours wait")
        return frame
    
    # methods to update treev and loading bar outside of this class (perhaps in a tkinter window / analyzer combinatory class)
    def insert_into_treev(self, compute_results) -> None:
        if self.treev and len(compute_results) == 6:
            self.treev.insert("", "end", values=tuple(compute_results))

    def update_loading_bar(self, set_to_value: float) -> None:
        if self.loading_bar:
            self.loading_bar.step(set_to_value)

# -- to be used at a later date:

    # def create_main_window(self, parent) -> tk.Frame:
    #     frame = tk.Frame(parent)
    
    #     label = tk.Label(frame, text="Welcome to Skyblock Data Analyzer!")
    #     label.pack(pady=20)

    #     button_frame = tk.Frame(frame)
    #     button_frame.pack(fill="y", padx=5, pady=5)
    #     craft_flip_button = tk.Button(button_frame, text="Craft Flips", command=lambda: self.show_frame("flip"))
    #     craft_flip_button.pack(side="left", padx=5)
        
    #     # This is additional functionality that will be added soon.
    #     single_flip_button = tk.Button(button_frame, text="Single Flips")
    #     single_flip_button.pack(side="left", padx=5)

    #     # button = tk.Button(frame, text="Go to flips", command=lambda: self.show_frame("flip"))
    #     # button.pack()

    #     return frame

if __name__ == "__main__":
    window = DataAnalyzerWindow()
    window.start()
