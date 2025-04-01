
from barre_superieure.barre_superieure import TopBar
from barre_superieure.styles import Styles
import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Apply theme Styles
        self.title("File Explorer")
        self.geometry("1200x700")  # Window size
        Styles.apply_styles(self)  # Corrected method name

        # Configure grid layout
        self.columnconfigure(0, weight=1)  # Main content expands
        self.rowconfigure(1, weight=1)  # File display area expands

        # **Top Bar (Navigation, Search, Buttons)**
        self.top_bar = TopBar(self)
        self.top_bar.grid(row=0, column=0, sticky="ew")

        # **Main Content Area (Placeholder for now)**
        self.main_frame = tk.Frame(self, bg="#ffffff")  # White background
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        # **Bottom Status Bar (Placeholder)**
        self.status_bar = tk.Label(self, text="Ready", anchor="w", bg="#e0e0e0")
        self.status_bar.grid(row=2, column=0, sticky="ew")


# Run Application
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()