import numpy as np 
import cv2 as cv
import time

HAUTEUR = 480
LARGEUR = 640
tab = np.zeros((HAUTEUR,LARGEUR,3),np.uint8)
cv.rectangle(tab, (LARGEUR//2-100,HAUTEUR//2-100), (LARGEUR//2+100,HAUTEUR//2+100), (255,255,0), -1)
cv.imshow("simulation", tab)
f=0.25
k=0.25
dA = 0.5
dB = 0.5
alpha=0.1
nabla=np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])

def update():
  conv = np.tab = np.zeros((HAUTEUR,LARGEUR,3),np.uint8)
  for x in range(HAUTEUR-2):
    for y in range(LARGEUR-2):
      conv[x][y][0] = np.sum(tab[x:x+3, y:y+3][:0]*nabla)
      conv[x][y][1] = np.sum(tab[x:x+3, y:y+3][:1]*nabla)

  for x in range(HAUTEUR):
    for y in range(LARGEUR):
      deltaA = dA*conv[x][y][0]-tab[x][y][0]*(tab[x][y][1]**2)+f*(1-tab[x][y][0])
      deltaB = dB*conv[x][y][0]+tab[x][y][0]*(tab[x][y][1]**2)-(k+f)*tab[x][y][1]
      tab[x][y][0] += alpha*deltaA
      tab[x][y][1] += alpha*deltaB

for i in range(10):
  update()
  time.sleep(1)


cv.waitKey(0)
cv.destroyAllWindows()