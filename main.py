import numpy as np 
import cv2 as cv
import time

HAUTEUR = 500
LARGEUR = 500
tab = np.zeros((HAUTEUR,LARGEUR,3),np.uint8)
A = np.random.rand(HAUTEUR,LARGEUR)
B = np.random.rand(HAUTEUR,LARGEUR) 
for y in range(HAUTEUR):
  for x in range(LARGEUR):
    tab[y][x] = (int(A[y][x]*255), int(B[y][x]*255), 255)
cv.imshow("simulation", tab)


# f=0.25
# k=0.05
# dA = 2.8e-4
# dB = 5e-3


# nabla=np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])

a = 2.8e-4
b = 5e-3
tau = .1
k = -.005

dx=2./HAUTEUR
T = 9.0  # total time
dt = .001  # time step
n = int(T / dt)  # number of iterations

def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2

def pixels():
   for y in range(HAUTEUR):
     for x in range(LARGEUR):
        tab[y][x] = (int(A[y][x]*255), int(B[y][x]*255), 255)

for i in range(n):
  time.sleep(0.01)
  deltaA = laplacian(A)
  deltaB = laplacian(B)
  Ac = A[1:-1, 1:-1]
  Bc = B[1:-1, 1:-1]
  # We update the variables.
  A[1:-1, 1:-1], B[1:-1, 1:-1] = Ac + dt * (a * deltaA + Ac - Ac**3 - Bc + k), Bc + dt * (b * deltaB + Ac - Bc) / tau
  # Neumann conditions: derivatives at the edges
  # are null.
  for Z in (A, B):
    Z[0, :] = Z[1, :]
    Z[-1, :] = Z[-2, :]
    Z[:, 0] = Z[:, 1]
    Z[:, -1] = Z[:, -2]
  if i % (n//9) == 0:
    pixels()
    cv.imshow("simulation", tab)




cv.waitKey(0)
cv.destroyAllWindows()