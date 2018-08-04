# UCL-SenseHat

## Fichier

``curvometer.py`` : Script principal

## Curvometer
Le curvometer permet d'enregistrer la température et l'humidité sur une durée variable et de représenter ces valeurs sous forme de courbe.

Les deux courbes affichées sont celle de l'humidité et de l'indice humidex (Indice représentant la température percue calculée grâce à plusieurs formules mathématiques. https://fr.wikipedia.org/wiki/Indice_humidex)

Les valeurs minimales et maximales des deux courbes sont aussi affichées avant la courbe elle-même. Une indication au dessus des chiffres montre à quoi correspond la valeur.

### Utilisation

Pour lancer le script et enregistrer les deux données : `python3 curvometer.py`.

Une fois le script lancé, les courbes se construiront au fur et à mesure. Appuyer sur le joystick passe change le contenu de l'écran. Il est possible de naviguer sur la courbe avec le bouton gauche et droite.

### Faisabilité

* Manipuler des listes
* Faire de longues fonctions mathématiques
* Découpes en sous-méthodes
* Selectionner juste une partie d'un large tableau
* Créer des dictionnaires

### Difficultés
* Approcher le problème (&ast;)
* Créer mathématiquement la courbe de température => tableau double-entrées (&ast;&ast;)
* Se déplacer sur la courbe (;&ast;&ast;)
* Traiter les données (&ast;)
* Basculer entre les états. (&ast;)

### Délivrables
La première partie consiste à récolter les différentes données et à les traiter (eg: utiliser la température et l'humidité pour trouver l'indice humidex). Cette partie prends plus ou moins 2h en tenant en compte la vérification des données sachant qu'il faut calculer plusieurs valeurs intermédiaires et donc vérifier le résultat de chacunes manuellement.

La deuxième partie consiste à transformer les données en un tableau de 8 * nbre_de_données. Pour cela il faut normaliser les données de bases afin d'avoir une courbe plus lisse. Cette partie prends à peu près 3h

La troisième partie partie permettant d'afficher la courbe et de pouvoir se déplacer le long de celle-ci a pris plus-ou-moins 2h.

### Emulation
Aucuns soucis à émuler ce programme grâce à Trinket.io vu la possibilité de changer les données en temps réel.

Pour le logiciel **stand-alone sense_emu**, il suffit de créer des données manuellement et les fournir au programme pour vérifier l'allure de la courbe.

### Extensions
* Lire des fichiers contenant des données et les afficher au lieu d'en récolter.
* Récolter d'autre données : pression, magnétisme, etc
