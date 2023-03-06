import numpy as np 
import cv2 as cv
import time
import itertools




HAUTEUR = 500
LARGEUR = 500
tab = np.random.rand(HAUTEUR,LARGEUR,3)
for y in range(HAUTEUR):
     for x in range(LARGEUR):
        tab[y][x][2] = 0
prochain = np.copy(tab)

cv.imshow("simulation", tab)
time.sleep(5)

def echanger(tab, prochain):
  temp = np.copy(tab)
  tab = np.copy(prochain)
  prochain = np.copy(temp)

# f=0.25
# k=0.05
# dA = 2.8e-4
# dB = 5e-3


# nabla=np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])

# a = 2.8e-4
# b = 5e-3
# tau = .1
# k = -.005

# dx=2./HAUTEUR
# T = 9.0  # total time
# dt = .01  # time step
# n = int(T / dt)  # number of iterations

# def laplacian(Z):
#     Ztop = Z[0:-2, 1:-1]
#     Zleft = Z[1:-1, 0:-2]
#     Zbottom = Z[2:, 1:-1]
#     Zright = Z[1:-1, 2:]
#     Zcenter = Z[1:-1, 1:-1]
#     return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2



# fps = 5
# delai = 1./fps

# tps = tps_vise = time.time()
# for i in range(10):
#   ancien_tps, tps = tps, time.time()
#   delta_tps = tps-ancien_tps
#   for y in range(HAUTEUR):
#      for x in range(LARGEUR):
#        prochain=tab*1.01
#   echanger(tab, prochain)
#   cv.imshow("simulation", pixels)
#   tps_vise += delai
#   attente = tps_vise - time.time() 
#   if attente > 0:
#     time.sleep(attente)

cv.waitKey(0)
cv.destroyAllWindows()