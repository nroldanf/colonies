# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:49:59 2019

@author: Nicolas
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from skimage.io import imread
from scipy.misc import imsave
from skimage.color import rgb2lab
import os

from skimage.measure import label
from skimage.measure import regionprops

from skimage.exposure import rescale_intensity
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import closing
from skimage.color import rgb2gray
from skimage.morphology import diamond

# In[]
# Load images PATHS

# Cargar PATHS de imágenes de validación de carpeta "Imagenes_validación"
# (Tener en cuenta que aún no están binarizadas)

gen = 'Imagenes_validacion/'
images_man = []
images_man.append(os.listdir(gen));images_man = images_man[0]

# Cargar PATH de imágenes del algoritmo de carpeta "Resultados_GUI/2019-02-14"

gen2 = 'Resultados_GUI/2019-02-14/'
images_aut = []
images_aut.append(os.listdir(gen2));
images_aut = images_aut[0][14:21]

# In[] Binarización de Ground Truth

# Máscara de la de puntos rojos para cálculo de especificidad
# Máscara de la de puntos azules para cálculo de sensibilidad

# Necesario obtener las coordenadas de cada objeto con regionprops

"""
    - Con las imágenes con marcaciones, segmentar el color.
    - Obtener las coordenadas de cada blob.
    -Calcular la distancia euclidiana a todos los puntos en una vecindad pequeña
    luego, hallar el min (vecino más cercano)
    - Con el vecino más cercano, calcular el error.
    
    True positive = correctly identified
        - 1 propio, 1 manual: AND entre blobs, si 1 {conserve}
    False positive = incorrectly identified
        - 1 propio, 0 manual
    True negative = correctly rejected
        - 0 Propio, 0 manual: 
    False negative = incorrectly rejected
        - 0 Propio, 1 manual: AND entre blobs, si 1 {elimine}
        
    Sensibilidad: true positives/(true positives + false negatives)
    Especificidad: true negatives/(true negatives + false positives)
"""

            
# verifique que está en la primer lista de coodAu -> segunda -> ...

# para cada imagen

[],[],[],[],[],[]

TP_FP = [[],[]]# lista de true positives and false positives
FN_TN = [[],[]]



names = ['True positives','False positives','False negatives','True negatives']
r_pozo = 140
r_small = 50
template = circle(r_small)
se = diamond(4)#elemento estructurante para el cierre

# TP, FN, 
for im in range(0,len(images_man)):
    I = imread(gen+images_man[im])
    I2 = imread(gen2+images_aut[im])    
    centros = corrCruz(I,template,r_pozo,se)
    BW_r1 = segColor(I,[255,0,0])# Rojo 255,0,0
    BW_b1 = segColor(I,[0,0,255])# Azul 0,0,255
    # Aunque la imagen está en blanco y negro, tiene valores intensidad 
    # diferentes de 0 y 1
    BW_au1 = I2 > 220
    BW_au1 = BW_au1.astype('float64')
    #Para cada pozo
    for p in range(0,len(centros)):
        BW_r = pozo(BW_r1,centros[p],r_pozo)
        BW_b = pozo(BW_b1,centros[p],r_pozo)
        BW_au = pozo(BW_au1,centros[p],r_pozo)
        # Obtenga las coordenadas de cada region conectada
        coodR = coordBlobs(BW_r)# lista de listas de tuplas ordenadas (x,y)
        coodB = coordBlobs(BW_b)
        coodAu = coordBlobs(BW_au)        
        
        cA = [coodR,coodB,coodAu]
        s = BW_r.shape
        for k in range(0,2):# Para máscara roja y azul
            mBW = np.zeros([s[0],s[1]])
            Tp = 0    
            for obj in range(0,len(cA[k])):# Para cada objeto dentro de la manual (lista de listas(tuplas))
                for obj2 in range(0,len(coodAu)):# Para cada objeto dentro de la automática
                    cont = 0# Contador de coordenadas comunes
                    for i in range(0,len(cA[k][obj])):# Para cada lista(tupla) del manual
                        for j in range(0,len(coodAu[obj2])):# Para cada lista(tupla) de la automática
                            if np.array_equal(cA[k][obj][i],coodAu[obj2][j]):# son iguales las tuplas?
                                cont += 1
                                c = coodAu[obj2][j]
                                mBW[c[0]][c[1]] = 1
                                
                    if (cont/len(coodAu[obj2]))*100 >= 40:# Si por lo menos 50% de las coordenadas coincidieron
                        Tp += 1# Cuente un verdadero/falso positivo
    #                    del cA[k][obj]# Remuve el elemento para que no tenga que compararlo de nuevo
                        
            TP_FP[k].append(Tp)# Adjunte el conteo una vez termine (acorde a la máscara)
            print(names[k] + ': ' + str(Tp))     
            
            FN_TN[k].append(len(cA[k])-Tp)
            print(names[k+2] + ': ' + str(len(cA[k])-Tp))  


#Sensibilidad: true positives/(true positives + false negatives)
#Especificidad: true negatives/(true negatives + false positives)
    
TP_FP = np.array(TP_FP)
FN_TN = np.array(FN_TN)
sen = TP_FP[0]/(TP_FP[0]+FN_TN[0])
esp = FN_TN[1]/(FN_TN[1]+TP_FP[1])

t = np.arange(0.0,len(sen),1)
l1 =  str("%.2f" % np.mean(sen)) + ' ± ' + str("%.2f" % np.std(sen))
l2 =  str("%.2f" % np.mean(esp)) + ' ± ' + str("%.2f" % np.std(esp))


plt.figure()
plt.hist(sen,range=[0,1],label=l1)
plt.title('Sensibilidad')
plt.grid()
plt.legend()
plt.show()

plt.figure()
plt.hist(esp,range=[0,1],label=l2)
plt.title('Especificidad')
plt.grid()
plt.legend()
plt.show()


# In[]
images = images[0:4]
for im in range(0,len(images)):
    I = imread(gen+images[im])
    I = I[:,:,0:3]
    s = I.shape
    BWred = np.ones([s[0],s[1]])
    BWblue = np.ones([s[0],s[1]])
    for i in range(0,s[0]):
        for j in range(0,s[1]):
            if (I[i,j,0] == 255) and (I[i,j,1] == 0) and (I[i,j,2] == 0):
                BWred[i,j] = 1
            else:
                BWred[i,j] = 0
            
            if (I[i,j,0] == 0) and (I[i,j,1] == 0) and (I[i,j,2] == 255):
                BWblue[i,j] = 1
            else:
                BWblue[i,j] = 0

    imsave('Si'+images[im],BWred)
    imsave('No'+images[im],BWblue)

# In[]
def loadImages(gen='Imagenes/'):
    
    folder_ids = os.listdir(gen)
    image_ids = list()#ID's de las imágenes
    #Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
    for i in range(0,len(folder_ids)):
        image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
        
    return folder_ids,image_ids

def pozos(m_I,centros,r):
    h,w = m_I.shape
    I_new = np.ones([h,w])#matriz blanca
    for i in range(0,h):
        for j in range(0,w):
            x = centros[:,0] - j
            y = centros[:,1] - i
            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
            if any ( np.logical_and(d <= r,d >= r - 20) ):
                I_new[i,j] = m_I[i,j]


    return I_new


def hist_comparison(original,modified,name):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.hist(original.ravel(),256,[0,255])
    ax1.set_title('original')
    ax2.hist(modified.ravel(),256,[0,255])
    ax2.set_title(name)
    
    
def segColor(I,tri):
    s = I.shape
    BW = np.ones([s[0],s[1]])
    for i in range(0,s[0]):
        for j in range(0,s[1]):
            if (I[i,j,0] == tri[0]) and (I[i,j,1] == tri[1]) and (I[i,j,2] == tri[2]):
                BW[i,j] = 1
            else:
                BW[i,j] = 0
            
    return BW


def coordBlobs(BW):
    coord = []
    lb = label(BW,neighbors=8, background=0)
    for region in regionprops(lb):
        coord.append(region.coords)#matriz de coordenadas
    return coord

def addColor(I,BW):
    R = I[:,:,0]
    G = I[:,:,1]
    B = I[:,:,2]
    BW[BW > 200] = 255
    s = BW.shape
    for i in range(0,s[0]):
        for j in range(0,s[1]):
            if BW[i,j] == 255:
                R[i,j] = 255
                G[i,j] = 0
                B[i,j] = 0        
    I[:,:,0] = R
    I[:,:,1] = G
    I[:,:,2] = B
    return I
    

def corr2d(coordinates,template,r_pozo):
    '''
    Realiza la correlación cruzada normalizada [1] con una imagen template y
    retorna los centros de obtenidos de la correlación.
    
    Args:
        coordinates: Coordenadas de los centros de los circulos del
        recipiente.
        template: Imagen con el template para realizar la correlación.
        r_pozo: Radio del pozo en píxeles.
    
    Retorna: 
        centros: Arreglo de coordenadas (x,y) con los centros de los pozos
        ubicados en el siguiente orden .   
    '''
    #podría reeemplazar el if-else:
#    coordinates = np.sort(coordinates, axis=1, kind='quicksort', order=None)
    if coordinates[0][1] < coordinates[1][1]:
        y = coordinates[0][0]-r_pozo-5
        x = coordinates[0][1]+r_pozo+5
    else:
        y = coordinates[1][0]-r_pozo-5
        x = coordinates[1][1]+r_pozo+5
    #coordenadas de los otros pozos por simetría
    centros = [[x,y],[x,y+2*r_pozo + 10]]
    for i in range(0,2):
        centros.append([centros[i][0] + 2*r_pozo + 10 ,centros[i][1] ])
        centros.append([centros[i][0] - 2*r_pozo - 10,centros[i][1] ])    
    centros = sorted(centros)
    centros = np.asarray(centros)#(x,y)    
    return centros

def corrCruz(I,template,r_pozo,s):
    Igray = rgb2gray(I)
    Imejora = rescale_intensity(Igray,in_range=(0.2,0.8),out_range=(0,1))
    BW = canny(Imejora,sigma=0.5)
    BW = closing(BW,s)
    result = match_template(BW,template,pad_input = True)
    coordinates = peak_local_max(result, min_distance=160)#centro del pequeño 
    centros = corr2d(coordinates,template,r_pozo)
    
    return centros

def circle(r):
    '''
    Genera un template circular negro con radio r.
    Args:
        r: int con el radio del círculo en píxeles.
    Retorna: 
        Matriz que describe un círculo con radio r píxeles.
    '''
    dim = r*2 + 15#dimensión de la matriz.
    Circ = np.zeros([dim,dim])
    c = dim/2
    for i in range(0,dim):
        for j in range(0,dim):
            d = np.sqrt(abs((c-i)**2+(c-j)**2))
            if d > r and d < r+4:
                Circ[i,j] = 1
    return Circ



def pozo(I,c,r):
    '''
    Secciona 1 pozo de forma tal que para todo píxel P(i,j) que se encuentre 
    a una distancia d menor o igual a r, se conserve su valor original en 
    escala de grises, de lo contrario, se le asigna un valor de 0 (Blanco).
    
    Args: 
        m_I: Imagen de 1 dimensión.
        centros: Coordenadas de los centros de los pozos (x,y) en 
        un arreglo de np.
        r: Radio del pozo en píxeles.

    Retorna I_new: Imagen con el pozo seccionado.
    '''
    m = I.shape
    Im = np.zeros([m[0],m[1]])    
    n = [c[1]-r,c[1]+r,c[0]-r,c[0]+r]
    for i in range(n[0],n[1]):
        for j in range(n[2],n[3]):
            d = np.sqrt(abs((c[1]-i)**2+(c[0]-j)**2)) 
            if d < r:
                Im[i,j] = I[i,j]
    return Im