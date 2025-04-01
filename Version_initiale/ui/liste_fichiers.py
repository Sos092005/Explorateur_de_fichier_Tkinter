import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json


class ThemeManager:
    def __init__(self):
        self.themes = {
            "clair": {
                "background": "#ffffff",
                "foreground": "#000000",
                "tree_bg": "#f8f8f8",
                "tree_fg": "#222222",
                "tree_even": "#f5f5f5",
                "tree_odd": "#ffffff",
                "highlight": "#e1e1e1"
            },
            "sombre": {
                "background": "#2d2d2d",
                "foreground": "#e0e0e0",
                "tree_bg": "#252525",
                "tree_fg": "#e0e0e0",
                "tree_even": "#2a2a2a",
                "tree_odd": "#333333",
                "highlight": "#3d3d3d"
            }
        }
        self.current_theme = "clair"
        self.load_preferences()

    def load_preferences(self):
        try:
            with open("preferences.json", "r") as f:
                prefs = json.load(f)
                if prefs.get("theme") in self.themes:
                    self.current_theme = prefs["theme"]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_preferences(self):
        with open("preferences.json", "w") as f:
            json.dump({"theme": self.current_theme}, f)

    def apply_theme(self, widget, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme

        theme = self.themes[theme_name]
        self.current_theme = theme_name

        widget.configure(bg=theme["background"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".",
                        background=theme["background"],
                        foreground=theme["foreground"])
        style.configure("Treeview",
                        background=theme["tree_bg"],
                        foreground=theme["tree_fg"],
                        fieldbackground=theme["tree_bg"],
                        rowheight=25)
        style.map("Treeview",
                  background=[("selected", theme["highlight"])])

        self.save_preferences()
        return theme


class ListeFichiers(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.repertoire_actuel = "Simulation"  # Dossier simulé
        self.fichiers = []
        self.tri_actuel = "nom"
        self.ordre_tri = "asc"
        self.filtre_actuel = None

        # Création des icônes simulées (si les fichiers ne sont pas trouvés)
        self.creer_icones_simulees()

        # Initialisation du gestionnaire de thèmes
        self.theme_manager = ThemeManager()

        # Création de l'interface
        self.creer_interface()
        self.mettre_a_jour_liste()

    def creer_icones_simulees(self):
        """Crée des icônes simulées si les fichiers ne sont pas trouvés"""
        try:
            # Icône de dossier
            self.icon_dossier = tk.PhotoImage(file="icones/dossier.png").subsample(2, 2)
        except:
            self.icon_dossier = tk.PhotoImage(width=16, height=16)
            self.icon_dossier.put("blue", to=(0, 0, 15, 15))

        try:
            # Icône de fichier
            self.icon_fichier = tk.PhotoImage(file="icones/filer.png").subsample(2, 2)
        except:
            self.icon_fichier = tk.PhotoImage(width=16, height=16)
            self.icon_fichier.put("green", to=(0, 0, 15, 15))

        try:
            # Icône de favori
            self.icon_favori = tk.PhotoImage(file="icones/bookmark.png").subsample(2, 2)
        except:
            self.icon_favori = tk.PhotoImage(width=16, height=16)
            self.icon_favori.put("red", to=(0, 0, 15, 15))

    def creer_interface(self):
        # Appliquer le thème
        theme = self.theme_manager.apply_theme(self)

        # Barre d'outils
        toolbar = tk.Frame(self, bg=theme["background"])
        toolbar.pack(fill="x", padx=5, pady=5)

        # Boutons de thème
        for theme_name in self.theme_manager.themes.keys():
            btn = tk.Button(
                toolbar,
                text=theme_name.capitalize(),
                command=lambda n=theme_name: self.changer_theme(n),
                bg=theme["highlight"],
                relief="flat"
            )
            btn.pack(side="left", padx=2)

        # Barre de chemin (désactivée car nous simulons les fichiers)
        self.chemin_label = tk.Label(
            self,
            text="Contenu : 2 dossiers, 2 fichiers, 2 favoris",
            bg=theme["background"],
            fg=theme["foreground"]
        )
        self.chemin_label.pack(fill="x", padx=5, pady=5)

        # Treeview
        self.treeview = ttk.Treeview(self, columns=("type", "taille", "modification"), selectmode="extended")
        self.treeview.pack(expand=True, fill="both", padx=5, pady=5)

        # Configuration des colonnes
        self.treeview.column("#0", width=200, anchor="w")  # Colonne principale pour le nom
        self.treeview.column("type", width=100, anchor="w")
        self.treeview.column("taille", width=80, anchor="e")
        self.treeview.column("modification", width=120, anchor="w")

        # En-têtes
        self.treeview.heading("#0", text="Nom", command=lambda: self.trier_fichiers("nom"))
        self.treeview.heading("type", text="Type", command=lambda: self.trier_fichiers("type"))
        self.treeview.heading("taille", text="Taille", command=lambda: self.trier_fichiers("taille"))
        self.treeview.heading("modification", text="Modifié le", command=lambda: self.trier_fichiers("modification"))

        # Barre de défilement
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Événements
        self.treeview.bind("<Double-1>", self.on_double_click)
        self.treeview.bind("<Button-3>", self.on_right_click)

    def changer_theme(self, theme_name):
        """Change le thème de l'interface"""
        theme = self.theme_manager.apply_theme(self, theme_name)

        self.chemin_label.configure(
            bg=theme["background"],
            fg=theme["foreground"]
        )

        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["background"])

        self.mettre_a_jour_liste()

    def obtenir_info_fichier(self, nom_fichier):
        """Simule les informations des fichiers"""
        if "Dossier" in nom_fichier:
            return {
                "nom": nom_fichier,
                "type": "Dossier",
                "taille": "",
                "modification": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "chemin": f"/simulation/{nom_fichier}",
                "icone": self.icon_dossier
            }
        elif "Favori" in nom_fichier:
            return {
                "nom": nom_fichier,
                "type": "Favori",
                "taille": "",
                "modification": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "chemin": f"/simulation/{nom_fichier}",
                "icone": self.icon_favori
            }
        else:  # Fichier
            return {
                "nom": nom_fichier,
                "type": "Fichier",
                "taille": "10 Ko",
                "modification": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "chemin": f"/simulation/{nom_fichier}",
                "icone": self.icon_fichier
            }

    def lister_fichiers(self):
        """Retourne la liste simulée des fichiers"""
        elements_simules = [
            "Dossier 1",
            "Dossier 2",
            "Document.txt",
            "Image.jpg",
            "Favori 1",
            "Favori 2"
        ]

        return [self.obtenir_info_fichier(f) for f in elements_simules]

    def mettre_a_jour_liste(self):
        self.treeview.delete(*self.treeview.get_children())
        self.fichiers = self.lister_fichiers()
        self.appliquer_tri()

        theme = self.theme_manager.themes[self.theme_manager.current_theme]

        for i, fichier in enumerate(self.fichiers):
            tag = "even" if i % 2 == 0 else "odd"
            self.treeview.insert(
                "", "end",
                text=fichier["nom"],
                image=fichier["icone"],
                values=(fichier["type"], fichier["taille"], fichier["modification"]),
                tags=(tag,),
                iid=fichier["chemin"]
            )

        self.treeview.tag_configure("even", background=theme["tree_even"])
        self.treeview.tag_configure("odd", background=theme["tree_odd"])

    def trier_fichiers(self, critere):
        if self.tri_actuel == critere:
            self.ordre_tri = "desc" if self.ordre_tri == "asc" else "asc"
        else:
            self.tri_actuel = critere
            self.ordre_tri = "asc"
        self.mettre_a_jour_liste()

    def appliquer_tri(self):
        if not self.fichiers:
            return

        cle_tri = {
            "nom": lambda x: x["nom"].lower(),
            "type": lambda x: x["type"].lower(),
            "taille": lambda x: float(x["taille"].split()[0]) if x["taille"] else 0,
            "modification": lambda x: datetime.strptime(x["modification"], "%d/%m/%Y %H:%M")
        }.get(self.tri_actuel, lambda x: x["nom"].lower())

        try:
            self.fichiers = sorted(
                self.fichiers,
                key=cle_tri,
                reverse=(self.ordre_tri == "desc")
            )
        except (ValueError, KeyError):
            self.fichiers = sorted(self.fichiers, key=lambda x: x["nom"].lower())

    def on_double_click(self, event):
        item = self.treeview.selection()[0]
        if item:
            info = next((f for f in self.fichiers if f["chemin"] == item), None)
            if info and info["type"] == "Dossier":
                messagebox.showinfo("Info", f"Ouverture du dossier: {info['nom']}")

    def on_right_click(self, event):
        item = self.treeview.identify_row(event.y)
        if item:
            self.treeview.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Ouvrir", command=self.ouvrir_selection)
            menu.add_command(label="Propriétés", command=self.afficher_proprietes)
            menu.post(event.x_root, event.y_root)

    def ouvrir_selection(self):
        selection = self.treeview.selection()
        if selection:
            self.on_double_click(None)

    def afficher_proprietes(self):
        selection = self.treeview.selection()
        if selection:
            info = next((f for f in self.fichiers if f["chemin"] == selection[0]), None)
            if info:
                messagebox.showinfo(
                    "Propriétés",
                    f"Nom: {info['nom']}\nType: {info['type']}\nTaille: {info['taille']}\nModifié le: {info['modification']}"
                )


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Explorateur de fichiers")
    root.geometry("800x600")

    liste_fichiers = ListeFichiers(root)
    liste_fichiers.pack(expand=True, fill="both")

    root.mainloop()
  
