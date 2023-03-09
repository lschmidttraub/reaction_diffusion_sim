import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import cv2 as cv

def laplacien1D(a, dx):
    '''
    Calcul de l'opérateur laplacien discrétisé dans un tableau à une dimension
    '''
    return (
        - 2 * a
        + np.roll(a,1,axis=0) 
        + np.roll(a,-1,axis=0)
    ) / (dx ** 2)

def laplacien2D(a, dx):
    '''
    Calcul de l'opérateur laplacien discrétisé dans un tableau à 2 dimensions
    '''
    return (
        - 4 * a
        + np.roll(a,1,axis=0) 
        + np.roll(a,-1,axis=0)
        + np.roll(a,+1,axis=1)
        + np.roll(a,-1,axis=1)
    ) / (dx ** 2)

def initialisation_aleatoire(shape):
    '''
    Permet de générer deux tableau à valeurs aléatoires a et b
    '''
    return (np.random.normal(loc=0, scale=0.05, size=shape), np.random.normal(loc=0, scale=0.05, size=shape))

class Simulation1D():
    '''
    Simulation d'un système de réaction-diffusion dans une dimension
    '''
    def __init__(self, Da, Db, Ra, Rb, f_init, largeur=1000, dx=1, dt=0.1, etapes=1):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.f_init = f_init
        self.largeur = largeur
        self.dx = dx
        self.dt = dt
        self.etates = etapes
    
    def initialisation(self):
        '''
        Initialise les paramètres de la simulation
        '''
        self.t = 0
        self.a, self.b = self.f_init(self.largeur)
    
    def actualiser(self):
        '''
        Actualise la fonction pour simuler le système de réaction diffusion
        '''
        for _ in range(self.etapes):
            self.t += self.dt
            lapA = laplacien1D(self.a, self.dx)
            lapB = laplacien1D(self.b, self.dx)
            deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
            deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
            self.a += deltaA
            self.b += deltaB


    def tracer(self, ax):
        '''
        Trace la figure
        '''
        ax.clear()
        ax.plot(self.a, color="b", label="A")
        ax.plot(self.b, color="g", label="B")
        ax.legend()
        ax.set_ylim(-1,1)
        ax.set_title("t = "+str(self.t))
    
    def initialisation_graphique(self):
        '''
        Initialise le graphique matplotlib
        '''
        fig, ax = plt.subplots()
        return fig, ax
    
    def creer_image(self, fichier, nb_etapes):
        ''''
        Sauvegarde le résultat après nb_etapes itérations dans un fichier image
        '''  
        self.initialisation()
        fig, ax = self.initialisation_graphique()
        
        for _ in range(nb_etapes):
            self.actualiser()

        self.tracer(ax)
        fig.savefig(fichier)
        plt.close()

    def creer_gif(self, fichier, nb_etapes=30):
        '''
        Génère un GIF de l'évolution de la courbe à travers le temps
        '''
        self.initialisation()
        fig, ax = self.initialisation_graphique()

        def etape(t):
            self.actualiser()
            self.tracer(ax)

        anim = animation.FuncAnimation(fig, etape, frames=np.arange(nb_etapes), interval=20)
        anim.save(filename=fichier, dpi=60, fps=10, writer='pillow')
        plt.close()

class Simulation2D():
    '''
    Simulation d'un système de réaction-diffusion dans 2 dimensions
    '''
    def __init__(self, Da, Db, Ra, Rb, f_init, largeur=1000, hauteur = 1000, dx=1, dt=0.1, etapes=1):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.f_init = f_init
        self.largeur = largeur
        self.hauteur = hauteur
        self.dx = dx
        self.dt = dt
        self.etapes = etapes
    
    def initialisation(self):
        '''
        Initialise les paramètres de la simulation
        '''
        self.t = 0
        self.a, self.b = self.f_init((self.hauteur, self.largeur))
    
    def actualiser(self):
        '''
        Actualise la fonction pour simuler le système de réaction diffusion
        '''
        for _ in range(self.etapes):
            self.t += self.dt
            lapA = laplacien2D(self.a, self.dx)
            lapB = laplacien2D(self.b, self.dx)
            deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
            deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
            self.a += deltaA
            self.b += deltaB

    def tracer(self, ax):
        '''
        Trace le graphique du tableau de concentrations de la substance A
        '''
        ax.clear()
        ax.imshow(self.a)
        ax.set_title("A, t = "+str(self.t))
    
    def initialisation_graphique(self):
        '''
        Initialise le graphique matplotlib
        '''
        fig, ax = plt.subplots(figsize = (10,10))
        return fig, ax
    
    def simulation(self, couleur=False):
        self.initialisation()
        cv.namedWindow('simulation', cv.WINDOW_KEEPRATIO)
        cv.resizeWindow('simulation', 300, 300)
        while True:
            self.actualiser()
            if couleur:
                image = np.stack((self.a*255, np.zeros((self.largeur, self.hauteur)), self.b*255), axis=2)
            else:
                image = self.a*255
            cv.imshow("simulation", image)
            if cv.waitKey(10) == ord('q'):
                break
        cv.destroyAllWindows()

    def creer_image(self, fichier, nb_etapes):
        ''''
        Sauvegarde le résultat après nb_etapes itérations dans un fichier image
        '''  
        self.initialisation()
        fig, ax = self.initialisation_graphique()
        for i in range(nb_etapes):
            self.actualiser()
        
        
        self.tracer(ax)
        fig.savefig(fichier)
        plt.close()

    def creer_gif(self, fichier, nb_etapes=30):
        '''
        Génère un GIF de l'évolution de la concentration de la substance A à travers le temps
        '''
        self.initialisation()
        fig, ax = self.initialisation_graphique()
        def etape(t):
            self.actualiser()
            self.tracer(ax)

        anim = animation.FuncAnimation(fig, etape, frames=np.arange(nb_etapes), interval=20)
        anim.save(filename=fichier, dpi=60, fps=10, writer='pillow')
        plt.close()
    
    def creer_video(self, fichier, nb_etapes=30, couleur=False):
        '''
        Créé une vidéo de la réaction, en couleur ou en noir et blanc
        '''
        self.initialisation()
        if couleur:
            video = cv.VideoWriter(fichier, cv.VideoWriter_fourcc(*"mp4v"), fps=10.0, frameSize=(self.largeur, self.hauteur))
        else:
            video = cv.VideoWriter(fichier, cv.VideoWriter_fourcc(*"mp4v"), fps=10.0, frameSize=(self.largeur, self.hauteur), isColor=False)

        for _ in range(nb_etapes):
            self.actualiser()
            if couleur:
                image = np.stack((self.a*255, np.zeros((self.largeur, self.hauteur)), self.b*255), axis=2)
            else:
                image = self.a*255
            video.write(image.astype(np.uint8))
        video.release()

Da, Db, alpha, beta = 1, 40, -0.005, 15

def Ra(a,b): 
    return a - a ** 3 - b + alpha
def Rb(a,b): 
    return (a - b) * beta

largeur = 250
dx = 1
dt = 0.001
Sim2  = Simulation2D(Da, Db, Ra, Rb, initialisation_aleatoire, largeur = largeur, hauteur = largeur, dx=dx, dt=dt, etapes=250)
Sim2.creer_video("rendu.mp4", 250, couleur=True)
# Sim2.creer_image("output.png", 50)
# Sim2.simulation(couleur=True)