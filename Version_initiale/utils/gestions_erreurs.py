import os
import pathlib
import logging
import tkinter.messagebox as messagebox
import traceback

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='erreurs.log',
                    filemode='w')

def utiliser_decorateur_gerer_erreur(func):
    """Décorateur pour centraliser la gestion des erreurs."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            gerer_erreur_fichier(e)
    return wrapper

def gerer_erreur_fichier(exception):
    """Gérer les erreurs liées à la lecture et l'écriture de fichiers."""
    logging.error(f"Erreur de fichier: {exception}")
    messagebox.showerror("Erreur de fichier", str(exception))

def gerer_erreur_navigation(chemin):
    """Gérer les erreurs liées à la navigation dans les répertoires."""
    try:
        if not pathlib.Path(chemin).exists():
            raise FileNotFoundError(f"Le chemin '{chemin}' n'existe pas.")
    except FileNotFoundError as e:
        logging.warning(f"Erreur de navigation: {e}")
        messagebox.showwarning("Erreur de navigation", str(e))

def gerer_erreur_permissions(chemin):
    """Gérer les erreurs liées aux permissions d'accès."""
    if not os.access(chemin, os.R_OK):
        error_message = f"Accès refusé au chemin '{chemin}'."
        logging.error(error_message)
        messagebox.showerror("Erreur de permissions", error_message)

class GestionErreurs:
    def __init__(self, message, type_erreur, log_level=logging.ERROR):
        self.message = message
        self.type_erreur = type_erreur
        self.log_level = log_level

    def afficher_message(self):
        """Afficher le message d’erreur avec tkinter.messagebox."""
        messagebox.showerror("Erreur", self.message)

    def enregistrer_log(self):
        """Enregistrer les erreurs dans un fichier log avec logging."""
        logging.log(self.log_level, self.message)

    def formater_traceback(self):
        """Formater et afficher les erreurs détaillées avec traceback."""
        tb = traceback.format_exc()
        logging.error(f"Traceback: {tb}")
        messagebox.showerror("Erreur", f"{self.message}\n\nDétails:\n{tb}")

# Exemple d'utilisation
@utiliser_decorateur_gerer_erreur
def lire_fichier(chemin):
    """Lire un fichier et gérer les erreurs."""
    gerer_erreur_navigation(chemin)
    gerer_erreur_permissions(chemin)
    with open(chemin, 'r') as f:
        return f.read()

if __name__ == "__main__":
    # Exemple d'appel de la fonction
    try:
        contenu = lire_fichier("exemple.txt")
        print(contenu)
    except Exception as e:
        gerer_erreur_fichier(e)
