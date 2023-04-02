import numpy as np
import cv2 as cv
from reaction_diffusion import laplacien2D, initialisation_aleatoire



class MSTP():
    def __init__(self, forme, initialisateur, nb_echelles, activiteurs, inhibiteurs, quantites, poids, dt):
        self.forme=forme
        self.initialisateur = initialisateur
        self.nb_echelles = nb_echelles
        self.activiteurs = activiteurs
        self.inhibiteurs = inhibiteurs
        self.quantites = quantites
        self.poids = poids
        self.dt = dt

    def initialisation(self):
        self.tab=self.initialisateur(self.forme)

    def actualiser(self, nb_etapes):
        

Sim = MSTP()