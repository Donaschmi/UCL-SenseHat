# UCL-SenseHat


## Podometre

Le podomètre enregistre le nombre de pas effectué par un randonneur. Il utilise l'accéléromètre pour détecté des mouvements et compter les nombres de pas. Dès le début du script, les pas sont compté et affiché sur l'écran (limite d'affichage est de 0 à 99). Pour arreter le script, il suffit de bouger le joystick.

### Etapes à suivre

Il y a 2 manières de procéder pour le comptage du nombres de pas:

1. Lire les données de l'accéléromètre, calculer la magnitude des 3 données ( sqrt(x^2+y^2+z^2)), ensuite compter un pas si cette valeurs est au dessus d'un certain seuil

2. Lire les données de l'accéléromètre, calculer la magnitude des 3 données ( sqrt(x^2+y^2+z^2)), ensuite analyser si la donnée est un pic de mouvement (la donné précédente est plus grande). Si c'est le cas alors compter un pas.

La seconde manière de faire est plus précise que la première

### Faisabilité

* Consulter la documentation concernant l'accéléromètre, température, humidité
* utiliser les libraries mathématique de base de python pour faire des racines carrées, exponentiel, arondissement

### Difficultés

* Trouver les bons paramètres de calibrage pour le comptage de pas
* Afficher un nombre à 2 chiffres sur l'écran LED
* Détecter un pic de gravité dans les mesures (simple: en comparaison la valeur actuelle et la précédente)

### Délivrables

Pour l'implementation du podomètre en soit, il y a 2 grande partie. La partie affichage nous à pris 2h et la partie mesure et application pour detecter les pas nous a pris 4h. Cette dernière tâche était la plus fastidieuse car il faut trouver (en testant) les bonnes valeurs de calibrage (pour la fréquence de mesure et la limite à partir de laquel on compte un pic de gravité comme un pas).


### Emulation
Il est facile d'enregistrer la valeurs des différents capteurs sur une certaine durée (sense_rec) pendant une marche. Ensuite avec sense_play, on peut rejouer les valuers enregistrées avec la librarie sense_emu. Il ne faut pas oublier de remplacer l'import de sense_hat par sense_emu dans le script python pour qu'il utilise les données injecté et pas les données réelles du sense hat.

### Extensions

* Marcher un nombre de pas définie (fait: podo_goal.py)
* Afficher des plus grands nombres de pas tout en conservant la lisibilité

### Données de Test
Les fichiers .hat dans le répertoire exp_data sont des enregistrements d'une marche de 10s. Environ 23 pas ont été effectué pour tous les fichiers.

### Test with sense_play
to test the podometer, please use the following command:

__sense_play data.hat & python3 podoscript.py__
 This will send data to the sense_emu and your script will directly read those values. don't forget to use sense_emu instead of sense_hat for testing with emulator

or launch the script and start walking
