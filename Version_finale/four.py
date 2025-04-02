import sys
import subprocess
import os
# 1. Test d'importation et d'installation des modules nécessaires
def install_dependencies():
    """Installe les dépendances depuis requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("Fichier requirements.txt introuvable!")
        return

    try:
        subprocess.check_call([
            sys.executable, 
            "-m", "pip", "install",
            "-r", requirements_file
        ])
        print("\nToutes les dépendances sont installées avec succès!")
    except subprocess.CalledProcessError:
        print("\nÉchec de l'installation des dépendances")
        sys.exit(1)

# Vérifie et installe les dépendances au démarrage
install_dependencies()

# Vérification des modules Windows
# Vérification des modules Windows SEULEMENT sur Windows
WINDOWS = False
HAS_WINSHELL = False

if os.name == 'nt':
    try:
        import win32api
        import win32con  # Ajouté
        import winshell
        WINDOWS = True
        HAS_WINSHELL = True
    except ImportError as e:
        print(f"Erreur d'importation des modules Windows: {str(e)}")
        sys.exit(1)

# 2. Importation des bibliothèques nécessaires
import tkinter as tk
import shutil
import logging
import threading
import queue
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFont
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import ttk, messagebox, simpledialog, filedialog
import platform 
import ttkthemes
import webbrowser
import zipfile
import winshell
import json



# ======================
# LOGGING CONFIGURATION
# ======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# ======================
# ICON MANAGER
# ======================
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont

class IconManager:
    """Handles icon loading with fallback system"""
    def __init__(self):
        self.icons = {}
        self.toolbar_icons = {}  # Separate storage for toolbar icons
        self.default_icon = self._create_default_icon(size=(24, 24))
        
        # Get absolute path to assets directory
        self.base_path = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Define paths with absolute locations
        self.ICON_PATHS = {
            'folder': os.path.join(self.base_path, 'folder.png'),
            'sort_asc': os.path.join(self.base_path, 'sort_asc.png'),
            'sort_desc': os.path.join(self.base_path, 'sort_desc.png'),
            'file': os.path.join(self.base_path, 'file.png'),
            'copy': os.path.join(self.base_path, 'copy.png'),
            'cut': os.path.join(self.base_path, 'cut.png'),
            'paste': os.path.join(self.base_path, 'paste.png'),
            'delete': os.path.join(self.base_path, 'delete.png'),
            'new_folder': os.path.join(self.base_path, 'new_folder.png'),
            'refresh': os.path.join(self.base_path, 'refresh.png'),
            'theme': os.path.join(self.base_path, 'theme.png'),
            'search': os.path.join(self.base_path, 'search.png'),
            'view': os.path.join(self.base_path, 'view.png'),
            'info': os.path.join(self.base_path, 'info.png'),
            'pdf': os.path.join(self.base_path, 'pdf.png'),
            'image': os.path.join(self.base_path, 'image.png'),
            'music': os.path.join(self.base_path, 'music.png'),
            'video': os.path.join(self.base_path, 'video.png'),
            'archive': os.path.join(self.base_path, 'archive.png'),
            'code': os.path.join(self.base_path, 'code.png'),
            'text': os.path.join(self.base_path, 'text.png'),
            'exe': os.path.join(self.base_path, 'exe.png'),
            'word': os.path.join(self.base_path, 'word.png'),
            'excel': os.path.join(self.base_path, 'excel.png'),
            'powerpoint': os.path.join(self.base_path, 'powerpoint.png'),
            'favorites': os.path.join(self.base_path, 'favorites.png'),
            'up': os.path.join(self.base_path, 'up.png'),
            'forward': os.path.join(self.base_path, 'forward.png'),
            'backward': os.path.join(self.base_path, 'backward.png')
        }
        
        self.load_icons()

    def load_icons(self):
        """Load icons with different sizes for toolbar vs. other uses"""
        for key, path in self.ICON_PATHS.items():
            try:
                # Default icons (24x24)
                img = Image.open(path).resize((24, 24))
                self.icons[key] = ImageTk.PhotoImage(img)
                
                # Larger toolbar icons (32x32)
                img_large = Image.open(path).resize((32, 32))
                self.toolbar_icons[key] = ImageTk.PhotoImage(img_large)
            except Exception as e:
                print(f"Error loading icon {key}: {str(e)}")
                self.icons[key] = self.default_icon
                self.toolbar_icons[key] = self.default_icon

    def get_toolbar_icon(self, name):
        """Get larger icon specifically for toolbar"""
        return self.toolbar_icons.get(name, self.default_icon)

    def get_file_icon(self, path):
        """Get appropriate icon based on file type"""
        if os.path.isdir(path):
            return self.get_icon('folder')
    
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        
        icon_map = {
            'pdf': 'pdf',
            'png': 'image', 'jpg': 'image', 'jpeg': 'image', 'gif': 'image',
            'mp3': 'music', 'wav': 'music', 'flac': 'music',
            'mp4': 'video', 'avi': 'video', 'mov': 'video',
            'zip': 'archive', 'rar': 'archive', '7z': 'archive',
            'py': 'code', 'js': 'code', 'html': 'code', 'css': 'code',
            'txt': 'text',
            'doc': 'word', 'docx': 'word',
            'xls': 'excel', 'xlsx': 'excel',
            'ppt': 'powerpoint', 'pptx': 'powerpoint',
            'exe': 'exe', 'msi': 'exe'
        }
        
        icon_name = icon_map.get(ext, 'file')
        return self.get_icon(icon_name)

    def _create_default_icon(self, size=(24, 24)):
        """Create fallback icon with question mark"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()
        draw.text((size[0]//2, size[1]//2), "?", 
                 fill="#808080", font=font, anchor="mm")
        return ImageTk.PhotoImage(img)

    def get_icon(self, name):
        """Get icon with fallback"""
        return self.icons.get(name, self.default_icon)
    

# ======================
# THEME MANAGER
# ======================
class ThemeManager:
    """Handles theme switching with ttkbootstrap integration"""
    CUSTOM_THEMES = {
        'VSCode Dark': {
            'primary': '#1e1e1e',
            'secondary': '#252526',
            'accent': '#3794ff',
            'font': '#d4d4d4'
        },
        'VSCode Light': {
            'primary': '#ffffff',
            'secondary': '#f3f3f3',
            'accent': '#007acc',
            'font': '#333333'
        },
        'Monokai': {
            'primary': '#272822',
            'secondary': '#3e3d32',
            'accent': '#a6e22e',
            'font': '#f8f8f2'
        }
    }

    def __init__(self, root):
        self.style = ttkb.Style()
        self.root = root
        self.current_theme = 'litera'  # Default light theme
            
    def get_theme_names(self):
        """Return all available ttkbootstrap themes plus custom ones"""
        # Get all built-in ttkbootstrap themes
        builtin_themes = sorted(self.style.theme_names())
        
        # Add custom themes
        return builtin_themes + sorted(self.CUSTOM_THEMES.keys())
    
    def apply_theme(self, theme_name):
        """Apply selected theme"""
        if theme_name in self.CUSTOM_THEMES:
            self._apply_custom_theme(theme_name)
        else:
            self.style.theme_use(theme_name)
        self.current_theme = theme_name
        
        
    def _apply_custom_theme(self, theme_name):
        """Apply VSCode-style custom theme with proper ttkbootstrap integration"""
        colors = self.CUSTOM_THEMES[theme_name]
        
        # Create a new theme based on ttkbootstrap
        self.style.theme_create(
            name=theme_name.lower().replace(' ', '_'),  # Theme names should be lowercase with underscores
            parent='litera',  # Start with a base ttkbootstrap theme
            settings={
                '.' : {
                    'configure': {
                        'background': colors['primary'],
                        'foreground': colors['font'],
                        'font': ('Segoe UI', 10)
                    }
                },
                'TButton': {
                    'configure': {
                        'background': colors['secondary'],
                        'foreground': colors['font'],
                        'borderwidth': 1,
                        'padding': (6, 3)
                    },
                    'map': {
                        'background': [('active', colors['accent'])]
                    }
                },
                'TLabel': {
                    'configure': {
                        'background': colors['primary'],
                        'foreground': colors['font']
                    }
                },
                'Treeview': {
                    'configure': {
                        'background': colors['secondary'],
                        'fieldbackground': colors['secondary'],
                        'foreground': colors['font'],
                        'rowheight': 25
                    },
                    'map': {
                        'background': [('selected', colors['accent'])],
                        'foreground': [('selected', colors['primary'])]
                    }
                },
                'TFrame': {
                    'configure': {
                        'background': colors['primary']
                    }
                },
                'TEntry': {
                    'configure': {
                        'fieldbackground': colors['secondary'],
                        'foreground': colors['font'],
                        'insertcolor': colors['font']
                    }
                }
            }
        )
        self.style.theme_use(theme_name.lower().replace(' ', '_'))

# ======================
# TOOLTIP SYSTEM
# ======================
class Tooltip:
    """Custom tooltip implementation"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1
        )
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

# ======================
# MAIN APPLICATION
# ======================
class FileExplorer(ttkb.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("EXplorateur de Fichier Tkinter")
        self.geometry('1920x1080')
        
        
        # Initialize navigation history
        self.history = []
        self.history_index = -1
        
    # Initialize attributes FIRST
        self.selected_items = []
        self.clipboard = None
        self.view_mode = 'list'
        self.current_path = os.path.expanduser("~")
        self.search_running = False  
        self.search_cancel = False
        self.search_dialog = None
        self.results_list = None
        
        self.favorites = []
        self.load_favorites()
        
        # Then setup resources and UI
        self._setup_resources()
        self._build_ui()  # This will create all widgets first
        self._setup_bindings()  # Then setup bindings
    
        self.protocol("WM_DELETE_WINDOW", self._on_close)        
        
 
 
 
         
    def load_favorites(self):
        """Load favorites from config file"""
        config_path = os.path.join(os.path.expanduser("~"), ".fluentexplorer", "prefs.json")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.favorites = config.get('favorites', [])
        except:
            self.favorites = []
    
    def save_favorites(self):
        """Save favorites to config file"""
        config_path = os.path.join(os.path.expanduser("~"), ".fluentexplorer", "prefs.json")
        config = {}
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except:
            pass
        config['favorites'] = self.favorites
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _add_to_favorites(self, path):
        """Add current item to favorites"""
        if path not in self.favorites:
            self.favorites.append(path)
            self.save_favorites()
            self._refresh_sidebar()
    
    def _remove_from_favorites(self, path):
        """Remove item from favorites"""
        if path in self.favorites:
            self.favorites.remove(path)
            self.save_favorites()
            self._refresh_sidebar()

    def _refresh_sidebar(self):
        """Refresh the favorites section in sidebar"""
        self._populate_favorites()
        self.favorites_list.update_idletasks() 
 
    def _on_close(self):
        """Handle window close event"""
        # Save user preferences
        self._save_preferences()
        # Clean up resources
        self.destroy()

    #saving

    def _save_preferences(self):
        """Save user settings to config file"""
        config = {
            'theme': self.theme_manager.current_theme,
            'view_mode': self.view_mode,
            'window_size': self.geometry(),
            'last_directory': self.current_path
        }
        
        config_dir = os.path.join(os.path.expanduser("~"), ".fluentexplorer")
        os.makedirs(config_dir, exist_ok=True)
        
        config_path = os.path.join(config_dir, "prefs.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)



    def _setup_bindings(self):
        """Configure all keyboard and mouse bindings"""
        # Keyboard shortcuts
        self.bind("<F5>", lambda e: self._refresh_view())
        self.bind("<Delete>", lambda e: self._delete_selected())
        self.bind("<Control-n>", lambda e: self._create_new_folder())
        self.bind("<Control-q>", lambda e: self.quit())
        
        # Treeview bindings
        self.list_view.bind("<<TreeviewSelect>>", self._on_selection_change)
        self.list_view.bind("<Double-1>", self._on_item_double_click)
        
        # Context menu
        self.list_view.bind("<Button-3>", self._show_context_menu)
        self.grid_canvas.bind("<Button-3>", self._show_context_menu)
        
        # Navigation
        self.bind("<Alt-Left>", lambda e: self._navigate_back())
        self.bind("<Alt-Right>", lambda e: self._navigate_forward())


    def _setup_resources(self):
        """Initialize shared resources"""
        self.icon_manager = IconManager()
        self.theme_manager = ThemeManager(self)
        self.theme_manager = ThemeManager(self)
        self.clipboard = {'operation': None, 'path': None}
        self.current_path = os.path.expanduser("~")
        self.selected_items = []
        self.view_mode = 'list'  # 'list' or 'grid'

    def _build_ui(self):
        """Build UI with proper vertical sidebar and toolbar"""
        # Main container (vertical)
        main_container = ttkb.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 1. Toolbar (top)
        self._build_toolbar(main_container)
        
        # 2. Create main content paned window
        self.main_paned = ttkb.PanedWindow(main_container, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # 3. Vertical sidebar (left)
        self._build_sidebar(self.main_paned)  # Pass the paned window
        
        # 4. Main content (right)
        self._build_main_content(self.main_paned)
        
        # 5. Status bar (bottom)
        self._build_statusbar(main_container)
    
    def _on_selection_change(self, event):
        """Handle selection changes in the list view"""
        self.selected_items = [
            self.list_view.item(item)['tags'][0]
            for item in self.list_view.selection()
        ]
        self.selected_label.config(
            text=f"Selected: {len(self.selected_items)} items"
        )

    def _on_item_double_click(self, event):
        """Handle double-click on list view items"""
        try:
            selected = self.list_view.selection()
            if not selected:
                return
                
            item = selected[0]
            path = self.list_view.item(item, 'tags')[0]
            
            if os.path.isdir(path):
                self._navigate_to(path)
            else:
                try:
                    if platform.system() == 'Windows':
                        os.startfile(path)
                    elif platform.system() == 'Darwin':
                        subprocess.run(['open', path])
                    else:
                        subprocess.run(['xdg-open', path])
                except Exception as e:
                    messagebox.showerror("Open Error", f"Could not open file: {str(e)}")
        except IndexError:
            pass  # No item selected
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def _create_main_paned_window(self):
        """Create the main paned window container with proper pane configuration"""
        self.main_paned = ttk.PanedWindow(self, bootstyle="primary", orient=VERTICAL)
        self.main_paned.pack(fill=BOTH, expand=True)

        # 1. Toolbar Frame (fixed height)
        self.toolbar_frame = ttk.Frame(self.main_paned, height=40)
        self.main_paned.add(self.toolbar_frame)  # Fixed height pane

        # 2. Main Content Area 
        content_pane = ttk.Frame(self.main_paned)
        self.main_paned.add(content_pane)  # Expanding pane

        # 3. Prevent toolbar frame from resizing
        self.toolbar_frame.pack_propagate(False)

    def _build_toolbar(self,parent):
        """Add toolbar without affecting sidebar layout"""
        self.toolbar_frame = ttkb.Frame(parent, height=40)
        self.toolbar_frame.pack(fill=tk.X, pady=2)
        
        """Build toolbar with guaranteed 40px height"""
        # Clear existing widgets (now safe since toolbar_frame exists)
        for widget in self.toolbar_frame.winfo_children():
            widget.destroy()

        # Left-aligned buttons container
        left_container = ttkb.Frame(self.toolbar_frame)
        left_container.pack(side=LEFT, fill=BOTH, expand=True)

        actions = [
            ('new_folder', self._create_new_folder),
            ('copy', self._copy_items),
            ('cut', self._cut_items),
            ('paste', self._paste_items),
            ('delete', self._delete_selected),
            ('refresh', self._refresh_view),
            ('view', self._toggle_view_mode),  # VIEW BUTTON ADDED HERE
            ('theme', self._show_theme_selector)
        ]

        for icon_key, command in actions:
            btn = ttkb.Button(
                left_container,
                image=self.icon_manager.get_icon(icon_key),
                bootstyle=(LINK, OUTLINE),
                command=command,
                padding=(2, 0)
            )
            btn.pack(side=LEFT, padx=2)

        # Right-aligned search
        right_container = ttkb.Frame(self.toolbar_frame)
        right_container.pack(side=RIGHT)

        search_frame = ttkb.Frame(right_container)
        search_frame.pack(side=LEFT, padx=2)
        
        self.search_entry = ttkb.Entry(search_frame, width=18)
        self.search_entry.pack(side=LEFT)
        
        ttkb.Button(
            search_frame,
            image=self.icon_manager.get_icon('search'),
            bootstyle=(LINK, OUTLINE),
            command=self._start_search
        ).pack(side=LEFT)
        
        # Add sorting controls (AFTER EXISTING BUTTONS)
        sort_frame = ttkb.Frame(left_container)
        sort_frame.pack(side=LEFT, padx=5)

        ttkb.Label(sort_frame, text="Sort by:").pack(side=LEFT)
        
        self.sort_var = ttkb.StringVar(value='name')
        self.sort_order_var = ttkb.BooleanVar(value=True)  # True = ascending
        
        sort_menu = ttkb.Combobox(
            sort_frame,
            textvariable=self.sort_var,
            values=['name', 'size', 'type', 'modified'],
            state='readonly',
            width=10
        )
        sort_menu.pack(side=LEFT, padx=2)
        sort_menu.bind('<<ComboboxSelected>>', self._update_sorting)
        
        self.sort_order_btn = ttkb.Button(
            sort_frame,
            image=self.icon_manager.get_icon('sort_asc'),
            command=self._toggle_sort_order,
            bootstyle=(LINK, OUTLINE)
        )
        self.sort_order_btn.pack(side=LEFT)
        
    def _update_sorting(self, event=None):
        if not hasattr(self, 'list_view') or not self.list_view.winfo_exists():
            return
        
        sort_column = self.sort_var.get()
        reverse = not self.sort_order_var.get()
        
        # For list view
        if self.view_mode == 'list':
            self._sort_list_view(sort_column, reverse)
        
        self._refresh_view()
    
    
    def _toggle_sort_order(self):
        self.sort_order_var.set(not self.sort_order_var.get())
        icon = 'sort_asc' if self.sort_order_var.get() else 'sort_desc'
        self.sort_order_btn.config(image=self.icon_manager.get_icon(icon))
        self._update_sorting()

    def _sort_list_view(self, column, reverse):
        # Map column names to treeview identifiers
        column_map = {
            'name': '#0',
            'size': 'size',
            'type': 'type',
            'modified': ('modified', lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'))
        }
        tv_column = column_map[column]
        
        # Get all items and their values
        items = [(self.list_view.set(child, tv_column), child) 
                for child in self.list_view.get_children('')]
        
        # Special sorting for different columns
        if column == 'size':
            items.sort(key=lambda x: self._parse_size(x[0]), reverse=reverse)
        elif column == 'modified':
            items.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M'), reverse=reverse)
        else:
            items.sort(reverse=reverse, key=lambda x: x[0].lower())
        
        # Rearrange items in treeview
        for index, (_, child) in enumerate(items):
            self.list_view.move(child, '', index)
        
        # Update column header indicators
        for col in self.list_view['columns'] + ('#0',):
            current_text = self.list_view.heading(col)['text']
            new_text = current_text.replace('↑', '').replace('↓', '')
            if col == tv_column:
                new_text += ' ↑' if reverse else ' ↓'
            self.list_view.heading(col, text=new_text)
                    
    # FILE OPERATION METHODS (should be defined BEFORE _build_toolbar)
    def _copy_items(self):
        """Copy selected items to clipboard"""
        if self.selected_items:
            self.clipboard = {
                'operation': 'copy',
                'paths': self.selected_items.copy()
            }
            self.status_label.config(text=f"Copied {len(self.selected_items)} items")

    def _cut_items(self):
        """Cut selected items to clipboard"""
        if self.selected_items:
            self.clipboard = {
                'operation': 'cut',
                'paths': self.selected_items.copy()
            }
            self.status_label.config(text=f"Cut {len(self.selected_items)} items")


    def _refresh_view(self):
        """Refresh current directory view"""
        self.selected_items.clear()
        
        # Only update selected_label if it exists
        if hasattr(self, 'selected_label') and self.selected_label.winfo_exists():
            self.selected_label.config(text="Selected: 0 items")
        
        if self.view_mode == 'list':
            self._update_list_view()
        else:
            self._update_grid_view()
        
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text=f"Loaded {self.current_path}")

    def _paste_items(self):
        """Paste items from clipboard"""
        if not self.clipboard or not self.clipboard['paths']:
            return

        success_count = 0
        failed_items = []

        for src_path in self.clipboard['paths']:
            try:
                dest_path = os.path.join(
                    self.current_path,
                    os.path.basename(src_path)
                )
                
                if self.clipboard['operation'] == 'copy':
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                    success_count += 1
                elif self.clipboard['operation'] == 'cut':
                    shutil.move(src_path, dest_path)
                    success_count += 1
            except Exception as e:
                failed_items.append(f"{os.path.basename(src_path)}: {str(e)}")

        # Show results
        msg = f"Successfully {self.clipboard['operation']}ied {success_count} items"
        if failed_items:
            msg += f"\nFailed: {len(failed_items)} items"
            messagebox.showwarning("Paste Errors", "\n".join(failed_items))
            
        self.status_label.config(text=msg)
        self._refresh_view()


    def _delete_selected(self):
        """Delete selected items with confirmation"""
        if not self.selected_items:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(self.selected_items)} selected items?",
            parent=self
        )
        if not confirm:
            return

        failed_deletions = []
        for path in self.selected_items:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                failed_deletions.append(f"{os.path.basename(path)}: {str(e)}")

        if failed_deletions:
            messagebox.showerror(
                "Deletion Errors",
                "Failed to delete:\n\n" + "\n".join(failed_deletions))
        self._refresh_view()


    def _show_theme_selector(self):
        """Show theme selection dialog"""
        dialog = ttkb.Toplevel(self)
        dialog.title("Select Theme")
        dialog.transient(self)

        themes = self.theme_manager.get_theme_names()
        selected_theme = ttkb.StringVar(value=self.theme_manager.current_theme)

        ttkb.Label(dialog, text="Choose a theme:").pack(pady=5)
        theme_list = ttkb.Combobox(
            dialog,
            textvariable=selected_theme,
            values=themes,
            state='readonly'
        )
        theme_list.pack(padx=10, pady=5)
        theme_list.bind('<<ComboboxSelected>>', 
                      lambda e: self._apply_theme(selected_theme.get()))

        ttkb.Button(dialog, 
                   text="Apply",
                   command=lambda: self._apply_theme(selected_theme.get()),
                   bootstyle="primary").pack(pady=5)


    def _show_search_dialog(self):
        """Show file search dialog with safe existence checks"""
        # Check if dialog needs creation or recreation
        if self.search_dialog is None or not self.search_dialog.winfo_exists():
            # Create new dialog
            self.search_dialog = ttkb.Toplevel(self)
            self.search_dialog.title("Search")
            self.search_dialog.transient(self)
            self.search_dialog.grab_set()

            # Build dialog components
            search_frame = ttkb.Frame(self.search_dialog, padding=10)
            search_frame.pack(fill=X)
            
            self.search_entry = ttkb.Entry(search_frame, width=40)
            self.search_entry.pack(side=LEFT, padx=5)
            
            ttkb.Button(
                search_frame,
                text="Search",
                command=self._start_search,
                bootstyle=PRIMARY
            ).pack(side=LEFT, padx=5)

            # Initialize results list
            self.results_list = ttkb.Treeview(
                self.search_dialog,
                columns=('path', 'type'),
                show='headings',
                height=15
            )
            self.results_list.pack(fill=BOTH, expand=True, padx=10, pady=5)
            
            # Initialize progress bar
            self.search_progress = ttkb.Progressbar(
                self.search_dialog,
                orient=HORIZONTAL,
                mode='indeterminate'
            )
            self.search_progress.pack(fill=X, padx=10, pady=5)
            
            # Reset search states
            self.search_running = False
            self.search_cancel = False
        else:
            # Bring existing dialog to front
            self.search_dialog.lift()
            self.search_dialog.focus_set()
            
            
    def _show_context_menu(self, event):
        """Display right-click context menu with favorites option"""
        menu = ttkb.Menu(self, tearoff=0)
        clicked_path = None

        # Get clicked item based on current view mode
        if self.view_mode == 'list':
            item = self.list_view.identify_row(event.y)
            if item:
                clicked_path = self.list_view.item(item, 'tags')[0]
        else:  # Grid view
            # Implement grid view click detection if needed
            pass

        # Validate path exists
        valid_path = clicked_path and os.path.exists(clicked_path)

        # Build menu items for valid paths
        if valid_path:
            # Update selection if needed
            if clicked_path not in self.selected_items:
                self.selected_items = [clicked_path]

            # Main context menu items
            menu.add_command(
                label="Open",
                command=lambda: self._open_item(clicked_path)
            )
            menu.add_separator()
            menu.add_command(label="Copy", command=self._copy_items)
            menu.add_command(label="Cut", command=self._cut_items)
            menu.add_command(label="Paste", command=self._paste_items)
            menu.add_separator()
            menu.add_command(label="Delete", command=self._delete_selected)
            menu.add_command(
                label="Rename",
                command=lambda: self._rename_item(clicked_path)
            )
            menu.add_command(
                label="Properties",
                command=lambda: self._show_properties(clicked_path)
            )
            
            # Favorites section
            menu.add_separator()
            favorite_label = ("Remove from Favorites" 
                            if clicked_path in self.favorites 
                            else "Add to Favorites")
            menu.add_command(
                label=favorite_label,
                command=lambda: self._toggle_favorite(clicked_path)
            )
        else:
            # Empty space menu
            menu.add_command(
                label="New Folder", 
                command=self._create_new_folder
            )
            menu.add_command(
                label="Paste", 
                command=self._paste_items,
                state='normal' if self.clipboard else 'disabled'
            )
            menu.add_separator()
            menu.add_command(label="Refresh", command=self._refresh_view)

        # Show the menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
                
    def _toggle_favorite(self, path):
        """Toggle item in favorites with validation"""
        if not os.path.exists(path):
            messagebox.showerror("Error", "Path no longer exists")
            return
        
        if path in self.favorites:
            self._remove_from_favorites(path)
        else:
            self._add_to_favorites(path)
        
        # Force UI update
        self._refresh_sidebar()
        self._refresh_view()  # Update any favorite-related visuals
                        
    def _navigate_to(self, path):
        """Navigate to path and update history"""
        path = os.path.abspath(path)
        if path == self.current_path:
            return
            
        # Add to navigation history
        if self.history_index < len(self.history)-1:
            self.history = self.history[:self.history_index+1]
        self.history.append(path)
        self.history_index = len(self.history)-1
        
        self.current_path = path
        self._update_nav_buttons()
        self._update_address_bar()
        self._refresh_view()          
              
    def _build_sidebar(self, parent):
        """Build a vertical sidebar like Windows 11"""
        self.sidebar_frame = ttkb.Frame(self.main_paned, width=150)  # Fixed width
        parent.add(self.sidebar_frame)

        # Quick Access Section (always visible)
        quick_access = ttkb.LabelFrame(
            self.sidebar_frame,
            text="Quick Access",
            bootstyle="info",
            padding=(5, 2)
        )
        quick_access.pack(fill=X, padx=5, pady=5)

        # Favorites Section (scrollable if too many items)
        favorites_frame = ttkb.LabelFrame(
            self.sidebar_frame,
            text="Favorites",
            bootstyle="info",
            padding=(5, 2)
        )
        favorites_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Add a scrollable canvas for favorites
        self.favorites_canvas = ttkb.Canvas(favorites_frame)
        scrollbar = ttkb.Scrollbar(
            favorites_frame,
            orient=VERTICAL,
            command=self.favorites_canvas.yview
        )
        self.favorites_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.favorites_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Frame to hold favorite items inside the canvas
        self.favorites_inner = ttkb.Frame(self.favorites_canvas)
        self.favorites_canvas.create_window((0, 0), window=self.favorites_inner, anchor=NW)

        # Bind canvas resize
        self.favorites_inner.bind(
            "<Configure>",
            lambda e: self.favorites_canvas.configure(scrollregion=self.favorites_canvas.bbox("all"))
        )

        # Populate sections
        self._build_quick_access(quick_access)
        self._populate_favorites()

    def _build_sidebar_toggle(self):
        """Add a collapse/expand button (like Win11)"""
        self.sidebar_toggle = ttkb.Button(
            self.content_frame,
            text=">",  # ">" when collapsed, "<" when expanded
            width=2,
            bootstyle="light-outline",
            command=self._toggle_sidebar
        )
        self.sidebar_toggle.pack(side=LEFT, fill=Y)

    def _toggle_sidebar(self):
        """Collapse/expand the sidebar"""
        if self.sidebar_frame.winfo_ismapped():
            self.sidebar_frame.pack_forget()
            self.sidebar_toggle.config(text=">")
        else:
            self.sidebar_frame.pack(side=LEFT, fill=Y)
            self.sidebar_toggle.config(text="<")

    def _build_quick_access(self, parent):
        """Add drives and common folders as vertical buttons"""
        # Common folders (Home, Desktop, Documents, Downloads)
        folders = {
            "Home": os.path.expanduser("~"),
            "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "Downloads": os.path.join(os.path.expanduser("~"), "Downloads")
        }

    # Lecteurs Windows uniquement
        if WINDOWS:
            try:
                drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
                for drive in drives:
                    btn = ttkb.Button(
                        parent,
                        text=drive,
                        image=self.icon_manager.get_icon('folder'),
                        compound=LEFT,
                        bootstyle="light",
                        command=lambda d=drive: self._navigate_to(d)
                    )
                    btn.pack(fill=X, pady=2)
            except Exception as e:
                logging.error(f"Erreur chargement lecteurs: {str(e)}")

        for name, path in folders.items():
            if os.path.exists(path):
                btn = ttkb.Button(
                    parent,
                    text=name,
                    image=self.icon_manager.get_icon('folder'),
                    compound=LEFT,
                    bootstyle="light",
                    command=lambda p=path: self._navigate_to(p)
                )
                btn.pack(fill=X, pady=2)  # Fill horizontally, small vertical padding

        # Add drives (Windows only)
        if os.name == 'nt' and WINDOWS:
            try:
                drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
                for drive in drives:
                    btn = ttkb.Button(
                        parent,
                        text=drive,
                        image=self.icon_manager.get_icon('folder'),
                        compound=LEFT,
                        bootstyle="light",
                        command=lambda d=drive: self._navigate_to(d)
                    )
                    btn.pack(fill=X, pady=2)
            except Exception as e:
                logging.error(f"Could not load drives: {e}")
                
            
    def _add_quick_access_item(self, parent, name, path):
        """Add clickable item to quick access section"""
        btn = ttkb.Button(
            parent,
            text=name,
            image=self.icon_manager.get_icon('folder'),
            compound=LEFT,
            command=lambda p=path: self._navigate_or_open(p),
            bootstyle="light"
        )
        btn.pack(fill=X, pady=2)
        
            
    def _build_favorites_section(self):
        """Build the favorites section in sidebar"""
        favorites_frame = ttkb.Frame(self.sidebar_frame)
        favorites_frame.pack(fill=X, padx=5, pady=5)
        
        # Header with icon
        header = ttkb.Frame(favorites_frame)
        header.pack(fill=X)
        ttkb.Label(header, image=self.icon_manager.get_icon('favorites')).pack(side=LEFT)
        ttkb.Label(header, text="Favorites", font=('Helvetica', 9, 'bold')).pack(side=LEFT, padx=2)
        
        # Favorites list
        self.favorites_list = ttkb.Frame(favorites_frame)
        self.favorites_list.pack(fill=BOTH, expand=True)
        self._populate_favorites()
            
    def _populate_favorites(self):
        """Populate favorites in a scrollable vertical list"""
        for widget in self.favorites_inner.winfo_children():
            widget.destroy()

        for path in self.favorites:
            if not os.path.exists(path):
                continue  # Skip invalid favorites

            btn = ttkb.Button(
                self.favorites_inner,
                text=os.path.basename(path),
                image=self.icon_manager.get_file_icon(path),
                compound=LEFT,
                bootstyle="light",
                command=lambda p=path: self._navigate_or_open(p)
            )
            btn.pack(fill=X, pady=2)  # Fill width, small vertical padding
            btn.bind("<Button-3>", lambda e, p=path: self._show_favorite_context_menu(e, p))
            
            
    def _navigate_or_open(self, path):
        """Smart open that works for both files and folders"""
        if os.path.isdir(path):
            self._navigate_to(path)
        else:
            self._open_item(path)
            
                    
    def _show_favorite_context_menu(self, event, path):
        """Context menu for favorite items"""
        menu = ttkb.Menu(self, tearoff=0)
        menu.add_command(
            label="Remove from Favorites",
            command=lambda: self._remove_from_favorites(path)
        )
        menu.tk_popup(event.x_root, event.y_root)


    def _build_main_content(self, parent):
        """Build the main content area"""
        # Clear previous content
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        
        self.content_frame = ttkb.Frame(parent)
        parent.add(self.content_frame, weight=1)
        
        # Build components
        self._build_breadcrumb_bar()
        self._build_view_controls()
        
        # Create view container using grid
        self.view_container = ttkb.Frame(self.content_frame)
        self.view_container.pack(fill=BOTH, expand=True)  # Keep using pack here
        
        # Set up initial view
        if self.view_mode == 'list':
            self._setup_list_view()
        else:
            self._setup_grid_view()
                    
    def _navigate_back(self):
        """Navigate back in history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            self._update_nav_buttons()
            self._update_address_bar()
            self._refresh_view()

            
    def _build_breadcrumb_bar(self):
        """Create navigation bar with back/forward/up buttons"""
        self.breadcrumb_frame = ttkb.Frame(self.content_frame)
        self.breadcrumb_frame.pack(fill=X, pady=5)

        # Navigation buttons container
        nav_buttons = ttkb.Frame(self.breadcrumb_frame)
        nav_buttons.pack(side=LEFT)

        # Back button
        self.back_btn = ttkb.Button(
            nav_buttons,
            image=self.icon_manager.get_toolbar_icon('backward'),
            bootstyle="light",
            command=self._navigate_back,
            state='disabled'
        )
        self.back_btn.pack(side=LEFT, padx=2)

        # Forward button
        self.forward_btn = ttkb.Button(
            nav_buttons,
            image=self.icon_manager.get_toolbar_icon('forward'),
            bootstyle="light",
            command=self._navigate_forward,
            state='disabled'
        )
        self.forward_btn.pack(side=LEFT, padx=2)

        # Up button
        self.up_btn = ttkb.Button(
            nav_buttons,
            image=self.icon_manager.get_toolbar_icon('up'),
            bootstyle="light",
            command=self._navigate_up
        )
        self.up_btn.pack(side=LEFT, padx=2)

        # Address bar
        self.address_bar = ttkb.Frame(self.breadcrumb_frame)
        self.address_bar.pack(side=LEFT, fill=X, expand=True)
        self._update_address_bar()
            
    def _update_address_bar(self):
        """Update the clickable address bar"""
        for widget in self.address_bar.winfo_children():
            widget.destroy()
            
        path_components = self._split_path(self.current_path)
        
        for i, (name, full_path) in enumerate(path_components):
            if i > 0:
                ttkb.Label(self.address_bar, text=">").pack(side=LEFT, padx=2)
                
            btn = ttkb.Button(
                self.address_bar,
                text=name,
                bootstyle="link",
                command=lambda p=full_path: self._navigate_to(p)
            )
            btn.pack(side=LEFT)
                
    def _split_path(self, path):
        """Split path into clickable components"""
        components = []
        path = os.path.normpath(path)
        
        # Handle Windows drives differently
        if os.name == 'nt':
            if path.startswith('\\\\'):
                # Network path
                parts = path.split('\\')
                components.append((parts[0], '\\\\' + parts[2]))
                path = '\\'.join(parts[3:])
            else:
                # Local path
                drive, rest = os.path.splitdrive(path)
                if drive:
                    components.append((drive, drive + '\\'))
                    path = rest.lstrip('\\')
        
        parts = path.split(os.sep)
        current_path = components[-1][1] if components else ''
        
        for part in parts:
            if not part:
                continue
            current_path = os.path.join(current_path, part)
            # Handle Windows drive root properly
            if os.name == 'nt' and current_path.endswith(':\\'):
                components.append((current_path, current_path))
            else:
                components.append((part, current_path))
        
        return components


    def _create_grid_item(self, path, row, col):
        """Create a grid view item with interactive elements"""
        frame = ttkb.Frame(
            self.grid_frame,
            padding=5,
            bootstyle="light"
        )
        frame.path = path
        frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        frame.bind("<Button-3>", lambda e, p=path: self._on_grid_right_click(e, p))
        
        # Configure grid cell
        self.grid_frame.rowconfigure(row, weight=0)
        self.grid_frame.columnconfigure(col, weight=1, minsize=120)
        
        # Create icon
        icon = self.icon_manager.get_file_icon(path)
        icon_label = ttkb.Label(frame, image=icon)
        icon_label.image = icon  # Keep reference
        icon_label.pack(pady=2)
        
        # Create text label with elipsis
        name = os.path.basename(path)
        text_label = ttkb.Label(
            frame,
            text=name,
            wraplength=100,
            anchor="center",
            bootstyle="primary"
        )
        text_label.pack(fill=X, expand=True)
        
        # Selection highlight
        is_selected = path in self.selected_items
        frame.config(bootstyle="danger" if is_selected else "light")
        
        # Event bindings
        frame.bind("<Button-1>", lambda e, p=path: self._select_grid_item(p, frame))
        frame.bind("<Double-Button-1>", lambda e, p=path: self._open_item(p))
        text_label.bind("<Button-1>", lambda e, p=path: self._select_grid_item(p, frame))
        icon_label.bind("<Double-Button-1>", lambda e, p=path: self._open_item(p))
        frame.bind("<Button-3>", lambda e, p=path: self._select_grid_item(p, frame))
        
    # Add new handler method:
    def _on_grid_right_click(self, event, path):
        self.selected_items = [path]
        self._show_context_menu(event)


    def _select_grid_item(self, path, frame):
        """Handle selection of grid items (left or right click)"""
        if path not in self.selected_items:
            self.selected_items = [path]  # Single selection for context menu
        # Update visual selection
        self._refresh_grid_highlights()

    def _refresh_grid_highlights(self):
        """Update grid item highlights based on selection"""
        for child in self.grid_frame.winfo_children():
            if hasattr(child, 'path'):
                child.config(bootstyle="danger" if child.path in self.selected_items else "light")

    def _update_grid_view(self):
        """Optimized grid view update with dynamic columns"""
        # Clear previous items
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # Get directory contents
        try:
            items = os.listdir(self.current_path)
        except PermissionError:
            return
        
        # Create grid items in batches
        row = col = 0
        for idx, item in enumerate(items):
            full_path = os.path.join(self.current_path, item)
            self._create_grid_item(full_path, row, col)
            
            # Update grid position
            col += 1
            if col >= self.grid_columns:
                col = 0
                row += 1
            
            # Update periodically for better performance
            if idx % 10 == 0:
                self.update_idletasks()
        
        # Update scroll region
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))
        
    def _toggle_view_mode(self):
        """Switch between list and grid views"""
        # Clear current view
        for widget in self.view_container.winfo_children():
            widget.destroy()
        
        # Create new view
        if self.view_mode == 'list':
            self.view_mode = 'grid'
            self._setup_grid_view()
        else:
            self.view_mode = 'list'
            self._setup_list_view()
        
        # Re-establish bindings after view change
        self._setup_bindings()
        
        # Only refresh if UI is fully initialized
        if hasattr(self, 'status_label'):
            self._refresh_view()
                
    def _setup_grid_view(self):
        """Initialize grid view components with scrollable canvas"""
        # Clear previous grid widgets if they exist
        if hasattr(self, 'grid_scroll'):
            self.grid_scroll.destroy()
        if hasattr(self, 'grid_canvas'):
            self.grid_canvas.destroy()
        
        # Create canvas and scrollbar
        self.grid_canvas = ttkb.Canvas(
            self.view_container,
            background=self.theme_manager.style.colors.bg
        )
        self.grid_scroll = ttkb.Scrollbar(
            self.view_container,
            orient=VERTICAL,
            command=self.grid_canvas.yview
        )
        
        # Configure canvas scrolling
        self.grid_canvas.configure(yscrollcommand=self.grid_scroll.set)
        self.grid_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.grid_scroll.pack(side=RIGHT, fill=Y)
        
        # Create container frame for grid items
        self.grid_frame = ttkb.Frame(self.grid_canvas)
        self.grid_canvas.create_window((0, 0), window=self.grid_frame, anchor=NW)
        
        # Configure grid layout
        self.grid_columns = 6  # Initial number of columns
        self.grid_frame.grid_columnconfigure(tuple(range(self.grid_columns)), weight=1)
        
        # Set up event bindings
        self.grid_frame.bind(
            '<Configure>',
            lambda e: self.grid_canvas.configure(
                scrollregion=self.grid_canvas.bbox("all")
            )
        )
        
        # Bind mouse wheel scrolling
        self.grid_canvas.bind_all("<MouseWheel>", self._on_grid_mousewheel)
        
        # Bind resize handling
        self.grid_canvas.bind('<Configure>', self._handle_grid_resize)
        
    def _on_grid_mousewheel(self, event):
        """Handle mouse wheel scrolling for grid view"""
        self.grid_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        
        
    def _handle_grid_resize(self, event=None):
        """Handle window resize by recalculating grid columns"""
        if not hasattr(self, 'grid_canvas'):
            return
            
        canvas_width = self.grid_canvas.winfo_width()
        min_item_width = 150  # Minimum width per grid item
        new_columns = max(1, canvas_width // min_item_width)
        
        if new_columns != self.grid_columns:
            self.grid_columns = new_columns
            self._update_grid_view()


    def _setup_list_view(self):
        """Initialize list view components"""
        # Create list view with scrollbars
        self.list_view = ttkb.Treeview(
            self.view_container,
            columns=('size', 'type', 'modified'),
            show='tree headings',
            bootstyle="primary",
            selectmode='extended'  # Allow multiple selection
        )
        self._configure_list_view_columns()
        
        # Vertical scrollbar
        yscroll = ttkb.Scrollbar(
            self.view_container,
            orient=VERTICAL,
            command=self.list_view.yview
        )
        self.list_view.configure(yscrollcommand=yscroll.set)

        # Horizontal scrollbar
        xscroll = ttkb.Scrollbar(
            self.view_container,
            orient=HORIZONTAL,
            command=self.list_view.xview
        )
        self.list_view.configure(xscrollcommand=xscroll.set)

        # Grid layout
        self.list_view.grid(row=0, column=0, sticky='nsew')
        yscroll.grid(row=0, column=1, sticky='ns')
        xscroll.grid(row=1, column=0, sticky='ew', columnspan=2)
        
        # Configure grid weights
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.list_view.bind('<<TreeviewSelect>>', self._on_selection_change)
        self.list_view.bind('<Double-1>', self._on_item_double_click)
        
        # Immediately populate the view
        self._update_list_view()
            
    def _build_view_controls(self):
        """Create view mode controls"""
        self.view_controls = ttkb.Frame(self.content_frame)
        self.view_controls.pack(fill=X, pady=2)


    def _build_file_display(self):
        """Build the file display area"""
        self.view_container = ttkb.Frame(self.content_frame)
        self.view_container.pack(fill=BOTH, expand=True)

        # List View (Treeview)
        self.list_view = ttkb.Treeview(
            self.view_container,
            columns=('size', 'type', 'modified'),
            show='tree headings',
            bootstyle="primary"
        )
        self._configure_list_view_columns()

        # Grid View (Canvas)
        self.grid_canvas = ttkb.Canvas(self.view_container)
        self.grid_scroll = ttkb.Scrollbar(
            self.view_container,
            orient=VERTICAL,
            command=self.grid_canvas.yview
        )
        self.grid_canvas.configure(yscrollcommand=self.grid_scroll.set)
        self._toggle_view_mode()
        
    def _configure_list_view_columns(self):
        """Configure list view columns with optimal display settings"""
        # Configure columns with improved settings
        columns = {
            '#0': {
                'text': 'Name',
                'anchor': W,
                'width': 350,  # Wider for better filename display
                'stretch': True,
                'minwidth': 150,
                'ellipsis': True  # Add ellipsis for long names
            },
            'size': {
                'text': 'Size',
                'anchor': E,
                'width': 120,
                'stretch': False
            },
            'type': {
                'text': 'Type',
                'anchor': W,
                'width': 150,
                'stretch': False
            },
            'modified': {
                'text': 'Modified',
                'anchor': W,
                'width': 180,
                'stretch': False
            }
        }

        # Apply column configurations
        for col, config in columns.items():
            self.list_view.heading(
                col,
                text=config['text'],
                anchor=config['anchor'],
                command=lambda c=col: self._sort_by_column(c)
            )
            self.list_view.column(
                col,
                width=config['width'],
                anchor=config['anchor'],
                stretch=config.get('stretch', False),
                minwidth=config.get('minwidth', 50)
            )
            if config.get('ellipsis'):
                self.list_view.column(col, stretch=False)  # Required for ellipsis

        # Configure styling - only once
        style = self.theme_manager.style
        
        # Base style
        style.configure(
            'Treeview',
            background=style.colors.bg,
            foreground=style.colors.fg,
            fieldbackground=style.colors.bg,
            font=('Segoe UI', 10),
            rowheight=28  # Ample space for icons
        )
        
        # Heading style
        style.configure(
            'Treeview.Heading',
            font=('Segoe UI', 10, 'bold'),
            background=style.colors.secondary,
            foreground=style.colors.fg
        )

        # Configure tags for automatic application
        self.list_view.tag_configure(
            'directory',
            font=('Segoe UI', 10, 'bold'),
            foreground=style.colors.primary
        )
        self.list_view.tag_configure(
            'hidden',
            foreground=style.colors.secondary
        )
        
        # Critical: Ensure icons will display
        self.list_view['show'] = 'tree headings'  # Shows both tree lines and icons
        
        # Configure item padding for proper icon alignment
        style.layout(
            'Treeview.Item',
            [('Treeitem.padding', {
                'sticky': 'nswe',
                'children': [
                    ('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                    ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                    ('Treeitem.text', {'side': 'left', 'sticky': ''})
                ]
            })]
        )        

    def _create_new_folder(self):
        """Create a new folder in current directory"""
        folder_name = simpledialog.askstring(
            "New Folder", 
            "Enter folder name:", 
            parent=self
        )
        if folder_name:
            try:
                new_path = os.path.join(self.current_path, folder_name)
                os.mkdir(new_path)
                self._refresh_view()
                self.status_label.config(text=f"Created folder: {folder_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder: {str(e)}")


   
                    
    def _build_statusbar(self, parent):
        """Create the status bar"""
        self.status_frame = ttkb.Frame(parent)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label (left-aligned)
        self.status_label = ttkb.Label(
            self.status_frame, 
            text="Ready",
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Selected items label (right-aligned)
        self.selected_label = ttkb.Label(
            self.status_frame,
            text="Selected: 0 items"
        )
        self.selected_label.pack(side=tk.RIGHT, padx=5)
        
    def _setup_bindings(self):
        """Configure all keyboard and mouse bindings"""
        # Keyboard shortcuts (removed dir_tree binding)
        self.bind("<F5>", lambda e: self._refresh_view())
        self.bind("<Delete>", lambda e: self._delete_selected())
        self.bind("<Control-n>", lambda e: self._create_new_folder())
        self.bind("<Control-q>", lambda e: self.quit())
        
        # Treeview bindings (if list view exists)
        if hasattr(self, 'list_view') and self.list_view.winfo_exists():
            self.list_view.bind("<<TreeviewSelect>>", self._on_selection_change)
            self.list_view.bind("<Double-1>", self._on_item_double_click)
            self.list_view.bind("<Button-3>", self._show_context_menu)
        
        # Grid view bindings
        if hasattr(self, 'grid_canvas') and self.grid_canvas.winfo_exists():
            self.grid_canvas.bind("<Button-3>", self._show_context_menu)
        
        # Navigation
        self.bind("<Alt-Left>", lambda e: self._navigate_back())
        self.bind("<Alt-Right>", lambda e: self._navigate_forward())
   
    def _populate_directory_tree(self):
        """Populate sidebar tree with directory structure"""
        self.dir_tree.delete(*self.dir_tree.get_children())
        root = self.dir_tree.insert('', 'end', text="This PC", open=True)
        
        # Add drives (Windows specific)
        if os.name == 'nt':
            import win32api
            drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
            for drive in drives:
                self.dir_tree.insert(root, 'end', text=drive, values=(drive,))
        
        # Add user home directory
        home = os.path.expanduser("~")
        home_node = self.dir_tree.insert(root, 'end', text="Home", values=(home,))
        
        # Add common folders
        for folder in ['Desktop', 'Documents', 'Downloads']:
            path = os.path.join(home, folder)
            if os.path.exists(path):
                self.dir_tree.insert(home_node, 'end', text=folder, values=(path,))


    def _refresh_view(self):
        """Refresh current directory view"""
        self.selected_items.clear()
        self.selected_label.config(text="Selected: 0 items")
        
        if self.view_mode == 'list':
            self._update_list_view()
        else:
            self._update_grid_view()
        
        self.status_label.config(text=f"Loaded {self.current_path}")
        
    def _update_list_view(self):
        """Optimized list view update"""
        # Clear existing items
        self.list_view.delete(*self.list_view.get_children())
        
        # Get directory contents
        try:
            items = os.listdir(self.current_path)
            print(f"Found {len(items)} items in {self.current_path}") 
        except PermissionError:
            print(f"Error reading directory: {str(e)}")  # Debug output
            messagebox.showerror("Access Denied", "You don't have permission to view this directory")
            return
        
        # Insert items with proper tags and icons
        for item in items:
            full_path = os.path.join(self.current_path, item)
            try:
                is_dir = os.path.isdir(full_path)
                size = self._format_size(os.path.getsize(full_path)) if not is_dir else "<DIR>"
                if is_dir:
                    file_type = 'Folder'
                else:
                    ext = os.path.splitext(item)[1].upper()
                    file_type = ext[1:] if ext else 'File'
                modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M')
                
                # Get the appropriate icon
                icon = self.icon_manager.get_file_icon(full_path)
                
                # Insert the item with all properties
                self.list_view.insert('', 'end', 
                    text=item,
                    values=(size, file_type, modified),
                    tags=(full_path,),
                    image=icon
                )
                
            except (OSError, PermissionError) as e:
                logging.warning(f"Could not access {full_path}: {str(e)}")
                continue       
        
    def _add_list_item(self, path):
        """Add an item to the list view"""
        is_dir = os.path.isdir(path)
        name = os.path.basename(path)
        size = self._format_size(os.path.getsize(path)) if not is_dir else "<DIR>"
        file_type = 'Folder' if is_dir else 'File'
        modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
        
        self.list_view.insert('', 'end',
            text=name,  # This populates the #0 column
            values=(size, file_type, modified),
            tags=(path,),
            image=self.icon_manager.get_file_icon(path)  # Add icon if needed
        )
        
    def _format_size(self, size):        
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    

    def _update_nav_buttons(self):
        """Update back/forward button states"""
        self.back_btn['state'] = 'normal' if self.history_index > 0 else 'disabled'
        self.forward_btn['state'] = 'normal' if self.history_index < len(self.history)-1 else 'disabled'

    def _navigate_forward(self):
        """Navigate forward in history"""
        if self.history_index < len(self.history)-1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            self._update_nav_buttons()
            self._update_address_bar()
            self._refresh_view()

    def _navigate_up(self):
        """Navigate to parent directory"""
        parent = os.path.dirname(self.current_path)
        if os.path.exists(parent):
            self._navigate_to(parent)
                  
    def _select_item(self, path):
        """Handle item selection in grid view"""
        if path in self.selected_items:
            self.selected_items.remove(path)
        else:
            self.selected_items.append(path)
        self.selected_label.config(text=f"Selected: {len(self.selected_items)} items")

    def _open_item(self, path):
        """Open files with default application, folders in explorer"""
        try:
            if os.path.isdir(path):
                self._navigate_to(path)
            else:
                if platform.system() == 'Windows':
                    os.startfile(path)
                elif platform.system() == 'Darwin':
                    subprocess.run(['open', path])
                else:
                    subprocess.run(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Open Error", f"Could not open: {str(e)}")
        
        
    def _delete_selected(self):
        """Delete selected items with confirmation"""
        if not self.selected_items:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(self.selected_items)} selected items?",
            parent=self
        )
        if not confirm:
            return

        failed_deletions = []
        for path in self.selected_items:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                failed_deletions.append(f"{os.path.basename(path)}: {str(e)}")

        if failed_deletions:
            messagebox.showerror(
                "Deletion Errors",
                "Failed to delete:\n\n" + "\n".join(failed_deletions))
        self._refresh_view()

    def _copy_items(self):
        """Copy selected items to clipboard"""
        if self.selected_items:
            self.clipboard = {
                'operation': 'copy',
                'paths': self.selected_items.copy()
            }
            self.status_label.config(text=f"Copied {len(self.selected_items)} items")

    def _cut_items(self):
        """Cut selected items to clipboard"""
        if self.selected_items:
            self.clipboard = {
                'operation': 'cut',
                'paths': self.selected_items.copy()
            }
            self.status_label.config(text=f"Cut {len(self.selected_items)} items")

    def _paste_items(self):
        """Paste items from clipboard"""
        if not self.clipboard or not self.clipboard['paths']:
            return

        operation = self.clipboard['operation']
        success_count = 0
        failed_items = []

        for src_path in self.clipboard['paths']:
            try:
                dest_path = os.path.join(
                    self.current_path,
                    os.path.basename(src_path))
                
                if operation == 'copy':
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                    success_count += 1
                elif operation == 'cut':
                    shutil.move(src_path, dest_path)
                    success_count += 1
            except Exception as e:
                failed_items.append(f"{os.path.basename(src_path)}: {str(e)}")

        # Clear clipboard after cut operation
        if operation == 'cut':
            self.clipboard = None

        # Show results
        msg = f"Successfully {operation}ied {success_count} items"
        if failed_items:
            msg += f"\nFailed: {len(failed_items)} items"
            messagebox.showwarning(
                "Paste Errors",
                "Could not paste:\n\n" + "\n".join(failed_items))
        self.status_label.config(text=msg)
        self._refresh_view()

    def _show_theme_selector(self):
        """Show theme selection dialog"""
        dialog = ttkb.Toplevel(self)
        dialog.title("Select Theme")
        dialog.transient(self)

        themes = self.theme_manager.get_theme_names()
        selected_theme = ttkb.StringVar(value=self.theme_manager.current_theme)

        ttkb.Label(dialog, text="Choose a theme:").pack(pady=5)
        theme_list = ttkb.Combobox(
            dialog,
            textvariable=selected_theme,
            values=themes,
            state='readonly'
        )
        theme_list.pack(padx=10, pady=5)
        theme_list.bind('<<ComboboxSelected>>', 
                    lambda e: self._apply_theme(selected_theme.get()))

        ttkb.Button(dialog, 
                text="Apply",
                command=lambda: self._apply_theme(selected_theme.get()),
                bootstyle="primary").pack(pady=5)

    def _apply_theme(self, theme_name):
        """Apply selected theme to the application"""
        self.theme_manager.apply_theme(theme_name)
        self._refresh_view()
        self.status_label.config(text=f"Theme changed to {theme_name}")

    def _show_context_menu(self, event):
        """Display right-click context menu with favorite options"""
        menu = ttkb.Menu(self, tearoff=0)
        clicked_path = None

        # Detect clicked item based on view mode
        if self.view_mode == 'list':
            item = self.list_view.identify_row(event.y)
            if item:
                clicked_path = self.list_view.item(item, 'tags')[0]
        elif self.view_mode == 'grid':
            # Find grid item frame containing the path
            widget = event.widget.winfo_containing(event.x, event.y)
            while widget and not hasattr(widget, 'path'):
                widget = widget.master
            clicked_path = getattr(widget, 'path', None)

        # Validate the path exists
        valid_path = clicked_path and os.path.exists(clicked_path)

        # Build menu items
        if valid_path:
            # Update selection if needed
            if clicked_path not in self.selected_items:
                self.selected_items = [clicked_path]

            # Standard context menu items
            menu.add_command(
                label="Open",
                command=lambda: self._open_item(clicked_path)
            )
            menu.add_separator()
            menu.add_command(label="Copy", command=self._copy_items)
            menu.add_command(label="Cut", command=self._cut_items)
            menu.add_command(label="Paste", command=self._paste_items)
            menu.add_separator()
            menu.add_command(label="Delete", command=self._delete_selected)
            menu.add_command(
                label="Rename",
                command=lambda: self._rename_item(clicked_path)
            )
            menu.add_command(
                label="Properties",
                command=lambda: self._show_properties(clicked_path)
            )
            
            # Favorite section
            menu.add_separator()
            favorite_label = ("Remove from Favorites" 
                            if clicked_path in self.favorites 
                            else "Add to Favorites")
            menu.add_command(
                label=favorite_label,
                command=lambda: self._toggle_favorite(clicked_path)
            )
        else:
            # Empty space menu
            menu.add_command(
                label="New Folder", 
                command=self._create_new_folder
            )
            menu.add_command(
                label="Paste", 
                command=self._paste_items,
                state='normal' if self.clipboard else 'disabled'
            )
            menu.add_separator()
            menu.add_command(label="Refresh", command=self._refresh_view)

        # Show the menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()


    def _create_new_folder(self):
        """Create new folder in current directory"""
        folder_name = simpledialog.askstring(
            "New Folder",
            "Enter folder name:",
            parent=self
        )
        if folder_name:
            try:
                path = os.path.join(self.current_path, folder_name)
                os.mkdir(path)
                self._refresh_view()
                self.status_label.config(text=f"Created folder: {folder_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder: {str(e)}")

    def _rename_item(self, old_path):
        """Rename a file or folder"""
        new_name = simpledialog.askstring(
            "Rename",
            "Enter new name:",
            initialvalue=os.path.basename(old_path),
            parent=self
        )
        if new_name:
            try:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                self._refresh_view()
                self.status_label.config(text="Renamed successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename: {str(e)}")

    def _show_properties(self, path):
        """Display file/folder properties dialog"""
        stat = os.stat(path)
        is_dir = os.path.isdir(path)
        
        # Create properties dialog
        dialog = ttkb.Toplevel(self)
        dialog.title("Properties")
        dialog.transient(self)
        dialog.resizable(False, False)
        
        # Main content frame
        content = ttkb.Frame(dialog, padding=10)
        content.pack(fill=BOTH, expand=True)

        # File icon and name
        icon = self.icon_manager.get_file_icon(path)
        ttkb.Label(content, image=icon).grid(row=0, column=0, rowspan=4, padx=10, sticky=N)
        ttkb.Label(content, text=os.path.basename(path), font='TkDefaultFont 11 bold').grid(row=0, column=1, sticky=W)
        
        # Basic information
        info = {
            "Type": "Folder" if is_dir else "File",
            "Location": os.path.dirname(path),
            "Size": self._format_size(stat.st_size) if not is_dir else "",
            "Contains": f"{len(os.listdir(path))} items" if is_dir else "",
            "Created": datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M'),
            "Modified": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
            "Accessed": datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M')
        }

        # Permission information
        if os.name != 'nt':  # Unix permissions
            mode = stat.st_mode
            perms = {
                "Owner": f"{(mode & 0o700) >> 6:03o}",
                "Group": f"{(mode & 0o070) >> 3:03o}",
                "Others": f"{mode & 0o007:03o}"
            }
            info["Permissions"] = "-".join(perms.values())

        # Create info labels
        row = 1
        for key, value in info.items():
            if not value:
                continue
            ttkb.Label(content, text=f"{key}:").grid(row=row, column=1, sticky=E, padx=5)
            ttkb.Label(content, text=value).grid(row=row, column=2, sticky=W, padx=5)
            row += 1

        # Add separator
        ttkb.Separator(content).grid(row=row, column=0, columnspan=3, pady=10, sticky=EW)
        row += 1

        # Advanced button
        ttkb.Button(
            content,
            text="Advanced...",
            command=lambda: self._show_advanced_properties(path)
        ).grid(row=row, column=2, sticky=E, pady=5)

        # Center dialog
        self._center_window(dialog)

    def _show_advanced_properties(self, path):
        """Display advanced system properties"""
        # Implement platform-specific advanced properties
        messagebox.showinfo(
            "Advanced Properties",
            "Advanced properties not implemented in this version"
        )

    def _center_window(self, window):
        """Center a window relative to main window"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = self.winfo_x() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (height // 2)
        window.geometry(f"+{x}+{y}")

    def _start_search(self, event=None):
        """Start search with guaranteed widget initialization"""
        # Ensure dialog exists
        self._show_search_dialog()
        
        # Clear previous results
        self.results_list.delete(*self.results_list.get_children())
        
        # Rest of your search logic...
        search_term = self.search_entry.get().lower()
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term")
            return
        
        self.search_running = True
        self.search_cancel = False
        self.search_progress.start()
        
        threading.Thread(
            target=self._perform_search,
            args=(search_term,),
            daemon=True
        ).start()
        
    
    def _perform_search(self, search_term):
        """Background file search implementation"""
        matches = []
        
        try:
            for root, dirs, files in os.walk(self.current_path):
                if self.search_cancel:
                    break
                    
                # Check directory names
                if search_term in root.lower():
                    matches.append((
                        os.path.basename(root),
                        root,
                        'Folder'
                    ))
                    
                # Check files
                for f in files:
                    if self.search_cancel:
                        break
                    if search_term in f.lower():
                        matches.append((
                            f,
                            os.path.join(root, f),
                            'File'
                        ))
                        
                    # Update UI periodically
                    if len(matches) % 10 == 0:
                        self.after(0, self._update_search_results, matches.copy())
                        matches.clear()
            
            # Update final results
            self.after(0, self._update_search_results, matches)
            
        except Exception as e:
            self.after(0, messagebox.showerror, 
                    "Search Error", str(e))
        finally:
            self.after(0, self._end_search)
            
        
    def _update_search_results(self, matches):
        """Update UI with search results"""
        for name, path, type_ in matches:
            self.results_list.insert('', END, 
                text=name,
                values=(path, type_)
            )

    def _end_search(self):
        """Clean up after search completes"""
        self.search_progress.stop()
        self.search_running = False
        if not self.search_cancel:
            count = len(self.results_list.get_children())
            self.status_label.config(text=f"Found {count} matches")

    def _navigate_back(self):
        """Navigate to parent directory"""
        parent = os.path.dirname(self.current_path)
        if os.path.exists(parent):
            self._navigate_to(parent)

    def _on_item_double_click(self, event):
        """Handle double-click in list view"""
        item = self.list_view.selection()[0]
        path = self.list_view.item(item, 'tags')[0]
        self._open_item(path)

    def _save_preferences(self):
        """Save user preferences to config file"""
        config = {
            'theme': self.theme_manager.current_theme,
            'view_mode': self.view_mode,
            'window_size': self.geometry(),
            'last_directory': self.current_path
        }
        
        config_dir = os.path.join(os.path.expanduser("~"), ".fluentexplorer")
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, "prefs.json"), 'w') as f:
            json.dump(config, f, indent=2)

    def _load_preferences(self):
        """Load user preferences from config file"""
        config_path = os.path.join(
            os.path.expanduser("~"), 
            ".fluentexplorer",
            "prefs.json"
        )
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Apply preferences
            self.theme_manager.apply_theme(config.get('theme', 'litera'))
            self.view_mode = config.get('view_mode', 'list')
            self.geometry(config.get('window_size', '1200x800'))
            self.current_path = config.get('last_directory', os.path.expanduser("~"))
            
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _on_close(self):
        """Handle window close event"""
        try:
            self._save_preferences()
            if hasattr(self, 'search_dialog') and self.search_dialog.winfo_exists():
                self.search_dialog.destroy()
            self.destroy()
        except Exception as e:
            logging.error(f"Close error: {str(e)}")
            self.destroy()
            
              
    def _show_about(self):
        """Display about dialog"""
        about_dialog = ttkb.Toplevel(self)
        about_dialog.title("About Fluent Explorer")
        about_dialog.resizable(False, False)
        
        content = ttkb.Frame(about_dialog, padding=10)
        content.pack(fill=BOTH, expand=True)

        # Application icon
        ttkb.Label(content, 
                image=self.icon_manager.get_icon('info'),
                bootstyle=PRIMARY).pack(pady=5)

        # Application info
        info = [
            ("Fluent Explorer", 'title'),
            ("Version 1.0.0", ''),
            ("File Manager for Modern Windows", ''),
            ("\nDeveloped using Python and ttkbootstrap", ''),
            ("Icons by Feather Icons", '')
        ]

        for text, style in info:
            ttkb.Label(content, 
                    text=text, 
                    font=('Helvetica', 11) if style == 'title' else None
                    ).pack(pady=2)

        # Close button
        ttkb.Button(
            about_dialog,
            text="Close",
            command=about_dialog.destroy,
            bootstyle=PRIMARY
        ).pack(pady=10)

        self._center_window(about_dialog)

    def _toggle_dark_mode(self):
        """Toggle between light/dark base themes"""
        current = self.theme_manager.current_theme
        new_theme = 'cyborg' if 'light' in current.lower() else 'litera'
        self._apply_theme(new_theme)

    def _create_keybindings(self):
        """Set up additional keyboard shortcuts"""
        self.bind('<Control-q>', lambda e: self._on_close())
        self.bind('<Control-t>', lambda e: self._toggle_dark_mode())
        self.bind('<Alt-Left>', lambda e: self._navigate_back())
        self.bind('<Alt-Right>', lambda e: self._navigate_forward())


    def _validate_path(self, path):
        """Security: Validate path before operations"""
        try:
            return os.path.abspath(path).startswith(
                os.path.abspath(self.current_path)
            )
        except:
            return False

    def _show_operation_progress(self, title):
        """Show progress dialog for long operations"""
        dialog = ttkb.Toplevel(self)
        dialog.title(title)
        dialog.transient(self)
        
        ttkb.Label(dialog, text="Operation in progress...").pack(pady=5)
        progress = ttkb.Progressbar(dialog, mode='indeterminate')
        progress.pack(pady=5)
        progress.start()
        
        return dialog, progress

    def _handle_operation_error(self, error, context=""):
        """Central error handling with logging"""
        error_msg = f"{context}: {str(error)}" if context else str(error)
        logging.error(error_msg)
        messagebox.showerror("Operation Failed", error_msg)

    def _refresh_ui_theme(self):
        """Force UI elements to update theme"""
        self._build_ui()
        self._refresh_view()

    def _create_system_tray_icon(self):
        """Create system tray icon (Windows only)"""
        if os.name == 'nt':
            try:
                from infi.systray import SysTrayIcon
                menu_options = (("Open", None, lambda: self.deiconify()),)
                self.tray_icon = SysTrayIcon(
                    "assets/icon.ico",
                    "Fluent Explorer",
                    menu_options,
                    on_quit=self._on_close
                )
                self.tray_icon.start()
            except ImportError:
                pass

    def _minimize_to_tray(self):
        """Minimize window to system tray"""
        if hasattr(self, 'tray_icon'):
            self.withdraw()
        else:
            self.iconify()

    def _create_autostart_entry(self):
        """Create autostart entry (Windows only)"""
        if os.name == 'nt':
            autostart_path = os.path.join(
                os.getenv('APPDATA'),
                'Microsoft\\Windows\\Start Menu\\Programs\\Startup',
                'FluentExplorer.lnk'
            )
            
            if not os.path.exists(autostart_path):
                try:
                    import winshell
                    winshell.CreateShortcut(
                        Path=autostart_path,
                        Target=sys.executable,
                        Arguments=__file__,
                        Description="Fluent Explorer File Manager"
                    )
                except ImportError:
                    pass

    def _optimize_performance(self):
        """Apply performance optimizations"""
        # Disable visual effects during bulk operations
        self.list_view.configure(displaycolumns=('#0', 'size'))  # Fewer columns
        self.grid_canvas.configure(background=self.theme_manager.style.colors.bg)

    def _clear_cache(self):
        """Clear temporary caches"""
        self.icon_manager.cache.clear()
        self._refresh_view()

    def _create_zip_archive(self):
        """Create ZIP archive from selected items"""
        if not self.selected_items:
            return
            
        zip_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP Archive", "*.zip")]
        )
        
        if zip_path:
            try:
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for path in self.selected_items:
                        if os.path.isdir(path):
                            for root, dirs, files in os.walk(path):
                                for file in files:
                                    zipf.write(
                                        os.path.join(root, file),
                                        os.path.relpath(
                                            os.path.join(root, file),
                                            os.path.dirname(path)
                                        )
                                    )
                        else:
                            zipf.write(path, os.path.basename(path))
                            
                self.status_label.config(text="Archive created successfully")
            except Exception as e:
                self._handle_operation_error(e, "Archive creation failed")

    def _create_shortcut(self):
        """Create shortcut to selected item (Windows only)"""
        if os.name == 'nt' and self.selected_items:
            try:
                import winshell
                target = self.selected_items[0]
                shortcut_path = filedialog.asksaveasfilename(
                    defaultextension=".lnk",
                    filetypes=[("Shortcut", "*.lnk")]
                )
                
                if shortcut_path:
                    winshell.CreateShortcut(
                        Path=shortcut_path,
                        Target=target,
                        Description="Created by Fluent Explorer"
                    )
                    self.status_label.config(text="Shortcut created")
            except ImportError:
                messagebox.showerror("Error", "Windows shell integration required")

    def _show_clipboard_info(self):
        """Display clipboard status in status bar"""
        if self.clipboard:
            op = self.clipboard['operation'].capitalize()
            count = len(self.clipboard['paths'])
            self.status_label.config(text=f"{op}ing {count} items")
        else:
            self.status_label.config(text="Clipboard empty")

    def _reset_ui_layout(self):
        """Reset UI to default layout"""
        self.geometry("1200x800")
        self.view_mode = 'list'
        self._refresh_ui_theme()
        self.status_label.config(text="UI layout reset")

    def _create_file_menu(self):
        """Create right-click file menu"""
        self.file_menu = ttkb.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open", command=self._open_selected)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Cut", command=self._cut_items)
        self.file_menu.add_command(label="Copy", command=self._copy_items)
        self.file_menu.add_command(label="Paste", command=self._paste_items)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Delete", command=self._delete_selected)
        self.file_menu.add_command(label="Rename", command=self._rename_selected)

    def _open_selected(self):
        if self.selected_items:
            self._open_item(self.selected_items[0])

    def _rename_selected(self):
        if self.selected_items:
            self._rename_item(self.selected_items[0])

    def _show_help(self):
        """Display help documentation"""
        webbrowser.open("https://github.com/fluent-explorer/docs")
   
    def _sort_by_column(self, col):
        """Sort treeview contents when a column header is clicked"""
        # Get current sort order
        current_sort = self.list_view.heading(col)['text'][-1]
        
        # Toggle ascending/descending order
        new_sort = '▼' if current_sort != '▼' else '▲'
        
        # Update column header
        self.list_view.heading(col, text=f"{self.list_view.heading(col)['text'].rstrip('▼▲')} {new_sort}")
        
        # Get items differently for name column (#0)
        if col == '#0':
            # Use item text for name column
            items = [(self.list_view.item(child, 'text'), child)
                    for child in self.list_view.get_children('')]
        else:
            # Use standard set() for other columns
            items = [(self.list_view.set(child, col), child)
                    for child in self.list_view.get_children('')]

        # Special sorting for different columns
        if col == 'size':
            # Convert size to bytes for proper sorting
            items.sort(key=lambda x: self._parse_size(x[0]), reverse=(new_sort == '▲'))
        elif col == 'modified':
            # Convert to datetime objects for proper sorting
            items.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M'), reverse=(new_sort == '▲'))
        else:  # For name (#0) and type columns
            # Natural sorting for strings
            items.sort(key=lambda x: x[0].lower(), reverse=(new_sort == '▲'))

        # Rearrange items in treeview
        for index, (_, child) in enumerate(items):
            self.list_view.move(child, '', index)

    def _parse_size(self, size_str):
        """Convert human-readable size to bytes"""
        units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 
                'GB': 1024**3, 'TB': 1024**4, 'PB': 1024**5}
        if size_str == '<DIR>':
            return -1  # Directories come first in sorting
        try:
            number, unit = size_str.split()
            return float(number) * units[unit]
        except:
            return 0

if __name__ == "__main__":
    try:
        app = FileExplorer()
        app.mainloop()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        if 'bad window path name' in str(e):
            messagebox.showerror(
                "UI Error", 
                "Application interface corrupted. Please restart."
            )
            
