
import tkinter as tk

# Création de la fenêtre principale (plein écran)
root = tk.Tk()
root.title("Interface Fluent Design - Inspired by GitHub Codespaces")
root.state("zoomed")  # Plein écran
root.configure(bg="#f8f8f8")  # Fond blanc épuré

# 🔹 Configuration de la grille principale
root.columnconfigure(0, weight=0)  # Barre d'outils (fixe)
root.columnconfigure(1, weight=0)  # Barre latérale (fixe)
root.columnconfigure(2, weight=1)  # Fenêtre principale (élastique)
root.rowconfigure(0, weight=0)  # Barre supérieure (fixe)
root.rowconfigure(1, weight=1)  # Contenu principal (élastique)

# 🔹 Barre d'outils (colonne gauche)
barre_outils = tk.Frame(root, width=41, height=972, bg="#f9f9f9",
                        highlightbackground="#e5e5e5", highlightthickness=1, bd=0)
barre_outils.grid(row=1, column=0, sticky="nsw")

# 🔹 Barre latérale (explorateur de fichiers)
barre_laterale = tk.Frame(root, width=152, height=972, bg="#f9f9f9",
                          highlightbackground="#e5e5e5", highlightthickness=1, bd=0)
barre_laterale.grid(row=1, column=1, sticky="nsw")

# 🔹 Fenêtre principale (zone de travail)
fenetre_principale = tk.Frame(root, bg="#ffffff", bd=0)
fenetre_principale.grid(row=1, column=2, sticky="nsew")

# 🔹 Méthode pour dessiner un rectangle arrondi
def create_rounded_rect(self, x1, y1, x2, y2, radius=12, **kwargs):
    '''Dessine un rectangle arrondi sur un Canvas.'''
    self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, **kwargs)
    self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, **kwargs)
    self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, **kwargs)
    self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, **kwargs)
    self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
    self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)

# 🔹 Barre supérieure (contenant la barre de recherche et la barre de chemin)
barre_superieure = tk.Frame(root, height=48, bg="#f8f8f8",
                            highlightbackground="#e5e5e5", highlightthickness=1, bd=0)
barre_superieure.grid(row=0, column=0, columnspan=3, sticky="nsew")

# 🔹 Canvas pour dessiner les contours arrondis
canvas = tk.Canvas(barre_superieure, bg="#f8f8f8", height=48, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 🔹 Définition des proportions de la barre supérieure
largeur_totale = root.winfo_screenwidth()  # Largeur de l'écran
marge_gauche = int(largeur_totale * 0.16)  # 13% pour la partie gauche
largeur_chemin = int(largeur_totale * 0.62)  # 62% pour la barre de chemin
largeur_recherche = int(largeur_totale * 0.18)  # 18% pour la barre de recherche
espace_entre = 15  # Espacement entre les barres

# 🔹 Barre de chemin (au centre)
barre_chemin_x1 = marge_gauche
barre_chemin_x2 = barre_chemin_x1 + largeur_chemin
barre_chemin = tk.Entry(barre_superieure, font=("Segoe UI", 12), bg="#ebebeb", bd=0)
barre_chemin.place(x=barre_chemin_x1, y=10, width=largeur_chemin, height=28)
create_rounded_rect(canvas, barre_chemin_x1 - 5, 8, barre_chemin_x2 + 5, 38, radius=5, fill="#ebebeb", outline="#d0d0d0")

# 🔹 Barre de recherche (à droite)
barre_recherche_x1 = barre_chemin_x2 + espace_entre
barre_recherche_x2 = barre_recherche_x1 + largeur_recherche
barre_recherche = tk.Entry(barre_superieure, font=("Segoe UI", 12), bg="#ebebeb", bd=0)
barre_recherche.place(x=barre_recherche_x1, y=10, width=largeur_recherche, height=28)
create_rounded_rect(canvas, barre_recherche_x1 - 5, 8, barre_recherche_x2 + 5, 38, radius=5, fill="#ebebeb", outline="#d0d0d0")

# 🔹 Ajout de la fonction au Canvas
tk.Canvas.create_rounded_rect = create_rounded_rect

# 🔹 Ajout d'un Canvas avec un Scrollbar pour la fenêtre principale (fenetre_principale)
canvas_principal = tk.Canvas(fenetre_principale, bg="#ffffff", bd=0)
canvas_principal.pack(side="left", fill="both", expand=True)

# 🔹 Scrollbar vertical
scrollbar_vertical = tk.Scrollbar(fenetre_principale, orient="vertical", command=canvas_principal.yview)
scrollbar_vertical.pack(side="right", fill="y")

# 🔹 Configure canvas to respond to scrollbar
canvas_principal.config(yscrollcommand=scrollbar_vertical.set)

# 🔹 Create a frame to contain the content inside the canvas
content_frame = tk.Frame(canvas_principal, bg="#ffffff")

"""
# 🔹 Add content to the content frame (to simulate overflow)
for i in range(30):  # This will add a lot of content to overflow the canvas
    tk.Label(content_frame, text=f"Item {i+1}", font=("Segoe UI", 12)).pack(pady=5)
"""


# 🔹 Place the content frame inside the canvas
canvas_principal.create_window((0, 0), window=content_frame, anchor="nw")

# 🔹 Update the scrolling region whenever the content frame size changes
def on_frame_configure(event):
    canvas_principal.configure(scrollregion=canvas_principal.bbox("all"))

# Bind the content frame resize event to update the scrolling region
content_frame.bind("<Configure>", on_frame_configure)

# Lancement de l'interface
root.mainloop()

