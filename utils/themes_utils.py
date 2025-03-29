"""
themes_utils.py

Module de gestion des thèmes pour l'explorateur de fichiers.
Utilise `ttkthemes` pour appliquer des thèmes modernes à l'interface Tkinter.
Inclut la vérification des prérequis, le chargement des thèmes et la sauvegarde des préférences utilisateur.

Fonctionnalités :
- Vérification et installation des modules nécessaires.
- Chargement et application des thèmes via `ttkthemes`.
- Gestion des préférences utilisateur avec stockage en JSON.

"""

import sys
import subprocess
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

# ==========================
# 🔍 Vérification des prérequis
# ==========================

REQUIRED_MODULES = ["tkinter", "ttkthemes", "json", "os"]

def check_and_install_modules():
    """
    Vérifie si les modules nécessaires sont installés.
    Installe automatiquement `ttkthemes` s'il est absent.
    """
    missing_modules = []
    
    # Vérification de tkinter (intégré mais peut être absent)
    try:
        import tkinter
    except ImportError:
        missing_modules.append("tkinter (intégré à Python mais peut être désinstallé)")

    # Vérification de ttkthemes
    try:
        import ttkthemes
    except ImportError:
        missing_modules.append("ttkthemes")
    
    if not missing_modules:
        print("✅ Tous les prérequis sont satisfaits.")
        return

    print(f"⚠️ Modules manquants : {missing_modules}")
    
    # Installation automatique de ttkthemes si nécessaire
    if "ttkthemes" in missing_modules:
        print("📦 Installation de ttkthemes...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ttkthemes"])
        print("✅ ttkthemes installé avec succès.")

# ==========================
# 🎨 Gestion des thèmes
# ==========================

CONFIG_FILE = "theme_config.json"

def charger_preferences_theme():
    """
    Charge le thème préféré de l'utilisateur depuis un fichier JSON.
    Retourne le nom du thème par défaut si le fichier est inexistant ou corrompu.

    Returns:
        str: Nom du thème enregistré ou "clam" (par défaut).
    """
    if not os.path.exists(CONFIG_FILE):
        return "clam"

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("theme", "clam")
    except (json.JSONDecodeError, IOError):
        return "clam"

def sauvegarder_preferences_theme(theme_name):
    """
    Sauvegarde le thème sélectionné dans un fichier JSON.

    Args:
        theme_name (str): Nom du thème à sauvegarder.
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump({"theme": theme_name}, file, indent=4)
    except IOError:
        print("❌ Erreur lors de l'écriture du fichier de configuration.")

def appliquer_theme(root, theme_name):
    """
    Applique le thème sélectionné à l'interface Tkinter.

    Args:
        root (tk.Tk): Fenêtre principale Tkinter.
        theme_name (str): Nom du thème à appliquer.
    """
    try:
        style = ThemedStyle(root)
        style.set_theme(theme_name)
        print(f"✅ Thème appliqué : {theme_name}")
    except Exception as e:
        print(f"❌ Erreur lors de l'application du thème : {e}")

# ==========================
# 🧪 TEST D'EXÉCUTION
# ==========================

if __name__ == "__main__":
    check_and_install_modules()  # Vérifie et installe les dépendances si nécessaire

    # Création de la fenêtre principale Tkinter
    root = tk.Tk()
    root.title("Test des Thèmes")
    root.geometry("400x300")

    # Chargement du thème enregistré
    theme_actuel = charger_preferences_theme()
    appliquer_theme(root, theme_actuel)

    # Création d'un menu déroulant pour choisir un thème
    def changer_theme():
        nouveau_theme = theme_var.get()
        appliquer_theme(root, nouveau_theme)
        sauvegarder_preferences_theme(nouveau_theme)

    theme_var = tk.StringVar(value=theme_actuel)
    theme_menu = ttk.Combobox(root, textvariable=theme_var, values=ThemedStyle(root).theme_names())
    theme_menu.pack(pady=10)

    btn_appliquer = ttk.Button(root, text="Appliquer Thème", command=changer_theme)
    btn_appliquer.pack(pady=10)

    root.mainloop()
