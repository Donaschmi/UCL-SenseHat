# UCL-SenseHat

data.hat and data.csv are a test file with 10 seconds of sensehat data capture. different format but same raw data

## Test with sense_play
to test the podometer, please use the following command:

__sense_play data.hat & python3 podoscript.py__
 This will send data to the sense_emu and your script will directly read those values. don't forget to use sense_emu instead of sense_hat for testing with emulator
## Steps for step detection (2 ways)
The most accurate way is the second.

1. Read accelerometer data, calculate de magnitude: sqrt(x^2+y^2+z^2), then check if the magnitude is greater than a certain value. If yes then you count it as a step

2. Read accelerometer data, calculate de magnitude: sqrt(x^2+y^2+z^2), then analyse if it is a peak or not (by comparing to the prevouis data point) if it is a peak, check if it is above a certain level before counting it as a step

## Podometre

Le podomètre enregistre le nombre de pas effectué par un randonneur. Il enregistre aussi des paramètres comme la température et l'humidité. L'indice humidex qui est la température perçu, est aussi calcué avec une formule bien spécifique.

### Faisabilité

* Consulter la documentation concernant l'accéléromètre, température, humidité
* utiliser les libraries mathématique de base de python pour faire des racines carrées, exponentiel

### Difficultés

* Trouver les bons bon paramètres de calibrage pour le comptage de pas
* Appliquer une formule longue (indice Humidex)
* 

### Délivrables

### Emulation
Il est facile d'enregistrer la valeurs des différents capteurs sur une certaine durée (sense_rec). Ensuite avec sense_play, on peut rejouer les valuers enregistrées avec la librarie sense_emu.

### Extensions
