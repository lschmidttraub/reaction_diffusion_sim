import numpy as np 
import matplotlib.pyplot as plt
import cv2 as cv
from fonctions import *
from commandes import *


class Simulation2D():
    """
    Simulation d'un système de réaction-diffusion dans 2 dimensions
    """
    def __init__(self, Da, Db, Ra, Rb, f_init, dt, forme, etapes, symetrie):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.f_init = f_init
        self.symetrie = symetrie
        self.forme = forme
        self.dt = dt
        self.etapes = etapes
    
    def initialisation(self):
        """
        Initialiser les paramètres de la simulation
        """
        self.t = 0
        if self.symetrie:
            self.a, self.b = self.f_init(self.forme, self.symetrie)
        else:
            self.a, self.b = self.f_init(self.forme)
    
    def actualiser(self):
        """
        Actualise la fonction pour simuler le système de réaction diffusion
        """
        for _ in range(self.etapes):
            self.t += self.dt
            lapA = laplacien2D(self.a)
            lapB = laplacien2D(self.b)
            deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
            deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
            self.a += deltaA
            self.b += deltaB

    def determiner_img(self, couleur):
        """
        Générer l'image à partir du tableau de concentrations des substances A et B

        Args:
            couleur (str): couleur des substances A et B

        Returns:
            numpy.ndarray: 
        """
        if couleur:
            pos = {"b":0, "g":1, "r":2}
            ordre=np.zeros((3,)+tuple(self.forme))
            ordre[pos[couleur[0]]]=self.a*255
            ordre[pos[couleur[1]]]=self.b*255
            img = np.stack(ordre, axis=2)
        else:
            img = self.a*255
        return img
        
    
    def simulation(self, couleur):
        """
        Simulation du modèle de réaction en 2 dimensions. 

        Args:
            couleur (str): couleur des substances A et B
        """
        print("Tapez 'q' pour sortir de la simulation.")
        self.initialisation()
        cv.namedWindow('simulation', cv.WINDOW_KEEPRATIO)
        ratio_img =self.forme[1]/self.forme[0]
        cv.resizeWindow('simulation', (int(300*ratio_img), 300))
        while True:
            self.actualiser()
            img = self.determiner_img(couleur)
            cv.imshow("simulation", img.astype(np.uint8))
            if cv.waitKey(10) == ord('q'):
                break
        cv.destroyAllWindows()

    def creer_graphique(self, fichier, nb_etapes):
        """
        Sauvegarde le résultat après nb_etapes itérations dans un fichier image

        Args:
            fichier (str): fichier ou est stockée la vidéo
            nb_etapes (int): nombre d'étapes
        """
        fig, ax = plt.subplots(figsize = (10,10))
        self.initialisation()
        for _ in range(nb_etapes):
            self.actualiser()
        ax.imshow(self.a)
        ax.set_title("A, t = "+str(self.t))
        
        fig.savefig("rendus/"+fichier)
        plt.close()

    
    def creer_video(self, fichier, nb_etapes, couleur):
        """
        Générer une vidéo de la simulation

        Args:
            fichier (str): fichier ou est stockée la vidéo
            nb_etapes (int): nombre d'étapes
            couleur (str): couleur des substances A et B
        """
        self.initialisation()
        if couleur:
            video = cv.VideoWriter("rendus/"+fichier, cv.VideoWriter_fourcc(*"mp4v"), fps=10.0, frameSize=self.forme)
        else:
            video = cv.VideoWriter("rendus/"+fichier, cv.VideoWriter_fourcc(*"mp4v"), fps=10.0, frameSize=self.forme, isColor=False)

        for _ in range(nb_etapes):
            self.actualiser()
            img = self.determiner_img(couleur)
            video.write(img.astype(np.uint8))
        video.release()

GS_presets = [
    "Cellules (Default)", (0.16, 0.08, 0.035, 0.065, 1),  
    "Cellules rapides", (0.14, 0.06, 0.035, 0.065, 1),  
    "Corail", (0.14, 0.06, 0.06, 0.062, 1),  
    "Corail 2", (0.19, 0.05, 0.06, 0.062, 1),  
    "Petites vagues", (0.17, 0.095, 0.02, 0.05, 1),  
    "Spirales", (0.1675, 0.1, 0.02, 0.05, 1),  
    "Rayures", (0.01, 0.15, 0.02, 0.055, 1),  
    "Vers", (0.17, 0.08, 0.05, 0.065, 1),  
    "Trous", (0.23, 0.085, 0.039, 0.058, 1),  
]

FN_presets = [
    "Labyrinthe (Default)", (3, 100, -0.005, 10, 0.002), 
    "Corail", (1, 100, 0.01, 1, 0.002), 
    "Gros points", (5, 50, -0.05, 1, 0.002), 
    "Petits points", (2, 100, 0.01, 10, 0.002), 
    "Trous", (3, 100, -0.025, 10, 0.002), 
]
if afficher_p:
    print("Valeurs prédéfinies pour le système Fitzugh-Nagumo (Default): (Da, Db, alpha, beta, dt)")
    for i in range(len(FN_presets)//2):
        print(str(i+1) + ".", FN_presets[i*2],":", FN_presets[i*2+1])
    print("\nValeurs prédéfinies pour le système Gray-Scott: (Da, Db, f, k, dt)")
    for i in range(len(GS_presets)//2):
        print(str(i+1) + ".", GS_presets[i*2],":", GS_presets[i*2+1])
    exit()

if modele=="gs":
    if Da*Db*f*k*dt==0:
        Da, Db, f, k, dt = GS_presets[2*p-1]

    def GS_Ra(a,b):
        return -a*b*b+f*(1-a)

    def GS_Rb(a,b):
        return a*b*b-(f+k)*b
    Sim  = Simulation2D(Da, Db, GS_Ra, GS_Rb, initialisation_GS, dt, (largeur, longueur), etapes, symetrie)

else:
    if Da*Db*alpha*beta*dt==0:
        Da, Db, alpha, beta, dt = FN_presets[2*p-1]
    def FN_Ra(a,b): 
        return a - a ** 3 - b + alpha
    def FN_Rb(a,b): 
        return (a - b) * beta
    Sim  = Simulation2D(Da, Db, FN_Ra, FN_Rb, initialisation_aleatoire, dt, (largeur, longueur), etapes, symetrie)
   

if option==1:
    Sim.simulation(couleur)
elif option==2:
    Sim.creer_graphique(fichier, nb_etapes)
elif option==3:
    Sim.creer_video(fichier, nb_etapes, couleur)
