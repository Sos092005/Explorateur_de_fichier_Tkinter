# Importing necessary tkinter modules for styling
from tkinter import font

# Defining global color scheme based on GitHub's Light Theme
class Theme:
    primary_bg = "#F6F8FA"  # Light grayish white, used as the main background color
    secondary_bg = "#FFFFFF"  # Pure white, used for secondary panels and widgets
    border_color = "#D0D7DE"  # Soft gray, used for borders and dividers
    text_color = "#24292E"  # Dark gray-black, for text to provide high contrast
    hover_color = "#F3F4F6"  # Light gray, used for hover background
    selected_bg = "#EAECEF"  # Slightly darker gray for selected items
    
    # Path bar and search bar
    path_bar_bg = "#EAECEF"  # Light gray, consistent with selected background
    search_bar_bg = "#FFFFFF"  # Pure white for the search bar, clean and legible
    search_bar_text = "#24292E"  # Dark gray for text in search bar
    
    # Button Styles
    button_bg = "#F6F8FA"  # Matches primary background, subtly different from others
    button_text = "#24292E"  # Dark gray-black for button text
    active_button_bg = "#F3F4F6"  # Hover effect on buttons, slightly darker
    
    
    # Frame Styles
    frame_bg = "#F6F8FA"  # Matches primary background for frames


    # Font styles
    header_font = ("Arial", 12, "bold")
    regular_font = ("Arial", 10)
    button_font = ("Arial", 10, "bold")
    
    # Icon sizes (in case we use icon-based buttons)
    icon_size = 20  # Standard size for icons


# Applying styles to different elements
class Styles:
    @staticmethod
    def apply_button_style(button):
        """Apply common button styles."""
        button.config(
            bg=Theme.button_bg,
            fg=Theme.button_text,
            font=Theme.button_font,
            relief="flat",  # Removing borders for a clean look
            activebackground=Theme.active_button_bg,
            bd=0,  # No border
            highlightthickness=0  # No highlight thickness
        )
    
    @staticmethod
    def apply_entry_style(entry):
        """Apply common styles for entry widgets (like search bar)."""
        entry.config(
            bg=Theme.search_bar_bg,
            fg=Theme.search_bar_text,
            font=Theme.regular_font,
            bd=0,  # No border
            highlightthickness=0  # No highlight thickness
        )
    
    @staticmethod
    def apply_path_bar_style(path_bar):
        """Apply styling for the path bar."""
        path_bar.config(
            bg=Theme.path_bar_bg,
            fg=Theme.text_color,
            font=Theme.regular_font,
            relief="flat",  # Clean, flat design
            height=2
        )

    @staticmethod
    def apply_frame_style(frame):
        """Apply common styles for frames."""
        frame.config(
            bg=Theme.frame_bg,
            bd=0,  # No border
            highlightthickness=0  # No highlight thickness
        )




# Utility function to get icon size (in case it's needed for buttons)
def get_icon_size():
    return Theme.icon_size
