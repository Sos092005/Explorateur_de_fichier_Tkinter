import tkinter as tk
from barre_chemin import PathBar
from barre_recherche import SearchBar
from boutons import BarreSuperieureButtons
from styles import Styles

class TopBar(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Apply theme style to the frame
        Styles.apply_frame_style(self)

        # Configure grid layout
        self.columnconfigure(0, minsize=40)  # Forward Button
        self.columnconfigure(1, minsize=40)  # Up Button
        self.columnconfigure(2, minsize=40)  # Refresh Button
        self.columnconfigure(3, minsize=20)  # Spacer before Address Bar
        self.columnconfigure(4, weight=1)    # Address Bar (Path Bar)
        self.columnconfigure(5, minsize=20)  # Spacer before Search Bar
        self.columnconfigure(6, minsize=479) # Search Bar

        # Forward Button
        self.forward_button = tk.Button(self, text="→", font=("Arial", 14))
        self.forward_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Up Button
        self.up_button = tk.Button(self, text="↑", font=("Arial", 14))
        self.up_button.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        # Refresh Button (F5)
        self.refresh_button = tk.Button(self, text="⟳", font=("Arial", 14))
        self.refresh_button.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

        # Path Bar (Address Bar)
        self.path_bar = PathBar(self)
        self.path_bar.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Search Bar
        self.search_bar = SearchBar(self)
        self.search_bar.grid(row=0, column=6, padx=5, pady=10, sticky="ew")

        # Buttons (Extra Controls)
        self.buttons = BarreSuperieureButtons(self)
        self.buttons.grid(row=0, column=7, padx=5, pady=10, sticky="nsew")


import tkinter as tk
root = tk.Tk()
root.title("File Explorer")
a = TopBar(root)
a.pack(fill=tk.X, padx=10, pady=5)
root.mainloop()