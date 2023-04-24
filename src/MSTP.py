import numpy as np
import cv2 as cv
from fonctions import *
from commandes import *

class MSTP():
    def __init__(self, forme, initialisateur, r_activ, r_inhib, dt, symetrie, rogner):
        self.N = len(r_activ)
        self.forme=np.array(forme)
        self.initialisateur = initialisateur
        self.r_activ = np.array(r_activ)
        self.r_inhib = np.array(r_inhib)
        self.creer_noyaux()
        self.dt = np.array(dt)
        self.symetrie = symetrie
        self.variance = np.zeros([self.N] + list(forme))
        self.var_min = np.zeros(self.forme, dtype = int)
        self.rogner = rogner
        if self.rogner:
            x,y = self.forme
            r = min(x,y)/np.sqrt(x**2+y**2)
            long, larg = x*r, y*r
            L1, L2 = int(self.forme[0]-long)//2, int(self.forme[0]+long)//2
            l1, l2 = int(self.forme[1]-larg)//2, int(self.forme[1]+larg)//2
            self.dim = np.s_[L1:L2, l1:l2]

    def initialisation(self):
        """
        Initialiser le tableau.
        """
        self.tab = self.initialisateur(self.forme, self.symetrie)[0]

    def creer_noyaux(self):
        """
        Cette fonction du fait que la transformée de Fourier de la convolution de 
        deux fonctions est égale au produit de leurs transformées de Fourier.
        Elle calcule les transformées de Fourier des noyaux circulaires des rayons d'activateurs et d'inhibiteurs
        """
        def noyau(r):
            """
            Générer un noyau circulaire de rayon r, dont la somme des éléments est égale à 1
            Args:
                r (int): rayon du noyau

            Returns:
                numpy.ndarray: noyau circulaire
            """
            k = np.fromfunction(lambda x, y: ((x-self.forme[0]/2)**2 + (y-self.forme[1]/2)**2 <= r**2)*1, self.forme, dtype=int).astype(np.uint8)
            return k/np.sum(k) 
        self.noyaux = [np.fft.rfft2(noyau(ri)-noyau(ra), s=self.forme) for ri, ra in zip(self.r_activ, self.r_inhib)]

    def actualiser(self):
        """
        Calculer la variance, trouver la variance minimale pour chaque pixel et actualiser le tableau.
        """
        for n, noyau in enumerate(self.noyaux):
            # On prend la transformée de Fourier inverse pour actualiser la variance
            self.variance[n] = np.fft.irfft2(np.fft.rfft2(self.tab)*noyau)
        self.var_min = np.argmin(self.variance**2, axis = 0)
        # On ajuste le tableau en fonction de la variance minimale 
        self.tab += np.choose(self.var_min, self.dt[:, np.newaxis, np.newaxis]*np.sign(self.variance))
        # Normalisation min-max
        self.tab= (self. tab - self.tab.min()) / (self.tab.max() - self.tab.min())
        if self.symetrie:
            self.tab = symetrique(self.tab, self.symetrie)


    def simulation(self):
        """
        Afficher la simulation en temps réel.
        """
        print("Tapez 'q' pour sortir de la simulation.")
        self.initialisation()
        cv.namedWindow('simulation', cv.WINDOW_KEEPRATIO)
        ratio_img =self.forme[1]/self.forme[0]
        cv.resizeWindow('simulation', (int(600*ratio_img), 600))
        while True:
            self.actualiser()
            if self.rogner:
                img=self.tab[self.dim]*255  
            else:
                img = self.tab*255
            cv.imshow("simulation", img.astype(np.uint8))
            if cv.waitKey(10) == ord('q'):
                break
        cv.destroyAllWindows()

    def creer_image(self, fichier, nb_etapes):
        """
        Sauvegarder une image de la simulation après nb_etapes itérations

        Args:
            fichier (str): nom du fichier où l'image est stockée
            nb_etapes (int): nombre d'itérations
        """
        self.initialisation()
        for _ in range(nb_etapes):
            self.actualiser()
        cv.imwrite("rendus/"+fichier, self.tab*255)

    def creer_video(self, fichier, nb_etapes):
        """
        Créer une vidéo de la simulation.
        Args:
            fichier (str): nom du fichier où la vidéo est stockée
            nb_etapes (int): nombre d'étapes dans la vidéo
        """
        self.initialisation()
        video = cv.VideoWriter(filename = "rendus/"+fichier, fourcc = cv.VideoWriter_fourcc(*"mp4v"), fps=10.0, frameSize=tuple(self.forme), isColor=False)

        for _ in range(nb_etapes):
            self.actualiser()
            image = self.tab*255
            video.write(image.astype(np.uint8))
        video.release()
dt=[0.02]

presets = [
    ([ 64, 24,  9,  3,  1], [ 96, 32, 12, 4.5, 1.5]),
    ([ 100, 20, 10, 5, 1], [ 200, 40, 20, 10, 2]),
    ([ 100, 50, 20, 10, 5, 1], [ 150, 75, 30, 15, 7.5, 1.5]),
    ([24,  9,  3,  1], [32, 12, 4.5, 1.5]),
]

if afficher_p:
    print("Valeurs prédéfinies pour la simulation de motifs de Turing à échelles multiples: (r_activ, r_inhib)")
    for i in range(len(presets)):
        print(str(i+1) + ".", presets[i])
    exit()

if not r_activ or not r_inhib:
    r_activ, r_inhib = presets[p-1]

Sim = MSTP((largeur, longueur), initialisation_aleatoire, r_activ, r_inhib, dt, symetrie, rogner)
   

if option==1:
    Sim.simulation()
elif option==2:
    Sim.creer_image(fichier, nb_etapes)
elif option==3:
    Sim.creer_video(fichier, nb_etapes)