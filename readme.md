# Explorateur de Fichiers avec Tkinter

Un explorateur de fichiers simple développé avec Tkinter, offrant des fonctionnalités conviviale .

![Aperçu de l'Interface](app-screenshot.png)

## Fonctionnalités

| **Fonctionnalités Principales**       | **Fonctionnalités Bonus**       |
|---------------------------------------|----------------------------------|
| Navigation entre répertoires          | Basculer vue grille/liste       |
| Menu contextuel (Ouvrir/Supprimer/Renommer) | Changement de thème (tous les themes ttkbootstrap ) |
| Gestion des favoris                   |                                  |
| Recherche de fichiers                 |                                  |
| Affichage des infos (taille, date)    |                                  |
| Gestion des erreurs                   |                                  |
| Filtrage par type de fichier          |                                  |
| Création de dossiers                  |                                  |
| Barre de chemin interactive           |                                  |
| Actualisation manuelle                |                                  |

## Vidéos de Démonstration
- [Navigation Basique](https://sos092005.github.io/videos/v1.mp4)
- [Menu Contextuel & Favoris](https://sos092005.github.io/videos/v2.mp4)
- [Changement de Thème](https://sos092005.github.io/videos/v3.mp4)
- [Fonction de Recherche](https://sos092005.github.io/videos/v4.mp4)
- [Gestion des Erreurs](https://sos092005.github.io/videos/v5.mp4)

## Problèmes Rencontrés & Solutions


# Problème majeur
La structure initiale prevue était modulaire et developpée sous le dossier Version_initiale [Version_initiale](https://github.com/Sos092005/Explorateur_de_fichier_Tkinter/tree/main/Version_initiale)
Mais nous n'avons pu résourdre les problemes d'imports entre fichiers . Nous avons donc recemment optés pour une structure en un seul fichier  [un seul fichier](https://github.com/Sos092005/Explorateur_de_fichier_Tkinter/blob/main/Version_finale/four.py)

| **Problèmes**                          | **Solutions Appliquées**           |
|---------------------------------------|-----------------------------------|
| Complexité des imports multi-fichiers | Code consolidé dans [un seul fichier](https://github.com/Sos092005/Explorateur_de_fichier_Tkinter/blob/main/Version_finale/four.py) |
| Problèmes de compatibilité Linux      | Utilisation de bibliothèques multiplateformes (non entierement resolu) |
| Installation des dépendances (Pillow, ttkbootstrap, winshell) | Winshell et Pywin32 non resolus sous environnements non Windows |
| Affichage des vidéos dans le README   | Hébergement compressé sur [GitHub Pages](https://sos092005.github.io) |
| Échec de chargement des icônes        | Chemins de secours implémentés   |
| Erreurs d'indentation                 | Révision complète du code        |
| Problèmes avec `pywin32` sous Linux   | Conditionnement par système d'exploitation |

## Améliorations Futures
- Améliorer la précision de la recherche
- Optimiser la structure des imports
- Ajouter un système de prévisualisation de fichiers
- Support avancé des raccourcis clavier

`📁 Lien du Dépôt :` [Accéder au Code](https://github.com/Sos092005/Explorateur_de_fichier_Tkinter)  
`🌐 Site des Vidéos :` [Voir les Démonstrations](https://sos092005.github.io)
