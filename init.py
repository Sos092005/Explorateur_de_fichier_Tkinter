import tkinter as tk
from menu_conceptuel import *  # Import des fonctions depuis menu_conceptuel.py

# Création de la fenêtre tkinter
root = tk.Tk()
root.title("Explorateur de Fichiers")
root.geometry("800x600")

# Initialisation du Treeview
treeview = create_treeview(root)  # Créer un Treeview avec la fonction importée

# Initialiser le répertoire actuel et l'historique
current_directory = os.getcwd()
history = [current_directory]
history_index = 0

# Configurer le bouton "Actualiser"
refresh_button = tk.Button(root, text="Actualiser", command=lambda: refresh(treeview, current_directory))
refresh_button.pack()

# Configurer les boutons "Précédent" et "Suivant"
back_button = tk.Button(root, text="⬅ Précédent", command=lambda: go_back(history, treeview, current_directory, history_index))
back_button.pack(side=tk.LEFT, padx=5)

forward_button = tk.Button(root, text="Suivant ➡", command=lambda: go_forward(history, treeview, current_directory, history_index))
forward_button.pack(side=tk.LEFT, padx=5)

# Lancer la boucle principale
root.mainloop()
