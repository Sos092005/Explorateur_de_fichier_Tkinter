import tkinter as tk
from styles import Styles  # Import the Styles class for consistent styling

class SearchBar:
    def __init__(self, parent):
        self.parent = parent
        self.style = Styles()  # Access the Styles for theming
        self.create_search_bar()

    def create_search_bar(self):
        # Frame to hold the search bar components
        self.search_frame = tk.Frame(self.parent, bg=self.style.primary_background)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create the search entry widget
        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 12), bd=0, relief="flat")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)

        # Apply the entry field's style (background and text color from Styles)
        self.search_entry.config(
            bg=self.style.search_bar_background, 
            fg=self.style.search_bar_text, 
            insertbackground=self.style.search_bar_text
        )

        # Create the search button
        self.search_button = tk.Button(self.search_frame, text="🔍", command=self.search, bd=0, relief="flat")
        self.search_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Apply button style from Styles
        self.search_button.config(
            bg=self.style.button_background,
            fg=self.style.button_text
        )

        # Hover effect on search button
        self.search_button.bind("<Enter>", lambda e: self.on_hover(self.search_button))
        self.search_button.bind("<Leave>", lambda e: self.on_leave(self.search_button))

    def search(self):
        # Placeholder for search action (no logic yet)
        print("Search triggered...")

    def on_hover(self, button):
        # Change background color on hover (active state)
        button.config(bg=self.style.active_button_background)

    def on_leave(self, button):
        # Reset background color when hover ends
        button.config(bg=self.style.button_background)
