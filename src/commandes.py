import argparse 

parser = argparse.ArgumentParser(description="trouve les commandes entrées")

parser.add_argument("-L", "--longueur", type=int, default=300, help="Longueur de l'affichage")
parser.add_argument("-l", "--largeur", type=int,  default=300, help="Largeur de l'affichage")
parser.add_argument("-o", "--option", type=int, help="1. Simulation 2. Graphique 3. Video/GIF")
parser.add_argument("-fi","--fichier", type=str, default="rendu.mp4", help="Nom du fichier qui stocke le résultat.")
parser.add_argument("-p", type=int, default=1, help="Choix parmi la liste de valeurs prédéfinies")
parser.add_argument("-ap", action="store_true", help="Afficher les valeurs prédéfinies")


parser.add_argument("-e", "--etapes", type=int, default=100, help="Nombre d'étapes exécutées à chaque itération")
parser.add_argument("-ne", "--nb_etapes", type=int, default=200, help="Nombre d'itérations exécutées pour la vidéo ou l'image")
parser.add_argument("-s", "--symetrie", type=int, default=0, help="Nombre de symétries rotationnelles")
parser.add_argument("-c", "--couleur", type=str, default="", help="Couleur (deux lettres appartenant à 'rgb') : la première lettre correspond à celle de la substance A, et la deuxième à celle de la substance B. Si les 2 lettres sont identiques, on n'affichera que la substance B")
parser.add_argument("-m", "--modele", type=str, default="fn", help="Système d'équations utilisé: Fitzugh-Nagumo('fn') ou Gray-Scott('gs')")
parser.add_argument("-r", "--rogner", action="store_true", help="Rogner l'image pour éviter les zones floues produites par les symétries")



parser.add_argument("-dt", type=int, default=0.001, help="Période de temps entre chaque étape")
parser.add_argument("-Da", type=int, default=0, help="Vitesse de propagation de la substance a")
parser.add_argument("-Db", type=int, default=0, help="Vitesse de propagation de la substance b")
parser.add_argument("-a", type=int, default=0, help="Valeur de alpha pour la simulation Fitzugh-Nagumo")
parser.add_argument("-b", type=int, default=0, help="Valeur de beta pour la simulation Fitzugh-Nagumo")
parser.add_argument("-f", type=int, default=0, help="'feed rate': vitesse d'accroissement dans la simulation Gray-Scott")
parser.add_argument("-k", type=int, default=0, help="'kill rate': vitesse de disparition dans la simulation Gray-Scott")

parser.add_argument("-ra", type=list, default=[], help="Rayons des activateurs")
parser.add_argument("-ri", type=list, default=[], help="Rayons des inhibiteurs")


args = parser.parse_args()

longueur = args.longueur
largeur = args.largeur
option = args.option
fichier = args.fichier
p = args.p
afficher_p = args.ap
etapes = args.etapes
nb_etapes = args.nb_etapes
symetrie = args.symetrie
couleur = args.couleur
modele = args.modele
rogner = args.rogner
dt=args.dt
Da=args.Da
Db=args.Db
alpha=args.a
beta=args.b
f=args.f
k=args.k
r_activ=args.ra
r_inhib=args.ri