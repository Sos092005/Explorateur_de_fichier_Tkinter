"""
Module: Filtrage des Fichiers

Ce module contient la classe `Filtrage`, qui permet de filtrer et de gérer des fichiers dans un répertoire donné.
Les filtres disponibles incluent les extensions de fichiers, les motifs génériques, les dates de modification,
et les tailles des fichiers. De plus, il permet d'appliquer un tri sur les fichiers en fonction de critères comme
la date ou la taille.

Fonctionnalités :
- Filtrage des fichiers par extension.
- Filtrage des fichiers par motif (pattern).
- Filtrage des fichiers par date de modification.
- Filtrage des fichiers par taille (minimale et maximale).
- Tri des fichiers en fonction de critères spécifiques (date ou taille).
- Mise à jour dynamique de la liste des fichiers dans un widget Listbox Tkinter.

Classes :
- Filtrage : Permet de filtrer et de trier les fichiers d'un dossier en fonction de critères spécifiés.

Exceptions :
- FiltrageError : Exception personnalisée pour gérer les erreurs liées aux filtrages.

Dépendances :
- os : Pour les opérations de gestion des fichiers et des répertoires.
- fnmatch : Pour le filtrage basé sur des motifs de chaîne.
- tkinter : Pour l'interface graphique et la gestion des widgets.
"""



import os
import fnmatch
import tkinter as tk
from functools import lru_cache

class FiltrageError(Exception):
    """Exception personnalisée pour les erreurs liées au filtrage."""
    pass

class Filtrage:
    def __init__(self, dossier):
        self.dossier = dossier
        self.extensions = []
        self.motif = ""
        self.date_limite = None
        self.taille_min = None
        self.taille_max = None

    @lru_cache(maxsize=128)
    def get_file_info(self, fichier):
        """Récupère les métadonnées d’un fichier avec mise en cache."""
        chemin = os.path.join(self.dossier, fichier)
        try:
            return {
                "taille": os.path.getsize(chemin),
                "modification": os.path.getmtime(chemin)
            }
        except (FileNotFoundError, PermissionError):
            return None

    def appliquer_extension(self, extensions):
        """Filtre les fichiers en fonction des extensions spécifiées."""
        if not isinstance(extensions, list):
            raise TypeError("Les extensions doivent être fournies sous forme de liste.")
        self.extensions = extensions
        fichiers = os.listdir(self.dossier)
        return [f for f in fichiers if any(f.lower().endswith(ext.lower()) for ext in extensions)]

    def appliquer_motif(self, motif):
        """Filtre les fichiers en fonction d'un motif générique."""
        self.motif = motif
        fichiers = os.listdir(self.dossier)
        return fnmatch.filter(fichiers, motif)

    def appliquer_date(self, date_limite):
        """Filtre les fichiers selon une date limite de modification."""
        self.date_limite = date_limite
        fichiers = os.listdir(self.dossier)
        resultats = []
        for f in fichiers:
            try:
                if os.path.getmtime(os.path.join(self.dossier, f)) >= date_limite:
                    resultats.append(f)
            except (FileNotFoundError, PermissionError):
                continue  # Ignorer les fichiers qui posent problème
        return resultats

    def appliquer_taille(self, taille_min=None, taille_max=None):
        """Filtre les fichiers en fonction de leur taille."""
        self.taille_min = taille_min
        self.taille_max = taille_max
        fichiers = os.listdir(self.dossier)
        resultats = []
        for f in fichiers:
            try:
                taille = os.path.getsize(os.path.join(self.dossier, f))
                if (taille_min is None or taille >= taille_min) and (taille_max is None or taille <= taille_max):
                    resultats.append(f)
            except (FileNotFoundError, PermissionError):
                continue  # Ignorer les fichiers qui posent problème
        return resultats

    def combiner_filtrage_tri(self, criteres, tri=None):
        """Applique un filtrage combiné et un tri sur les fichiers du dossier."""
        fichiers = os.listdir(self.dossier)

        if "extension" in criteres and self.extensions:
            fichiers = self.appliquer_extension(self.extensions)
        if "motif" in criteres and self.motif:
            fichiers = self.appliquer_motif(self.motif)
        if "date" in criteres and self.date_limite is not None:
            fichiers = self.appliquer_date(self.date_limite)
        if "taille" in criteres and (self.taille_min is not None or self.taille_max is not None):
            fichiers = self.appliquer_taille(self.taille_min, self.taille_max)

        if tri:
            try:
                fichiers.sort(key=lambda f: self.get_file_info(f)[tri], reverse=True)
            except TypeError:
                fichiers = [f for f in fichiers if self.get_file_info(f) is not None]

        return fichiers

    def actualiser_liste_fichiers(self, listbox):
        """Mise à jour dynamique de la liste des fichiers dans un widget Listbox Tkinter."""
        listbox.delete(0, tk.END)
        fichiers = self.combiner_filtrage_tri(["extension"])
        for fichier in fichiers:
            listbox.insert(tk.END, fichier)





#tests
if __name__ == "__main__":
    import tempfile
    import time

    # Création d'un dossier temporaire pour les tests
    with tempfile.TemporaryDirectory() as test_dir:
        print(f"Création du dossier temporaire: {test_dir}")

        # Création de fichiers de test
        fichiers_test = [
            ("test1.txt", 500),   # 500 octets
            ("test2.py", 1500),   # 1.5 KB
            ("test3.jpg", 3000),  # 3 KB
            ("test4.txt", 7000),  # 7 KB
        ]

        for nom, taille in fichiers_test:
            chemin_fichier = os.path.join(test_dir, nom)
            with open(chemin_fichier, "wb") as f:
                f.write(b"0" * taille)
            time.sleep(1)  # Assurer des timestamps différents

        print("Fichiers de test créés avec succès.")

        # Initialisation de la classe Filtrage
        filtrage = Filtrage(test_dir)

        # Test 1: Filtrage par extension
        print("\n🔹 Test: Filtrage par extension (.txt)")
        filtrage.extensions = [".txt"]
        print(filtrage.appliquer_extension(filtrage.extensions))  # Doit retourner ['test1.txt', 'test4.txt']

        # Test 2: Filtrage par motif
        print("\n🔹 Test: Filtrage par motif ('*.py')")
        print(filtrage.appliquer_motif("*.py"))  # Doit retourner ['test2.py']

        # Test 3: Filtrage par date (fichiers modifiés après un certain timestamp)
        print("\n🔹 Test: Filtrage par date")
        timestamp_limite = time.time() - 2  # On filtre les fichiers modifiés dans les 2 dernières secondes
        print(filtrage.appliquer_date(timestamp_limite))  # Devrait retourner tous les fichiers

        # Test 4: Filtrage par taille (entre 1KB et 5KB)
        print("\n🔹 Test: Filtrage par taille (entre 1KB et 5KB)")
        print(filtrage.appliquer_taille(1024, 5000))  # Doit retourner ['test2.py', 'test3.jpg']

        # Test 5: Combinaison de filtres
        print("\n🔹 Test: Combinaison de filtres (extension .txt et taille > 6000)")
        filtrage.extensions = [".txt"]
        filtrage.taille_min = 6000
        print(filtrage.combiner_filtrage_tri(["extension", "taille"]))  # Doit retourner ['test4.txt']

        # Test 6: Tri par date de modification
        print("\n🔹 Test: Tri par date de modification")
        print(filtrage.combiner_filtrage_tri(["extension"], tri="modification"))  # Doit retourner les fichiers triés par date descendante

        # Test 7: Tri par taille
        print("\n🔹 Test: Tri par taille")
        print(filtrage.combiner_filtrage_tri(["extension"], tri="taille"))  # Doit retourner les fichiers triés par taille descendante

    print("\n✅ Tous les tests ont été exécutés.")
