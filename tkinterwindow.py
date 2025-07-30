"""
Class to be responsible for creating the GUI of Skyblock Data Analyzer.
Two screens are used: the main menu screen, and the flip screen.
"""

from tkinter import ttk
import tkinter as tk

class DataAnalyzerWindow:
    COLUMN_NAMES = ["Product Name", "Total Buy Price", "Total Sell Price", "Profit", "Quantity", "Num. hours wait"]
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skyblock Data Analyzer")
        self.root.geometry("600x300")

        # instance variables  for future reference
        self.treev: ttk.Treeview
        self.coin_input_box: ttk.Entry
        self.send_to_calculate_button: tk.Button
        # self.loading_bar: ttk.Progressbar
        self.ignore_expensive_items: ttk.Checkbutton
        self.ignore_expensive_var: tk.BooleanVar
        self.ignore_negative_profits: ttk.Checkbutton
        self.ignore_negative_var: tk.BooleanVar
        
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

    def create_coin_input(self, frame):
        coin_label = tk.Label(frame, text="Enter coin count: ")
        coin_label.pack(anchor="w")
        self.coin_input_box = ttk.Entry(frame, width=40)
        self.coin_input_box.pack()

    def _create_filter(self, frame, label_text):
        inner_frame = tk.Frame(frame)
        inner_frame.pack(anchor="w")

        label = tk.Label(inner_frame, text=label_text)
        label.pack(side="left")

        checkbutton_value = tk.BooleanVar(value=False)
        checkbutton = ttk.Checkbutton(inner_frame, variable=checkbutton_value)
        checkbutton.pack(side="left", padx=5)

        return checkbutton, checkbutton_value

    def create_expensive_filter(self, frame):
        self.ignore_expensive_items, self.ignore_expensive_var = self._create_filter(frame, "Ignore expensive items: ")

    def create_negative_filter(self, frame):
        self.ignore_negative_profits, self.ignore_negative_var = self._create_filter(frame, "Ignore negative profit: ")

    def create_refresh_button(self, frame):
        self.send_to_calculate_button = tk.Button(frame, text="→")
        self.send_to_calculate_button.pack(side="right", padx=5, pady=5)

    def create_treeview(self, frame):
        self.treev = ttk.Treeview(frame, selectmode="browse")
        self.treev.pack(expand=True, fill="both", padx=5, pady=5)
        self.setup_treeview()

    def setup_treeview(self):
        self.treev["columns"] = [str(i) for i in range(1, len(self.COLUMN_NAMES)+1)]
        self.treev["show"] = "headings"

        for i in range(len(self.treev["columns"])):
            self.treev.column(self.treev["column"][i], anchor="center", width=100)
            self.treev.heading(self.treev["column"][i], text=self.COLUMN_NAMES[i])
    
    def insert_into_treev(self, compute_results) -> None:
        if self.treev and len(compute_results) == 6:
            self.treev.insert("", "end", values=tuple(compute_results))

    def clear_treeview(self) -> None:
        for element in self.treev.get_children():
            self.treev.delete(element)

        
    
    def create_flip_window(self, parent):
        # create all frames necessary to hold elements
        main_window_frame = tk.Frame(parent)
        top_bar_frame = tk.Frame(main_window_frame)
        coin_input_frame = tk.Frame(top_bar_frame)
        filtering_options_frame = tk.Frame(top_bar_frame)
        ignore_expensive_frame = tk.Frame(filtering_options_frame)
        ignore_negative_frame = tk.Frame(filtering_options_frame)

        # pack all frames
        main_window_frame.pack()
        top_bar_frame.pack(fill="x", padx=5, pady=5)
        coin_input_frame.pack(side="left", padx=5, pady=5)
        filtering_options_frame.pack(side="left", padx=5, pady=5)
        ignore_expensive_frame.pack(side="top", padx=5, pady=5)
        ignore_negative_frame.pack(side="bottom", padx=5, pady=5)

        # all elements
        self.create_coin_input(coin_input_frame)
        self.create_expensive_filter(ignore_expensive_frame)
        self.create_negative_filter(ignore_negative_frame)
        self.create_refresh_button(top_bar_frame)
        self.create_treeview(main_window_frame)

        return main_window_frame

    def create_popup(self) -> None:
        popup = tk.Toplevel(self.root)
        popup.title("Skyblock Data Analyzer")
        popup.transient(self.root)
        popup.grab_set()

        popup.geometry("300x100+{}+{}".format(self.root.winfo_x() + 100, self.root.winfo_y() + 100))
        
        popup_label = tk.Label(popup, text="Please enter a valid integer!")
        popup_label.pack(padx=10, pady=10)

        close_button = ttk.Button(popup, text="OK", command=popup.destroy)
        close_button.pack(padx=10)

        self.root.wait_window(popup)



if __name__ == "__main__":
    window = DataAnalyzerWindow()
    window.start()
