# Toutankharton

Ce projet est un jeu 2D en vue du dessus développé en Python en utilisant la bibliothèque Pygame. Il a été réalisé par Nathan Delorme et Julien De Laharpe dans le cadre du mini-projet de l'école d'ingénieur EFREI Paris.

## Aperçu

Vous incarnez un carton qui se trouve au sommet d'une pyramide de labyrinth. Votre objectif, descendre le plus possible dans les niveaux de la pyramide.
Mais attention, cette pyramide appartenait à une dynastie de slimes qui habitent toujours ces lieux.
Au fur et à mesure de votre avancement, vous pourrez acheter des améliorations pour vaincre plus efficacement ces nuisibles.

![Insérez une capture d'écran du jeu ici](https://nathandelorme.dscloud.me/Toutankharton/game_image_1.png)

## Fonctionnalités

Les fonctionnalités principales sont les suivantes :
 - Affichage du jeu en temps réel,
 - Affichage responsive design
 - Interactions entre le joueur, les slimes et les objets ramassables ou achetables,
 - La durée de votre partie ne dépend que de votre talent puisqu'il n'y a pas de limite dans le nombre d'étage que vous pourrez parcourir,
 - Combat de boss à chaque fin d'étage,
 - Le joueur peut tirer des boulettes de papier dans 8 directions (visée avec la souris) pour infliger des dégâts aux slimes,
 - Génération de salles sous forme de labyrinthe qui grandit en fonction de votre avancement dans la partie,
 - Génération procédurale des salles, de l'apparition des items et des slimes,
 - Sauvegarde dynamique permettant de quitter le jeu en le sauvegardant à tout moment et de le recharger

## Les contrôles
Les touches **Z, Q, S, D** sont utilisées pour les déplacements du joueur.

La touche **SPACE** (clic ou maintien) permet au joueur de tirer des boulettes de papier.

La **souris** permet de diriger le tir des boulettes dans l'une des 8 directions Nord, Sud, Est, West, Nord-Est, Nord-West, Sud-Est, Sud-West.

La touche **ECHAP** permet de sauvegarder et quitter le jeu.

## Installation et exécution
Dans un premier temps, assurez-vous d'avoir un logiciel permettant d'exécuter du code python dans une version 3.11.0 ou plus.
Ensuite, clonez ce répertoire Git.

Ce projet utilise la librairie Pygame, une bibliothèque Python dédiée à la création de jeux.
Pour installer toutes les dépendances du projet, il faut se référer aux libraires présentes dans le fichier requirements.txt qui contient toutes les librairies externes utilisées.
Ouvrez un terminal de commande et entrez les commandes suivantes une à une :

```bash
pip install pygame
pip install pygame_gui
```

Si pip n'est pas reconnu sur votre ordinateur, essayez avec pip 3
```bash
pip3 install pygame
pip3 install pygame_gui
```

Lancer le script main.py présent à la racine du projet et bon jeu !

## Auteurs
- Nathan Delorme
- Julien De Laharpe
