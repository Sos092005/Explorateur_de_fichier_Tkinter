import tkinter as tk
from tkinter import messagebox
import os

class BarreChemin(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.repertoire_actuel = os.getcwd()  # Le répertoire de travail initial
        self.create_widgets()
        self.afficher_chemin()

    def create_widgets(self):
        # Label pour afficher le chemin actuel
        self.label = tk.Label(self, text="", width=50, anchor="w")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        # Entry pour permettre la saisie du chemin
        self.entry = tk.Entry(self, width=50)
        self.entry.grid(row=1, column=0, padx=10, pady=5)
        self.entry.bind("<Return>", self.selectionner_chemin)

        # Bouton pour revenir au répertoire parent
        self.parent_button = tk.Button(self, text="Parent", command=self.naviguer_vers_parent)
        self.parent_button.grid(row=0, column=1, padx=10, pady=5)

    def afficher_chemin(self):
        """Affiche le chemin actuel dans la barre"""
        self.label.config(text=self.repertoire_actuel)

    def mettre_a_jour(self):
        """Mettre à jour la barre de chemin lorsque l'utilisateur navigue"""
        self.afficher_chemin()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.repertoire_actuel)

    def naviguer_vers_parent(self):
        """Revenir au répertoire parent"""
        parent_path = os.path.dirname(self.repertoire_actuel)
        if parent_path != self.repertoire_actuel:
            self.repertoire_actuel = parent_path
            self.mettre_a_jour()
        else:
            messagebox.showwarning("Navigation", "Vous êtes déjà au répertoire racine.")

    def changer_chemin(self, nouveau_chemin):
        """Changer le chemin actuel en fonction de l'entrée de l'utilisateur"""
        if os.path.isdir(nouveau_chemin):
            self.repertoire_actuel = nouveau_chemin
            self.mettre_a_jour()
        else:
            messagebox.showerror("Erreur", "Le chemin spécifié est introuvable ou invalide.")

    def selectionner_chemin(self, event):
        """Gérer la sélection du chemin par l'utilisateur"""
        nouveau_chemin = self.entry.get()
        self.changer_chemin(nouveau_chemin)

# Fonction principale pour démarrer l'application
def main():
    root = tk.Tk()
    root.title("Explorateur de fichiers")
    root.geometry("600x150")  # Taille de la fenêtre
    barre_chemin = BarreChemin(master=root)
    barre_chemin.pack(fill="x", padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
