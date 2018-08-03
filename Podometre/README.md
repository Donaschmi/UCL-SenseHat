# UCL-SenseHat

## Fichiers

* __podometre.py__: lance un podomètre simple qui va compter vos pas en temps réelle. Pour l'arrêter il suffit d'appuyer sur le joystick. Le nombre de pas effectué restera afficher. (Mettre la partie USB du raspberry dans votre poche)
* __podo_display.py__: contient des méthodes pour l'affichage de numéros (0-99) sur le sense hat LED panel (utiliser dans podov2.py, podometre.py et podo_goal.py
* __podo_goal.py__: lance un selectionneur de numéro qui définira le nombre de pas a effectué. Qaund le nombre de pas est atteind, pour avez acces à un graph de la température enregistré durant la marche et de l'humidité.
* __podov2.py__: lance le podomètre. Quand on l'arrête, on peut changer de vue (graphe température, graphe humidité, nombre de pas) en appuyant sur le joystick
* __findPeaks.py__: Fichier avec des fonctions simple pour détecter des pics deans des tableaux 1D (pas utiliser)
* __README.md__: Ce fichier ci
* __exp_data__: dossier avec des fichiers .hat qui contienne 10s de données capteur du sense hat. (+- 23 pas) Utile avec les commande sense_play de la librairie sense_emu pour tester.

## Podometre

Le podomètre enregistre le nombre de pas effectués par un randonneur en utilisant l'accéléromètre du sense hat. Le nombre de pas est affiché sur l'écran (limite d'affichage est de 0 à 99). Après le lancement du script, il faut bouger le joystick pour débuter le comptage en temps réel. Pour l'arreter il suffit de bouger le joystick. Selon la version, après l'arrêt des graphes de la température et humidité sont afiché ou non.

### Etapes suivi durant l'implementation d'un simple podomètre

1. Lire les données de l'accéléromètre

2. Calculer la magnitude des 3 données ( sqrt(x^2+y^2+z^2))

3. Analyser si la donnée est un pic de mouvement (la donné précédente est plus grande...). Si c'est le cas alors compter un pas.

### Faisabilité

* Consulter la documentation concernant l'accéléromètre, température, humidité
* utiliser les libraries mathématique de base de python pour faire des racines carrées, exponentiel, arondissement
* tableaux

### Difficultés

* Trouver les bons paramètres de calibrage pour le comptage du nombres de pas
* Afficher un nombre à 2 chiffres sur l'écran LED
* Détecter un pic de gravité dans les mesures (simple: en comparaison la valeur actuelle et la précédente)

### Délivrables

Pour l'implementation du podomètre en soit, il y a 2 grande partie. La partie affichage nous à pris 2h et la partie mesure et application pour detecter les pas nous a pris 4h. Cette dernière tâche était la plus fastidieuse car il faut trouver (en testant) les bonnes valeurs de calibrage (pour la fréquence de mesure et la limite à partir de laquel on compte un pic de gravité comme un pas).


### Emulation
Il est facile d'enregistrer la valeurs des différents capteurs sur une certaine durée (sense_rec) pendant une marche. Ensuite avec sense_play, on peut rejouer les valuers enregistrées avec la librarie sense_emu. Il ne faut pas oublier de remplacer l'import de sense_hat par sense_emu dans le script python pour qu'il utilise les données injecté et pas les données réelles du sense hat.

### Extensions

* Marcher un nombre de pas définie (fait: podo_goal.py)
* Afficher des plus grands nombres de pas tout en conservant la lisibilité

### Test with sense_play
to test the podometer, please use the following command:

__sense_play data.hat & python3 podoscript.py__
 This will send data to the sense_emu and your script will directly read those values. don't forget to use sense_emu instead of sense_hat for testing with emulator

or launch the script and start walking
