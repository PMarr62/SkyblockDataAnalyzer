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
        self.treev: ttk.Treeview
        self.coin_input_box: ttk.Entry
        self.refresh_button: tk.Button
        self.loading_bar: ttk.Progressbar
        
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

        coin_input_frame = tk.Frame(top_bar)
        coin_input_frame.pack(side="left", padx=5, pady=5)

        coin_label = tk.Label(coin_input_frame, text="Enter coin count:")
        coin_label.pack(anchor="w")

        self.coin_input_box = ttk.Entry(coin_input_frame, width=40)
        self.coin_input_box.pack()

        self.refresh_button = tk.Button(top_bar, text="→")
        self.refresh_button.pack(side="right", padx=5, pady=5)

        self.loading_bar = ttk.Progressbar(frame, mode="indeterminate")
        self.loading_bar.pack(fill="x", padx=10, pady=5)

        self.treev = ttk.Treeview(frame, selectmode="browse")
        self.treev.pack(expand=True, fill="both", padx=5, pady=5)
        # Product name, total buy price, total sell price, number of items needed for craft, profit, profit margin?, time-to-wait (avg)
        num_columns = 6
        column_names = ["Product Name", "Total Buy Price", "Total Sell Price", "Profit", "Quantity", "Num. hours wait"]

        self.treev["columns"] = [str(i) for i in range(1, num_columns+1)]
        self.treev["show"] = "headings"

        for i in range(len(self.treev["columns"])):
            self.treev.column(self.treev["column"][i], anchor="center", width=100)
            self.treev.heading(self.treev["column"][i], text=column_names[i])

        return frame
    
    # methods to update treev and loading bar outside of this class (perhaps in a tkinter window / analyzer combinatory class)
    def insert_into_treev(self, compute_results) -> None:
        if self.treev and len(compute_results) == 6:
            self.treev.insert("", "end", values=tuple(compute_results))

    def start_loading_bar(self) -> None:
        self.loading_bar.start()

    def stop_loading_bar(self) -> None:
        self.loading_bar.stop()

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

    def clear_treeview(self) -> None:
        for element in self.treev.get_children():
            self.treev.delete(element)

        
        

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
