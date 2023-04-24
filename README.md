# reaction_diffusion_sim
## Simulations de systèmes de réaction-diffusion, motifs de Turing à échelles multiples
![Motif de Turing à échelles multiples](src/rendus/img_mstp.png)
Introduction


## Fonctionnement
### Systèmes de réaction-diffusion
![Simulation Fitzugh-Nagumo](src/rendus/FN_video.mp4)
Les modèles de réaction-diffusion décrivent l'évolution de concentrations de deux réactifs A et B dans l'espace. Ce modèle mathématique est décrit par les équations:
$$\frac{\partial A}{\partial t} = D_A*\nabla_A+R_A$$
$$\frac{\partial B}{\partial t} = D_B*\nabla_B+R_B$$
où $D_a$ et $D_B$ sont les vitesses diffusion des substances A et B et $\nabla$ est l'opérateur laplacien. $R_A$ et $R_B$ varient selon le modèle utilisé: 
Fitzugh-Nagumo:
$$R_A(A,B)=A-A^3-B+\alpha$$
$$R_B(A,B)=\beta(A-B)$$


Equations Gray-Scott:
$$R_a(a,b)=-ab^2+f(1-a)$$
$$R_b(a,b)=ab^2-(f+k)b$$
### Motifs de Turing à échelles multiples


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

### Dépendances
LANGAGE: Python 3.9.13

LIBRAIRIES:
matplotlib==3.5.1
numpy==1.22.3
opencv_python==4.7.0.72
scipy==1.10.1

## Tutorial
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



IMPORTANT LINKS: 
https://en.wikipedia.org/wiki/Reaction%E2%80%93diffusion_system
https://en.wikipedia.org/wiki/Turing_pattern

https://softologyblog.wordpress.com/2011/07/05/multi-scale-turing-patterns/
http://www.jonathanmccabe.com/Cyclic_Symmetric_Multi-Scale_Turing_Patterns.pdf

https://www.algosome.com/articles/reaction-diffusion-gray-scott.html
https://www.algosome.com/articles/reaction-diffusion-gray-scott-3d.html
