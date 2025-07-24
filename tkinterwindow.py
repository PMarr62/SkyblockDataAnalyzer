"""
Modified codestub of creating a tkinter window with a table.
Original code found from geeksforgeeks.com.
"""

from tkinter import ttk
import tkinter as tk

class DataAnalyzerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Skyblock Data Analyzer")
        self.root.geometry("500x300")

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        self.frames["main"] = self.create_main_window(self.container)
        self.frames["flip"] = self.create_flip_window(self.container)

        # instance variables for the table and loading bar for later access
        self.treev = None
        self.loading_bar = None

        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

        self.show_frame("main")

    def show_frame(self, window_name: str):
        frame: tk.Frame = self.frames[window_name]
        frame.tkraise()

    def start(self):
        self.root.mainloop()

    def create_main_window(self, parent) -> tk.Frame:
        frame = tk.Frame(parent)
    
        label = tk.Label(frame, text="Welcome to Skyblock Data Analyzer!")
        label.pack(pady=20)

        button = tk.Button(frame, text="Go to flips", command=lambda: self.show_frame("flip"))
        button.pack()

        return frame
    
    def create_flip_window(self, parent):
        frame = tk.Frame(parent)

        top_bar = tk.Frame(frame)
        top_bar.pack(fill="x", padx=5, pady=5)
        
        back_button = tk.Button(top_bar, text="←", command=lambda: self.show_frame("main"))
        back_button.pack(side="left", padx=5, pady=5)

        # currently no capability, will be a refresh for API data
        refresh_button = tk.Button(top_bar, text="↻")
        refresh_button.pack(side="right", padx=5, pady=5)

        self.loading_bar = ttk.Progressbar(frame)
        self.loading_bar.pack(fill="x", padx=10, pady=5)

        self.treev = ttk.Treeview(frame, selectmode="browse")
        self.treev.pack(expand=True, fill="both")

        self.treev["columns"] = ("1", "2", "3")
        self.treev["show"] = "headings"

        self.treev.column("1", anchor="center", width=100)
        self.treev.column("2", anchor="se", width=100)
        self.treev.column("3", anchor="se", width=100)

        self.treev.heading("1", text="Item name")
        self.treev.heading("2", text="Price")
        self.treev.heading("3", text="Profit")

        self.treev.insert("", "end", values=("test name", 1000, 100))

        return frame

if __name__ == "__main__":
    window = DataAnalyzerWindow()
    window.start()
