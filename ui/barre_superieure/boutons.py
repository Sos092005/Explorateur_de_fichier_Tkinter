import tkinter as tk
from tkinter import PhotoImage
import os
import styles

# Importing Styles from styles.py in the same folder (barre_superieure)
from styles import Styles


class BarreSuperieureButtons:
    def __init__(self, parent):
        self.parent = parent  # Parent is the frame or window where buttons will be placed
        self.buttons_frame = tk.Frame(self.parent, bg="#F6F8FA")  # Create a frame to hold buttons
        self.buttons_frame.pack(fill="x", padx=10, pady=10)  # Pack the frame with some padding

        # Load PNG icons
        self.load_icons()
        self.create_buttons()

    def load_icons(self):
        """Load PNG icons from the assets/icons folder."""
        self.icons = {}  # Dictionary to store the icons

        # List of button icons
        icon_files = ["back.png", "forward.png", "home.png", "next.png", "refresh.png", "search.png", "up.png"]

        # Path to assets/icons folder
        icon_folder = os.path.join(os.getcwd(), "assets", "icons")

        # Load each PNG icon
        for icon_file in icon_files:
            icon_path = os.path.join(icon_folder, icon_file)
            self.icons[icon_file] = PhotoImage(file=icon_path)

    def create_buttons(self):
        """This method creates all the buttons in the top bar."""
        
        # Example button 1: 'Back' button
        self.back_button = self.create_button(self.icons["back.png"], self.on_back_click)
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        # Example button 2: 'Forward' button
        self.forward_button = self.create_button(self.icons["forward.png"], self.on_forward_click)
        self.forward_button.grid(row=0, column=1, padx=5, pady=5)

        # Example button 3: 'Home' button
        self.home_button = self.create_button(self.icons["home.png"], self.on_home_click)
        self.home_button.grid(row=0, column=2, padx=5, pady=5)

        # Example button 4: 'Next' button
        self.next_button = self.create_button(self.icons["next.png"], self.on_next_click)
        self.next_button.grid(row=0, column=3, padx=5, pady=5)

        # Example button 5: 'Refresh' button
        self.refresh_button = self.create_button(self.icons["refresh.png"], self.on_refresh_click)
        self.refresh_button.grid(row=0, column=4, padx=5, pady=5)

        # Example button 6: 'Search' button
        self.search_button = self.create_button(self.icons["search.png"], self.on_search_click)
        self.search_button.grid(row=0, column=5, padx=5, pady=5)

        # Example button 7: 'Up' button
        self.up_button = self.create_button(self.icons["up.png"], self.on_up_click)
        self.up_button.grid(row=0, column=6, padx=5, pady=5)

    def create_button(self, icon, command):
        """Helper method to create a button with an icon and predefined styles."""
        button = tk.Button(self.buttons_frame, image=icon, command=command, bd=0, relief="flat", bg="#F6F8FA")
        Styles.apply_button_style(button)  # Apply the styling from styles.py
        return button

    # Button click event methods
    def on_back_click(self):
        print("Back button clicked")

    def on_forward_click(self):
        print("Forward button clicked")

    def on_home_click(self):
        print("Home button clicked")

    def on_next_click(self):
        print("Next button clicked")

    def on_refresh_click(self):
        print("Refresh button clicked")

    def on_search_click(self):
        print("Search button clicked")

    def on_up_click(self):
        print("Up button clicked")
