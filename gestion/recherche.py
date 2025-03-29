import os
import fnmatch
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
from pathlib import Path
from functools import lru_cache
import subprocess
import datetime


# Configuration du logging
logging.basicConfig(level=logging.DEBUG, filename='recherche.log', filemode='w')

# Fonction de recherche par nom
def rechercher_par_nom(dossier: Path, motif: str):
    try:
        results = []
        for entry in os.scandir(dossier):
            if entry.is_file() and fnmatch.fnmatch(entry.name, motif):
                results.append(entry.path)
        return results
    except Exception as e:
        logging.error(f"Erreur lors de la recherche par nom: {e}")
        return []

# Fonction de recherche par extension
def rechercher_par_extension(dossier: Path, extension: str):
    try:
        results = []
        for entry in os.scandir(dossier):
            if entry.is_file() and entry.name.endswith(extension):
                results.append(entry.path)
        return results
    except Exception as e:
        logging.error(f"Erreur lors de la recherche par extension: {e}")
        return []

# Fonction de recherche récursive
def rechercher_recursive(dossier: Path, motif: str):
    try:
        return [f for f in dossier.rglob(motif) if f.is_file()]
    except Exception as e:
        logging.error(f"Erreur lors de la recherche récursive: {e}")
        return []

# Fonction de recherche multi-critères
def rechercher_multi_criteres(dossier: Path, motif: str, extension: str):
    try:
        results = []
        for entry in os.scandir(dossier):
            if entry.is_file() and fnmatch.fnmatch(entry.name, motif) and entry.name.endswith(extension):
                results.append(entry.path)
        return results
    except Exception as e:
        logging.error(f"Erreur lors de la recherche multi-critères: {e}")
        return []

# Fonction pour ouvrir un fichier
def ouvrir_fichier(fichier):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(fichier)
        else:  # Linux
            subprocess.run(["xdg-open", fichier])
    except Exception as e:
        logging.error(f"Erreur lors de l'ouverture du fichier: {e}")

# Fonction pour mettre à jour la barre de progression
def mettre_a_jour_progressbar(progress, valeur):
    progress['value'] = valeur

# Fonction pour afficher les résultats
def afficher_resultats(resultats, listbox):
    listbox.delete(0, tk.END)  # Effacer les résultats précédents
    for fichier in resultats:
        listbox.insert(tk.END, fichier)

# Fonction pour activer la recherche
def activer_recherche(dossier, motif, extension, listbox, progress):
    def recherche():
        progress.start()
        results = rechercher_multi_criteres(Path(dossier), motif, extension)
        afficher_resultats(results, listbox)
        progress.stop()
    
    threading.Thread(target=recherche).start()

# Interface utilisateur
def creer_interface():
    root = tk.Tk()
    root.title("Explorateur de Fichiers")

    # Barre de recherche
    tk.Label(root, text="Motif de recherche:").pack()
    entry_motif = tk.Entry(root)
    entry_motif.pack()

    tk.Label(root, text="Extension:").pack()
    entry_extension = tk.Entry(root)
    entry_extension.pack()

    # Liste des résultats
    listbox = tk.Listbox(root, width=50)
    listbox.pack()

    # Barre de progression
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
    progress.pack()

    # Bouton de recherche
    bouton_recherche = tk.Button(root, text="Rechercher", command=lambda: activer_recherche(".", entry_motif.get(), entry_extension.get(), listbox, progress))
    bouton_recherche.pack()

    # Bouton pour ouvrir le fichier sélectionné
    bouton_ouvrir = tk.Button(root, text="Ouvrir le fichier sélectionné", command=lambda: ouvrir_fichier(listbox.get(listbox.curselection())))
    bouton_ouvrir.pack()

    root.mainloop()

if __name__ == "__main__":
    creer_interface()
