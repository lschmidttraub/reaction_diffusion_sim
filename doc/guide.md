# Guide d'utilisateur
## Installation
1.	Cloner le répertoire du projet et entre dans le dossier
```
$ git clone https://github.com/spicyboi26/reaction_diffusion_sim 
$ cd reaction_diffusion_sim
```

2.	Installer les bibliothèques nécessaires  
```
$ pip install -r requirements.txt
```


## Commandes
```
optional arguments:
  -h, --help            show this help message and exit
  -L LONGUEUR, --longueur LONGUEUR
                        Longueur de l'affichage
  -l LARGEUR, --largeur LARGEUR
                        Largeur de l'affichage
  -o OPTION, --option OPTION
                        1. Simulation 2. Graphique 3. Video/GIF
  -fi FICHIER, --fichier FICHIER
                        Nom du fichier qui stocke le résultat.
  -p P                  Choix parmi la liste de valeurs prédéfinies
  -ap                   Afficher les valeurs prédéfinies
  -e ETAPES, --etapes ETAPES
                        Nombre d'étapes exécutées à chaque itération
  -ne NB_ETAPES, --nb_etapes NB_ETAPES
                        Nombre d'itérations exécutées pour la vidéo ou l'image
  -s SYMETRIE, --symetrie SYMETRIE
                        Nombre de symétries rotationnelles
  -c COULEUR, --couleur COULEUR
                        Couleur (deux lettres appartenant à 'rgb') : la
                        première lettre correspond à celle de la substance A,
                        et la deuxième à celle de la substance B. Si les 2
                        lettres sont identiques, on n'affichera que la
                        substance B
  -m MODELE, --modele MODELE
                        Système d'équations utilisé: Fitzugh-Nagumo('fn') ou
                        Gray-Scott('gs')
  -r, --rogner          Rogner l'image pour éviter les zones floues produites
                        par les symétries
  -dt DT                Période de temps entre chaque étape
  -Da DA                Vitesse de propagation de la substance a
  -Db DB                Vitesse de propagation de la substance b
  -a A                  Valeur de alpha pour la simulation Fitzugh-Nagumo
  -b B                  Valeur de beta pour la simulation Fitzugh-Nagumo
  -f F                  'feed rate': vitesse d'accroissement dans la
                        simulation Gray-Scott
  -k K                  'kill rate': vitesse de disparition dans la simulation
                        Gray-Scott
  -ra RA                Rayons des activateurs
  -ri RI                Rayons des inhibiteurs
```
La simulation à 1 dimension possède un quatrième option, qui suit l'évolution du système à travers le temps en créant une image où chaque colonne représente la concentration de la substance A à une étape.


On peut également directement modifier les paramètres des simulations, mais cela nécessite une connaissance du modèle mathématique utilisé. La totalité des arguments peut être retrouvée dans le fichier `commandes.py`. Dans le cas du choix d'un graphique ou d'une vidéo, le résultat est stocké dans le répertoire `src/rendus/`.


Le programme est entièrement écrit en Python, et est donc compatible la grande majorité des architectures. Il a été conçu sur et pour le système d’exploitation Windows, mais il devrait également être compatible avec les OS Linux et Mac. Les librairies utilisées pour les simulations sont NumPy, OpenCV, Matplotlib et SciPy, qui sont tous des modules très répandus dans la communauté scientifique. Nous avons également utilisé la librairie argparse, qui fait partie de la Librairie Standard Python, pour permettre le contrôle du programme depuis l’interface de ligne de commande.
 
