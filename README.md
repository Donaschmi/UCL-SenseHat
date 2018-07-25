# UCL-SenseHat

## MagicLock
Le magic-lock est un moyen de cacher un message secret. Pour débloquer l'appareil et lire le message, l'utilisateur doit pivoter le raspberry dans une position et la valider à l'aide du joystick. Il peut aussi utiliser la direction du joystick (sans validation necessaire). Si la position/direction correspond à celle demandée, ce verrou est déverouillé. Le nombre de combinaison à réaliser dans l'ordre est compris entre 1 et 64 et est choisi par la personne cryptant le message.
Si aucun message n'existe, l'utilisateur peut créer sa propre combinaison et ensuite insérer son message.

### Faisabilité

* Manipuler des listes
* Manipuler des dictionnaires
* STDIN / STDOUT
* Ecriture et lecture de fichier
* Découpe en sous-méthodes
* Consulter de la doc
* Notions mathématiques TRES basiques (threshold)
* Représentation de couleurs par 3 decimal (RGB; pour l'écran LED)

### Difficultés

* Si un fichier existe, vérifier qu'il est valide (contient bien une combinaison plus un message)
* Différencier si le verrou suivant est une position ou bien un bouton du joystick
* Definir un control/execution flow correct: avancer dans la combinaison tant que les positions/directions sont correct. Quand une erreur survient, il faut reprendre du début de la combinaison
* Combinaisons de différentes tailles

### Délivrables

### Extensions

### Emulation


## Podomètre

### Faisabilité

### Difficultés

### Délivrables

### Extensions

### Emulation