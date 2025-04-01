import tkinter as tk
from tkinter import PhotoImage
from styles import Styles  # Correct import for Styles


class PathBar:
    def __init__(self, parent):
        self.parent = parent
        self.style = Styles()  # Access the Styles for theming
        self.create_path_bar()

    def create_path_bar(self):
        # Frame to hold the path bar components
        self.path_frame = tk.Frame(self.parent, bg=self.style.primary_background)
        self.path_frame.pack(fill=tk.X, padx=10, pady=5)

        # Load the home icon (this icon will always remain static at the beginning)
        self.home_icon = PhotoImage(file="assets/icons/home.png")  # Correct path for the home icon

        # Label to display the home icon
        self.home_label = tk.Label(self.path_frame, image=self.home_icon, bg=self.style.primary_background)
        self.home_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Label to display the static part of the path (home directory)
        self.home_label_text = tk.Label(self.path_frame, text="Home", font=("Arial", 12), bg=self.style.primary_background, fg=self.style.path_text)
        self.home_label_text.pack(side=tk.LEFT, padx=5, pady=5)

        # Optional: Add the separator and the rest of the path dynamically
        self.separator_label = tk.Label(self.path_frame, text=" > ", font=("Arial", 12), bg=self.style.primary_background, fg=self.style.separator_color)
        self.separator_label.pack(side=tk.LEFT)

        # Label to display the rest of the path (example for now, can be updated dynamically)
        self.path_label = tk.Label(self.path_frame, text="Users/YourUsername/Documents", font=("Arial", 12), bg=self.style.primary_background, fg=self.style.path_text)
        self.path_label.pack(side=tk.LEFT, padx=5, pady=5)

    def update_path(self, new_path):
        # Update the path dynamically (this method can be called when the directory changes)
        self.path_label.config(text=new_path)

