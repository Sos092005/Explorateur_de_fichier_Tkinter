import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import shutil
import subprocess
import sys

# Création du Treeview (fonction modifiée pour prendre root comme argument)
def create_treeview(root):
    treeview = ttk.Treeview(root, columns=("path",), show="tree")
    treeview.pack(fill=tk.BOTH, expand=True)
    return treeview

# Fonction pour actualiser l'affichage des fichiers et dossiers
def refresh(treeview, current_directory):
    treeview.delete(*treeview.get_children())
    populate_treeview(treeview, current_directory)

# Fonction de navigation dans les dossiers
def go_back(history, current_directory, history_index, refresh):
    if history_index > 0:
        history_index -= 1
        current_directory = history[history_index]
        refresh(treeview, current_directory)
    return current_directory, history_index

def go_forward(history, current_directory, history_index, refresh):
    if history_index < len(history) - 1:
        history_index += 1
        current_directory = history[history_index]
        refresh(treeview, current_directory)
    return current_directory, history_index

# Fonctions pour les actions (création de dossiers, fichiers, suppression, etc.)
def create_new_folder(current_directory, refresh):
    folder_name = simpledialog.askstring("Nouveau Dossier", "Nom du dossier:")
    if folder_name:
        new_path = os.path.join(current_directory, folder_name)
        try:
            os.makedirs(new_path)
            refresh()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier: {e}")

def create_new_file(current_directory, refresh):
    file_name = simpledialog.askstring("Nouveau Fichier", "Nom du fichier:")
    if file_name:
        new_path = os.path.join(current_directory, file_name)
        try:
            with open(new_path, 'w') as f:
                pass
            refresh()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le fichier: {e}")

def delete_item(item_path, refresh):
    if messagebox.askyesno("Supprimer", "Voulez-vous vraiment supprimer cet élément ?"):
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            refresh()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer: {e}")

def rename_item(item_path, refresh):
    new_name = simpledialog.askstring("Renommer", "Nouveau nom:")
    if new_name:
        new_path = os.path.join(os.path.dirname(item_path), new_name)
        try:
            os.rename(item_path, new_path)
            refresh()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de renommer: {e}")

def show_properties(item_path):
    try:
        size = os.path.getsize(item_path)
        modified_time = os.path.getmtime(item_path)
        messagebox.showinfo("Propriétés", f"Chemin: {item_path}\nTaille: {size} octets\nModifié: {modified_time}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'obtenir les propriétés: {e}")

def open_file(item_path):
    try:
        if sys.platform == "win32":
            os.startfile(item_path)  # Windows : ouvre avec l'appli par défaut
        elif sys.platform == "darwin":
            subprocess.run(["open", item_path])  # macOS : ouvre avec l'appli par défaut
        else:
            subprocess.run(["xdg-open", item_path])  # Linux : ouvre avec l'appli par défaut
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir: {e}")

def open_folder(folder_path, current_directory, history, history_index, refresh):
    if folder_path != current_directory:
        current_directory = folder_path
        history = history[:history_index + 1]
        history.append(folder_path)
        history_index += 1
        refresh()

def get_installed_apps():
    """Retourne une liste des applications installées sur le système."""
    apps = []
    if sys.platform == "win32":
        possible_apps = ["notepad.exe", "code.exe", "chrome.exe", "firefox.exe", "wordpad.exe"]
        for app in possible_apps:
            app_path = shutil.which(app)
            if app_path:
                apps.append((app.split(".")[0], app_path))  # Ex: ("Notepad", "C:/Windows/System32/notepad.exe")
    
    elif sys.platform == "darwin":
        apps = [("TextEdit", "/System/Applications/TextEdit.app"),
                ("Safari", "/Applications/Safari.app"),
                ("VS Code", "/Applications/Visual Studio Code.app")]

    else:  # Linux
        possible_apps = ["gedit", "code", "firefox", "chromium", "libreoffice"]
        for app in possible_apps:
            app_path = shutil.which(app)
            if app_path:
                apps.append((app.capitalize(), app_path))  
    return apps

# Menu contextuel
def show_context_menu(event, context, item_path=None):
    menu = tk.Menu(root, tearoff=0)
    if context == 'interface':
        menu.add_command(label="Nouveau Dossier", command=create_new_folder)
        if current_directory != os.getcwd():  # Vérifie si on est dans un dossier
            menu.add_command(label="Nouveau Fichier", command=create_new_file)
    elif context == 'folder':
        menu.add_command(label="Ouvrir", command=lambda: open_folder(item_path))
        menu.add_command(label="Supprimer", command=lambda: delete_item(item_path))
        menu.add_command(label="Renommer", command=lambda: rename_item(item_path))
        menu.add_command(label="Propriétés", command=lambda: show_properties(item_path))
    elif context == 'file':
         menu.add_command(label="Ouvrir", command=lambda: open_file(item_path))
        # Sous-menu "Ouvrir avec"
         open_with_menu = tk.Menu(menu, tearoff=0)
         installed_apps = get_installed_apps()
         for app_name, app_path in installed_apps:
            open_with_menu.add_command(label=app_name, command=lambda p=app_path: subprocess.run([p, item_path]))
    
         menu.add_cascade(label="Ouvrir avec...", menu=open_with_menu)

         menu.add_command(label="Supprimer", command=lambda: delete_item(item_path))
         menu.add_command(label="Renommer", command=lambda: rename_item(item_path))
         menu.add_command(label="Propriétés", command=lambda: show_properties(item_path))
    menu.tk_popup(event.x_root, event.y_root)

# Détection du contexte lors du clic droit
def on_right_click(event):
    item = treeview.identify_row(event.y)
    if not item:
        show_context_menu(event, 'interface')
    else:
        item_path = treeview.item(item, 'values')[0]
        if os.path.isdir(item_path):
            show_context_menu(event, 'folder', item_path)
        else:
            show_context_menu(event, 'file', item_path)

# Double-clic pour ouvrir un dossier
def on_double_click(event):
    item = treeview.identify_row(event.y)
    if item:
        item_path = treeview.item(item, 'values')[0]
        if os.path.isdir(item_path):
            open_folder(item_path)
        else:
            open_file(item_path)  # 🔥 Ajout : ouvrir le fichier si c'est un fichier


# Remplissage initial du Treeview
def populate_treeview(treeview, path, parent=""):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        node = treeview.insert(parent, "end", text=item, values=(item_path,))
        if os.path.isdir(item_path):
            populate_treeview(treeview, item_path, node)

