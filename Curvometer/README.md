# UCL-SenseHat

## Curvometer
Le curvometer permet d'enregistrer la température et l'humidité sur une durée variable et de représenter ces valeurs sous forme de courbe.

Les deux courbes affichées sont celle de l'humidité et de l'indice humidex (Indice représentant la température percue calculée grâce à plusieurs formules mathématiques. https://fr.wikipedia.org/wiki/Indice_humidex)

### Utilisation

Pour lancer le script et enregistrer les deux données : `python3 curvometer.py`, pour n'enregistrer que la température `python3 curvometer.py -t`, pour n'enregistrer que l'humidité `python3 curvometer.py -h`.

Une fois le script lancé, les données vont être enregistrées toutes les demi-secondes jusqu'à ce que l'utilisateur maintienne le joystick enfoncé. La courbe est alors affichée à l'écran et pour être parcourue de droite à gauche, chaque pixel horizontal étant une unité de temps.
Si aucun argument n'a été entré, il est possible de passer d'une courbe à l'autre en appuyant sur le bouton du milieu.

### Faisabilité

* Manipuler des listes
* Faire de longues fonctions mathématiques
* Découpes en sous-méthodes
* Selectionner juste une partie d'un large tableau

### Difficultés
* Approcher le problème (&ast;)
* Créer mathématiquement la courbe de température => tableau double-entrées (&ast;&ast;)
* Se déplacer sur la courbe (;&ast;&ast;)
* Traiter les données (&ast;)
* Basculer entre les courbes

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
* Récolter des données et les afficher sur une courbe en même temps. Cette extension est plutot compliquée car de nouveaux maxima/minima changent la forme de la courbe actuelle car elle est normalisée différement.
