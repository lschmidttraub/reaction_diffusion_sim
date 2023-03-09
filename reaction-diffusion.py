import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import cv2 as cv

def laplacian1D(a, dx):
    return (
        - 2 * a
        + np.roll(a,1,axis=0) 
        + np.roll(a,-1,axis=0)
    ) / (dx ** 2)

def laplacian2D(a, dx):
    return (
        - 4 * a
        + np.roll(a,1,axis=0) 
        + np.roll(a,-1,axis=0)
        + np.roll(a,+1,axis=1)
        + np.roll(a,-1,axis=1)
    ) / (dx ** 2)

def random_initialization(shape):
    return (np.random.normal(loc=0, scale=0.05, size=shape), np.random.normal(loc=0, scale=0.05, size=shape))

class Simulation1D():
    def __init__(self, Da, Db, Ra, Rb, initializer, width=1000, dx=1, dt=0.1, steps=1):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.initializer = initializer
        self.width = width
        self.dx = dx
        self.dt = dt
        self.steps = steps
    
    def initialize(self):
        self.t = 0
        self.a, self.b = self.initializer(self.width)
    
    def update(self):
        for i in range(self.steps):
            self.t += self.dt
            lapA = laplacian1D(self.a, self.dx)
            lapB = laplacian1D(self.b, self.dx)
            deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
            deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
            self.a += deltaA
            self.b += deltaB


    def draw(self, ax):
        ax.clear()
        ax.plot(self.a, color="b", label="A")
        ax.plot(self.b, color="g", label="B")
        ax.legend()
        ax.set_ylim(-1,1)
        ax.set_title("t = {:.2f}".format(self.t))
    
    def initialize_figure(self):
        fig, ax = plt.subplots()
        return fig, ax
    
    def plot_evolution_outcome(self, filename, n_steps):
        """
        Evolves and save the outcome of evolving the system for n_steps
        """
        self.initialize()
        fig, ax = self.initialize_figure()
        
        for _ in range(n_steps):
            self.update()

        self.draw(ax)
        fig.savefig(filename)
        plt.close()

    def plot_time_evolution(self, filename, n_steps=30):
        """
        Creates a gif from the time evolution of a basic state syste.
        """
        self.initialize()
        fig, ax = self.initialize_figure()

        def step(t):
            self.update()
            self.draw(ax)

        anim = animation.FuncAnimation(fig, step, frames=np.arange(n_steps), interval=20)
        anim.save(filename=filename, dpi=60, fps=10, writer='pillow')
        plt.close()

class Simulation2D():
    def __init__(self, Da, Db, Ra, Rb, initializer, width=1000, height = 1000, dx=1, dt=0.1, steps=1):
        self.Da = Da
        self.Db = Db
        self.Ra = Ra
        self.Rb = Rb
        self.initializer = initializer
        self.width = width
        self.height = height
        self.dx = dx
        self.dt = dt
        self.steps = steps
    
    def initialize(self):
        self.t = 0
        self.a, self.b = self.initializer((self.height, self.width))
    
    def update(self):
        for i in range(self.steps):
            self.t += self.dt
            self._update()
            
    def _update(self):
        lapA = laplacian2D(self.a, self.dx)
        lapB = laplacian2D(self.b, self.dx)
        deltaA = self.dt*(self.Da*lapA+self.Ra(self.a,self.b))
        deltaB = self.dt*(self.Db*lapB+self.Rb(self.a,self.b))
        self.a += deltaA
        self.b += deltaB

    def draw(self, ax):
        ax.clear()

        ax.imshow(self.a)

        ax.set_title("A, t = {:.2f}".format(self.t))
    
    def initialize_figure(self):
        fig, ax = plt.subplots(figsize = (10,10))
        return fig, ax
    
    def real_time_sim(self):
        self.initialize()
        cv.namedWindow('simulation', cv.WINDOW_KEEPRATIO)
        cv.resizeWindow('simulation', 300, 300)
        while True:
            self.update()
            cv.imshow("simulation", self.a*255)
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()

    def create_png(self, filename, n_steps):
        """
        Evolves and save the outcome of evolving the system for n_steps
        """
        self.initialize()
        fig, ax = self.initialize_figure()
        for i in range(n_steps):
            self.update()
        
        
        self.draw(ax)
        fig.savefig(filename)
        plt.close()

    def create_gif(self, filename, n_steps=30):
        """
        Creates a gif from the time evolution of a basic state syste.
        """
        self.initialize()
        fig, ax = self.initialize_figure()
        def step(t):
            self.update()
            self.draw(ax)

        anim = animation.FuncAnimation(fig, step, frames=np.arange(n_steps), interval=20)
        anim.save(filename=filename, dpi=60, fps=10, writer='pillow')
        plt.close()
    
    def create_video(self, filename, n_steps=30):
        """
        Creates a video from the time evolution of a basic state syste.
        """
        self.initialize()
        video = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"FFV1"), fps=10, frameSize=(100, 100), isColor=False)
        for i in range(n_steps):
            self.update()
            frame = self.a*255
            video.write(frame)
            # if i%10==0:
            #     cv.imshow("simulation", frame)
            #     cv.waitKey(0)
            #     cv.destroyAllWindows()
        video.release()

Da, Db, alpha, beta = 1, 100, -0.005, 10

def Ra(a,b): 
    return a - a ** 3 - b + alpha
def Rb(a,b): 
    return (a - b) * beta

width = 100
dx = 1
dt = 0.001
Sim2  = Simulation2D(Da, Db, Ra, Rb, random_initialization, width = width, height = width, dx=dx, dt=dt, steps=250)
# Sim2.plot_time_evolution("graph.avi", 50)
# Sim2.plot_evolution_outcome("output.png", 50)
# Sim2.real_time_sim()

