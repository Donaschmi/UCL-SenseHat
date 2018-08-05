# UCL-SenseHat

Ceci est une collection de projets en python qui utilise le raspberry pi et le module sense hat

## Libraries
Nous utilisons les libraries python pour communiquer avec le sense hat:
[sense-hat](https://pythonhosted.org/sense-hat/)

## Fichiers
* __record_sense.py__: script qui enregistre les capteurs du sense hat avec la commande __sense_rec__ durant 10 seconds. Ce script peut prendre une arguments qui est le temps en secondes de l'enregistrement. Le script enregistre les données dans un ficher __data_TIMESTAMP.hat__ dans le même répertoire
* __game_of_life.py__: Le jeu game of live en pytohn utilisant l'écran LED du sense hat comme display
* emu.md: Information de systèmes ayant fait tourner le [sense hat emu](https://sense-emu.readthedocs.io/en/v1.1/) sans souicis
* README.md: ce fichier


## Projets
* [MagicLock](https://github.com/Donaschmi/UCL-SenseHat/tree/master/MagicLock)
* [Podomètre](https://github.com/Donaschmi/UCL-SenseHat/tree/master/Podometre)
* [TempCurve](https://github.com/Donaschmi/UCL-SenseHat/tree/master/TempCurve)
