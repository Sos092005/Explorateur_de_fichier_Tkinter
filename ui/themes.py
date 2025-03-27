import json
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional


class ThemeError(Exception):
    """Exception personnalisée pour les erreurs de thème"""
    pass


class ThemeManager:
    def __init__(self, preferences_file: str = "preferences.json"):
        self.preferences_file = preferences_file
        self.current_theme = None
        self.available_themes = {
            "clair": {
                "background": "#ffffff",
                "foreground": "#000000",
                "highlight": "#e1e1e1",
                "text": "#333333",
                "treeview_bg": "#f8f8f8",
                "treeview_fg": "#222222",
                "treeview_highlight": "#e0e0e0",
                "treeview_even": "#f5f5f5",
                "treeview_odd": "#ffffff"
            },
            "sombre": {
                "background": "#2d2d2d",
                "foreground": "#e0e0e0",
                "highlight": "#3d3d3d",
                "text": "#f0f0f0",
                "treeview_bg": "#252525",
                "treeview_fg": "#e0e0e0",
                "treeview_highlight": "#3a3a3a",
                "treeview_even": "#2a2a2a",
                "treeview_odd": "#333333"
            },
            "bleu": {
                "background": "#e6f2ff",
                "foreground": "#003366",
                "highlight": "#cce0ff",
                "text": "#001a33",
                "treeview_bg": "#d9e6ff",
                "treeview_fg": "#00264d",
                "treeview_highlight": "#b3d1ff",
                "treeview_even": "#e6f0ff",
                "treeview_odd": "#d9e6ff"
            }
        }

        # Charger les préférences au démarrage
        self.load_preferences()

    def validate_theme(self, theme: Dict) -> bool:
        """Valide qu'un thème contient toutes les clés nécessaires"""
        required_keys = {
            "background", "foreground", "highlight", "text",
            "treeview_bg", "treeview_fg", "treeview_highlight",
            "treeview_even", "treeview_odd"
        }
        return all(key in theme for key in required_keys)

    def apply_theme(self, root: tk.Tk, theme_name: str) -> None:
        """Applique un thème à l'ensemble de l'application"""
        if theme_name not in self.available_themes:
            raise ThemeError(f"Thème '{theme_name}' non disponible")

        theme = self.available_themes[theme_name]

        if not self.validate_theme(theme):
            raise ThemeError("Structure de thème invalide")

        self.current_theme = theme_name

        # Appliquer le thème aux widgets de base
        root.configure(bg=theme["background"])

        # Style global pour ttk
        style = ttk.Style()
        style.theme_use("clam")  # Thème de base qui permet une bonne personnalisation

        # Configuration des widgets ttk
        style.configure(".",
                        background=theme["background"],
                        foreground=theme["foreground"],
                        fieldbackground=theme["background"],
                        insertcolor=theme["foreground"])

        style.configure("TFrame", background=theme["background"])
        style.configure("TLabel", background=theme["background"], foreground=theme["text"])
        style.configure("TButton",
                        background=theme["highlight"],
                        foreground=theme["text"],
                        borderwidth=1,
                        relief="raised")
        style.configure("TEntry",
                        fieldbackground=theme["background"],
                        foreground=theme["text"],
                        insertcolor=theme["text"])

        # Configuration spécifique pour Treeview
        style.configure("Treeview",
                        background=theme["treeview_bg"],
                        foreground=theme["treeview_fg"],
                        fieldbackground=theme["treeview_bg"],
                        rowheight=25)

        style.map("Treeview",
                  background=[("selected", theme["treeview_highlight"])],
                  foreground=[("selected", theme["treeview_fg"])])

        # Sauvegarder le thème appliqué
        self.save_preferences()

    def load_preferences(self) -> Optional[str]:
        """Charge les préférences de thème depuis le fichier de configuration"""
        try:
            with open(self.preferences_file, "r") as f:
                preferences = json.load(f)
                theme = preferences.get("theme")
                if theme in self.available_themes:
                    return theme
        except FileNotFoundError:
            print("Fichier de préférences non trouvé, utilisation du thème par défaut")
        except json.JSONDecodeError:
            print("Erreur de décodage JSON, fichier de préférences peut-être corrompu")
        except Exception as e:
            print(f"Erreur inattendue lors du chargement des préférences: {e}")

        return None

    def save_preferences(self) -> None:
        """Sauvegarde les préférences de thème dans le fichier de configuration"""
        try:
            preferences = {"theme": self.current_theme}
            with open(self.preferences_file, "w") as f:
                json.dump(preferences, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des préférences: {e}")

    def get_current_theme(self) -> Dict:
        """Retourne le thème actuellement appliqué"""
        return self.available_themes.get(self.current_theme, self.available_themes["clair"])

    def get_theme_names(self) -> list:
        """Retourne la liste des noms de thèmes disponibles"""
        return list(self.available_themes.keys())


# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestionnaire de thèmes")
    root.geometry("400x300")

    theme_manager = ThemeManager()

    # Charger le dernier thème utilisé
    saved_theme = theme_manager.load_preferences()
    if saved_theme:
        theme_manager.apply_theme(root, saved_theme)
    else:
        theme_manager.apply_theme(root, "clair")

    # Frame pour les boutons de thème
    frame = ttk.Frame(root)
    frame.pack(pady=20)

    # Boutons pour changer de thème
    for theme_name in theme_manager.get_theme_names():
        btn = ttk.Button(
            frame,
            text=theme_name.capitalize(),
            command=lambda name=theme_name: theme_manager.apply_theme(root, name)
        )
        btn.pack(side="left", padx=5)

    # Label de démonstration
    label = ttk.Label(root, text="Démonstration de thèmes")
    label.pack(pady=20)

    # Entry de démonstration
    entry = ttk.Entry(root)
    entry.pack(pady=10)
    entry.insert(0, "Zone de texte")

    # Treeview de démonstration
    tree_frame = ttk.Frame(root)
    tree_frame.pack(pady=10, fill="both", expand=True, padx=10)

    tree = ttk.Treeview(tree_frame, columns=("Colonne 1", "Colonne 2"))
    tree.heading("#0", text="Arbre")
    tree.heading("Colonne 1", text="Colonne 1")
    tree.heading("Colonne 2", text="Colonne 2")

    for i in range(5):
        tree.insert("", "end", text=f"Item {i}", values=(f"Valeur A{i}", f"Valeur B{i}"))

    tree.pack(fill="both", expand=True)

    root.mainloop()
