import json
import os
import tkinter as tk
from tkinter import messagebox

class Favoris:
    def __init__(self, fichier='favoris.json'):
        self.fichier = fichier
        self.favoris = self.charger()

    def charger(self):
        """Charger la liste des favoris depuis le fichier JSON."""
        try:
            with open(self.fichier, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retourne une liste vide si le fichier n'existe pas ou est corrompu

    def ajouter(self, favori):
        """Ajouter un favori à la liste et à la sauvegarde."""
        if favori not in self.favoris:
            self.favoris.append(favori)
            self.sauvegarder()
        else:
            raise ValueError("Ce favori est déjà présent.")

    def supprimer(self, favori):
        """Supprimer un favori de la liste et le fichier."""
        if favori in self.favoris:
            self.favoris.remove(favori)
            self.sauvegarder()
        else:
            raise ValueError("Ce favori n'existe pas.")

    def sauvegarder(self):
        """Sauvegarder la liste des favoris dans le fichier JSON."""
        try:
            with open(self.fichier, 'w') as f:
                json.dump(self.favoris, f)
        except (IOError, PermissionError) as e:
            print(f"Erreur lors de la sauvegarde des favoris: {e}")

def afficher_favoris(listbox, favoris):
    """Mettre à jour dynamiquement la liste affichée des favoris."""
    listbox.delete(0, tk.END)  # Effacer les résultats précédents
    for favori in favoris:
        listbox.insert(tk.END, favori)

def ajouter_favori(favoris, entry, listbox):
    """Ajouter un favori via l'interface utilisateur."""
    favori = entry.get()
    try:
        favoris.ajouter(favori)
        afficher_favoris(listbox, favoris.favoris)
        entry.delete(0, tk.END)  # Effacer le champ d'entrée
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

def supprimer_favori(favoris, listbox):
    """Supprimer un favori via l'interface utilisateur."""
    selection = listbox.curselection()
    if selection:
        favori = listbox.get(selection)
        try:
            favoris.supprimer(favori)
            afficher_favoris(listbox, favoris.favoris)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un favori à supprimer.")

def creer_interface():
    """Créer l'interface utilisateur pour gérer les favoris."""
    root = tk.Tk()
    root.title("Gestion des Favoris")

    favoris = Favoris()

    # Champ d'entrée pour ajouter un favori
    tk.Label(root, text="Ajouter un favori:").pack()
    entry_favori = tk.Entry(root)
    entry_favori.pack()

    # Liste des favoris
    listbox = tk.Listbox(root, width=50)
    listbox.pack()
    afficher_favoris(listbox, favoris.favoris)

    # Boutons pour ajouter et supprimer des favoris
    bouton_ajouter = tk.Button(root, text="Ajouter", command=lambda: ajouter_favori(favoris, entry_favori, listbox))
    bouton_ajouter.pack()

    bouton_supprimer = tk.Button(root, text="Supprimer", command=lambda: supprimer_favori(favoris, listbox))
    bouton_supprimer.pack()

    root.mainloop()

if __name__ == "__main__":
    creer_interface()
