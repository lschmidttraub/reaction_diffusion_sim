import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fonctions import *
from commandes import *

class Simulation1D():
    """
    Simulation d'un système de réaction-diffusion dans une dimension
    """
    def __init__(self, Da, Db, Ra, Rb, f_init, dt, longueur,  etapes, limites):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.f_init = f_init
        self.longueur = longueur
        self.dt = dt
        self.etapes = etapes
        self.limites = limites
    
    def initialisation(self):
        """
        Initialiser les paramètres de la simulation.
        """
        self.t = 0
        self.a, self.b = self.f_init(self.longueur)
    
    def actualiser(self):
        """
        Actualiser la fonction pour simuler le système de réaction diffusion
        """
        for _ in range(self.etapes):
            self.t += self.dt
            lapA = laplacien1D(self.a)
            lapB = laplacien1D(self.b)
            deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
            deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
            self.a += deltaA
            self.b += deltaB


    def tracer(self, ax):
        """
        Tracer la figure


        Args:
            ax (matplotlib.axes._subplots.AxesSubplot): Axes sur lequel tracer le graphique
        """
        ax.clear()
        ax.plot(self.a, color="b", label="A")
        ax.plot(self.b, color="r", label="B")
        ax.legend()
        ax.set_ylim(self.limites[0],self.limites[1])
        ax.set_title("t = "+str(self.t))
    
    
    def simulation(self):
        """
        Simulation du modèle de réaction-diffusion en 1 dimension (équation Fitzugh-Nagumo).
        """
        print("Tapez 'q' pour sortir de la simulation.")
        self.initialisation()
        fig, ax = plt.subplots()
        
        def iteration(t):
            self.actualiser()
            self.tracer(ax)
        
        ani = animation.FuncAnimation(fig, iteration, interval=10)
        plt.show()
        plt.close()
    
    def creer_graphique(self, fichier, nb_etapes):
        """
        Sauvegarde le résultat après nb_etapes itérations dans un fichier image.

        Args:
            fichier (str): nom du fichier
            nb_etapes (int): nombre d'étapes
        """
        self.initialisation()
        fig, ax = plt.subplots()
        
        for _ in range(nb_etapes):
            self.actualiser()

        self.tracer(ax)
        fig.savefig("rendus/"+fichier)
        plt.close()

    def creer_gif(self, fichier, nb_etapes):
        """
        Génère un GIF de l'évolution de la courbe au cours du temps


        Args:
            fichier (str): nom du fichier
            nb_etapes (int): nombre d'étapes
        """
        self.initialisation()
        fig, ax = plt.subplots()
        writer = animation.PillowWriter(fps=15)
        with writer.saving(fig, "rendus/"+fichier, 100):
            for _ in range(nb_etapes):
                self.actualiser()
                self.tracer(ax)
                writer.grab_frame()

        
        
        plt.close()
    
    def evolution(self, fichier, nb_etapes):
        """
        Générer un image de l'évolution du tableau au cours du temps. 
        Chaque colonne représente le tableau à un étape.

        Args:
            fichier (str): nom du fichier
            nb_etapes (int): nombre d'étapes
        """
        res = np.zeros((nb_etapes, self.longueur))
        self.initialisation()
        for i in range(nb_etapes):
            res[i]=self.a
            self.actualiser()
        cv.imwrite("rendus/"+fichier, np.rot90(res)*255)

FN_presets = [
    (3, 100, -0.005, 10, 0.002), 
    (1, 100, 0.01, 1, 0.002), 
    (5, 50, -0.05, 1, 0.002), 
]

GS_presets = [
    (0.19, 0.05, 0.06, 0.062, 1),  
    (0.14, 0.06, 0.06, 0.062, 1),
    (0.23, 0.085, 0.039, 0.058, 1),
    (0.17, 0.095, 0.02, 0.05, 1)
]

if afficher_p:
    print("Valeurs prédéfinies pour le modèle Fitzugh-Nagumo: (Da, Db, alpha, beta, dt)")
    for i in range(len(FN_presets)):
        print(str(i+1) + ".", FN_presets[i])
    print("\nValeurs prédéfinies pour le modèle Gray-Scott: (Da, Db, f, k, dt)")
    for i in range(len(GS_presets)):
        print(str(i+1) + ".", GS_presets[i])
    exit()

if modele=="gs":
    if Da*Db*f*k*dt==0:
        Da, Db, f, k, dt = GS_presets[p-1]

    def GS_Ra(a,b):
        return -a*b*b+f*(1-a)

    def GS_Rb(a,b):
        return a*b*b-(f+k)*b
    Sim  = Simulation1D(Da, Db, GS_Ra, GS_Rb, initialisation_GS, dt, longueur, etapes, (-0.5, 1.5))

else:
    if Da*Db*alpha*beta*dt==0:
        Da, Db, alpha, beta, dt = FN_presets[p-1]
    def FN_Ra(a,b): 
        return a - a ** 3 - b + alpha
    def FN_Rb(a,b): 
        return (a - b) * beta
    Sim  = Simulation1D(Da, Db, FN_Ra, FN_Rb, perturbation, dt, longueur, etapes, (-1,1))
   

if option==1:
    Sim.simulation()
elif option==2:
    Sim.creer_graphique(fichier, nb_etapes)
elif option==3:
    Sim.creer_gif(fichier, nb_etapes)