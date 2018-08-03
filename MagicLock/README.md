# UCL-SenseHat

## MagicLock
Le magic-lock est un moyen de cacher un message secret. Pour déverrouiller l'appareil et lire le message, l'utilisateur doit pivoter le raspberry dans une position et la valider à l'aide du joystick. Il peut aussi utiliser la direction du joystick comme 'position'. Si la position correspond à celle demandée, ce verrou est déverouillé. Le nombre de combinaison à réaliser dans l'ordre est compris entre 1 et 64 et est choisi par la personne cryptant le message.
Si aucun message n'existe, l'utilisateur peut créer sa propre combinaison et ensuite insérer son message uniquement avec le sense hat.

### Utilisation
Pour lancer le script: __python3 magiclock.py__

Si aucun ficher __secretKey.txt__ existe dans le même répertoire où se trouve le script, alors les script va vous demander de selectionner des chiffres à l'aide du senseHat. Qaund vous avez entré vos chiffres, il suffit d'enfoncer le joystick durant qqe secondes pour valider votre choix. Ensuite vous devez entrée une suite de positions du sense hat et/ou du joystick. Pour valider une position du sense hat, il faut appuyer sur le joystick. Pour enregistrer une position du joystick, il suffit de le bouger dans la direction voulu. Il n'est pas possible d'enregistrer l'action appuyer du joystick car elle sert à valider une position du sense hat. Pour chaque positions enregistrées,une led s'allumera. Pour finaliser votre sequence, il suffit d'enfoncer le joystick pendant quelques secondes.

Si un fichier __secretKey.txt__ existe dans le même répertoire où se trouve le script, alors le script va vous permettre de décrypter la sequence. Une image d'un cadenas verouiller va vous être présenté. Il suffit d'appuyer sur le joystick pour accéder à la phase de décryptage. Un certain nombres de LED seront rouge. Elles correspondent à des positions à déverrouiller. Quand vous avez une bonne combinaison, la LED passe au vert. Si vous vous tromper, vous devez refaire toute la combinaison. Une fois déverrouiller, votre message secret vous sera affiché.

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

Nous avons départagé le projet en deux parties : le cryptage et le decryptage. Cela nous a pris plus  ou moins 2h30 pour le cryptage et 3h pour le décryptage plus 2h30 pour merge les deux parties et rendre le programme 100% utilisable.

### Emulation

Le logiciel d'**émulation de Trinket.io** ne permettant pas d'utiliser les utilitaires de fichiers, il n'est possible de tester le code seulement avec des données *hard-codée*.

Pour le logiciel **stand-alone sense_emu**, cela fonctionne bien. Il est possible de crypter une combinaison ainsi que de décrypter la combinaison et faire afficher le message secret.

### Extensions

Voici quelques extensions faisables. Les étoiles représentent la difficulté sur une échelle de &ast; (facile) à &ast;&ast;&ast; (difficle).

* Limiter le nombre d'essai pour déverrouiller dans la partie décryptage (&ast;)
* Selection du message à enregistrer avec joystick et écran LED pour la partie cryptage (&ast;&ast;&ast;)
* Stocker la combinaison et le message autre part que dans un fichier txt (&ast;&ast;)
* Permettre de reset le message secret (&ast;&ast;)
* Input text characters only with RPI (&ast;&ast;)
