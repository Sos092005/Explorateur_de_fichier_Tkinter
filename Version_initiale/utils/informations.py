import os
import stat
import time
import mimetypes
import pwd
import grp
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PyPDF2 import PdfReader
import mutagen
import win32security
import win32api
import subprocess

# Fonction pour obtenir les informations de base d'un fichier
def obtenir_infos_fichier(chemin):
    try:
        # Vérification si le fichier existe
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Le fichier {chemin} n'existe pas.")
        
        # Informations de base
        nom_fichier = os.path.basename(chemin)
        taille = os.path.getsize(chemin)
        type_mime, _ = mimetypes.guess_type(chemin)
        date_creation = time.ctime(os.path.getctime(chemin))
        date_modification = time.ctime(os.path.getmtime(chemin))

        # Propriétaire et permissions (Unix)
        try:
            if os.name == 'posix':
                stat_info = os.stat(chemin)
                propriétaire = pwd.getpwuid(stat_info.st_uid).pw_name
                groupe = grp.getgrgid(stat_info.st_gid).gr_name
                permissions = stat.S_IMODE(stat_info.st_mode)
            else:
                propriétaire = groupe = permissions = "Non applicable"
        except Exception as e:
            print(f"Erreur lors de la récupération des informations de propriété/permissions : {e}")

        return {
            'Nom': nom_fichier,
            'Taille (octets)': taille,
            'Type MIME': type_mime,
            'Date de création': date_creation,
            'Date de modification': date_modification,
            'Propriétaire': propriétaire,
            'Groupe': groupe,
            'Permissions': oct(permissions),
        }
    
    except Exception as e:
        print(f"Erreur lors de l'obtention des informations du fichier : {e}")
        return None

# Fonction pour lire les métadonnées spécifiques des fichiers (images, audio, PDF, etc.)
def lire_metadonnees(chemin):
    try:
        metadonnees = {}
        # Type MIME du fichier
        type_mime, _ = mimetypes.guess_type(chemin)
        metadonnees['Type MIME'] = type_mime
        
        if type_mime and 'image' in type_mime:
            # Lecture des métadonnées d'une image
            with Image.open(chemin) as img:
                metadonnees['Dimensions'] = img.size
                metadonnees['Format'] = img.format
        
        elif type_mime and 'pdf' in type_mime:
            # Lecture des métadonnées d'un PDF
            reader = PdfReader(chemin)
            metadonnees['Auteur'] = reader.metadata.get('/Author', 'Inconnu')
            metadonnees['Nombre de pages'] = len(reader.pages)

        elif type_mime and 'audio' in type_mime:
            # Lecture des métadonnées d'un fichier audio
            audio = mutagen.File(chemin)
            metadonnees['Tags'] = audio.tags
        
        # Ajout d'autres types de fichiers ici (par exemple vidéo, exécutable, etc.)

        return metadonnees

    except Exception as e:
        print(f"Erreur lors de la lecture des métadonnées : {e}")
        return None

# Fonction pour afficher les permissions d'un fichier
def afficher_permissions(chemin):
    try:
        if os.name == 'posix':
            # Informations de permission sous Unix
            stat_info = os.stat(chemin)
            permissions = stat.S_IMODE(stat_info.st_mode)
            propriétaire = pwd.getpwuid(stat_info.st_uid).pw_name
            groupe = grp.getgrgid(stat_info.st_gid).gr_name
            return {
                'Permissions': oct(permissions),
                'Propriétaire': propriétaire,
                'Groupe': groupe,
            }
        elif os.name == 'nt':
            # Permissions sous Windows
            sec_info = win32security.GetFileSecurity(chemin, win32security.DACL_SECURITY_INFORMATION)
            dacl = sec_info.GetSecurityDescriptorDacl()
            permissions = []
            for i in range(dacl.GetAceCount()):
                ace = dacl.GetAce(i)
                permissions.append(ace[1])  # Utilise l'ID utilisateur pour identifier les permissions
            return {'Permissions': permissions}
        else:
            return {'Permissions': 'Système non supporté'}
    except Exception as e:
        print(f"Erreur lors de la récupération des permissions : {e}")
        return None

# Fonction pour vérifier l'accès à un fichier
def verifier_acces(chemin):
    try:
        acces = {
            'Lecture': os.access(chemin, os.R_OK),
            'Écriture': os.access(chemin, os.W_OK),
            'Exécution': os.access(chemin, os.X_OK),
        }
        return acces
    except Exception as e:
        print(f"Erreur lors de la vérification des accès : {e}")
        return None

# Interface Tkinter pour afficher les informations d'un fichier
def afficher_infos_gui(chemin):
    infos = obtenir_infos_fichier(chemin)
    if infos:
        root = tk.Tk()
        root.title(f"Informations sur {chemin}")

        for key, value in infos.items():
            label = tk.Label(root, text=f"{key}: {value}")
            label.pack()

        metadonnees = lire_metadonnees(chemin)
        if metadonnees:
            for key, value in metadonnees.items():
                label = tk.Label(root, text=f"{key}: {value}")
                label.pack()

        root.mainloop()

# Exemple d'utilisation
if __name__ == "__main__":
    chemin_fichier = "/chemin/vers/le/fichier"  # Remplace par un chemin réel
    afficher_infos_gui(chemin_fichier)
