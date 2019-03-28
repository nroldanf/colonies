# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:49:59 2019

@author: Nicolas
"""
import numpy as np
import pandas as pd
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
from skimage.filters.thresholding import threshold_otsu
from skimage.transform import resize
from scipy.ndimage.morphology import distance_transform_edt
from skimage.morphology import watershed
from scipy import ndimage as ndi

# In[]
folders = ['05.04.2016','25.09.2015','26.04.2016']
# Imágenes del conteo automático
#gen_aut = 'Scripts/GUI/Resultados_GUI/'+folders[0]
#images_aut = []
#images_aut.append(os.listdir(gen_aut))
#images_aut = images_aut[0]
#images_aut = images_aut[14:]
#images_aut.pop(6)
#images_aut.pop(10)

# *** Otros programas ***
gen_aut = 'Resultados_Cellcounter/'+folders[0]
images_aut = []
images_aut.append(os.listdir(gen_aut))
images_aut = images_aut[0];
#images_aut.pop(6)
#images_aut.pop(10)

#images_aut.pop(11)
#images_aut.pop(10)
# *** Imágenes del conteo manual ***
gen = 'Fotos/Imagenes_Manual/'+folders[0]
images = []
images.append(os.listdir(gen))
images = images[0]
#images  = images[0:11]
#images.pop(0)
#images.pop(6)
# In[] CellProfiler
I = imread(gen_aut+'/'+images_aut[0])
Ig = rgb2gray(I)
t = threshold_otsu(Ig)# plano verde y umbraliza
BW = Ig > t

plt.figure()
plt.imshow(BW,cmap='gray')
plt.show()

# Otsu -> Watershed -> coordBlobs 
# In[] CellCounter

I = imread(gen_aut+'/'+images_aut[0])
Inew = colorPro(I[:,:,0:3],60)

plt.figure()
plt.imshow(Inew,cmap='gray')
plt.show()

# Igual que con las de OpenCFU -> segmentación por DE en cielab
# Tener en cuenta plano de luminancia

# In[]
im = 0
I = imread(gen+'/'+images[im]);[m,n,p] = I.shape
I2 = imread(gen_aut+'/'+images_aut[im])
I2 = resize(I2, [m,n], order=1, mode='reflect', cval=0, clip=True,preserve_range=False)

plt.figure()
plt.imshow(I2,cmap='gray')
plt.show()

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
        - 0 Propio, 1 manual: AND entre blobs, si 1 {elimine}w
        
    Sensibilidad: true positives/(true positives + false negatives)
    Especificidad: true negatives/(true negatives + false positives)
"""

# *** Inicialización ***
TP_FP = [[],[]]# lista de true positives and false positives
FN_TN = [[],[]]
sen1 = []
esp1 = []

names = ['True positives','False positives','False negatives','True negatives']
r_pozo = 140
r_small = 50
template = circle(r_small)
se = diamond(4)#elemento estructurante para el cierre
# **** OPENCFU *****
umbral_G = 30
#*******************
for im in range(0,len(images)):
    I = imread(gen+'/'+images[im]);[m,n,p] = I.shape
    I2 = imread(gen_aut+'/'+images_aut[im])
    I2 = resize(I2, [m,n], order=2, mode='reflect', cval=0, clip=True,preserve_range=False)
    I2 = I2[:,:,0:3];
    centros = corrCruz(I,template,r_pozo,se)
    # ************************ Manuales ****************************
#    BW_r1 = segColor(I,[255,0,0])# Rojo 255,0,0
    BW_r1 = colorPro(I,umbral_G)# segmenta el color verde
    BW_b1 = segColor(I,[0,0,255])# Azul 0,0,255
    
    plt.figure()
    plt.imshow(BW_r1[:,:,0],cmap='gray')
    plt.show()
    
    
    # ********************* opencfu**********************************
    BW_au1 = colorPro(I2,umbral_G)# segmenta el color verde
#    plt.figure()
#    plt.imshow(BW_au1[:,:,1],cmap='gray')
#    plt.show()
    t = threshold_otsu(BW_au1[:,:,1])# plano verde y umbraliza
    BW_au1 = BW_au1[:,:,1] > t
    plt.figure()
    plt.imshow(BW_au1,cmap='gray')
    plt.show()
    
    # ***************************************************************
    mBW = np.zeros([m,n])
    for p in range(0,len(centros)):
        try:
            BW_r = pozo(BW_r1,centros[p],r_pozo)
            BW_b = pozo(BW_b1,centros[p],r_pozo)
            BW_au = pozo(BW_au1,centros[p],r_pozo)        
            # Obtenga las coordenadas de cada region conectada
            coodR = coordBlobs(BW_r)# lista de listas de tuplas ordenadas (x,y)
            coodB = coordBlobs(BW_b)
            coodAu = coordBlobs(BW_au)     
            cA = [coodR,coodB,coodAu]
            
            for k in range(0,2):# Para máscara roja y azul
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
                                    
                        try:
                            if (cont/len(coodAu[obj2]))*100 >= 5:# Si por lo menos 50% de las coordenadas coincidieron
                                Tp += 1# Cuente un verdadero/falso positivo
                        except:
                            print('No se encontraron elementos en dicho pozo.')
                            
                TP_FP[k].append(Tp)# Adjunte el conteo una vez termine (acorde a la máscara)
                print(names[k] + ': ' + str(Tp))     
                
                FN_TN[k].append(len(cA[k])-Tp)
                print(names[k+2] + ': ' + str(len(cA[k])-Tp))  
                
                if k == 0:
                    try:
                        sen1.append( Tp/len(cA[k]))
                    except:
                        sen1.append(1)
                        print('No hay elementos en el pozo '+ str(p) + 'de ' + images[im])
                elif k == 1:
                    try:
                        esp1.append( (len(cA[k])-Tp) / len(cA[k]) )
                    except:
                        esp1.append(1)
                        print('No hay elementos en el pozo '+ str(p) + ' de ' + images[im])
                        
            imsave(gen_aut+'/Coincidencias'+'/'+images_aut[im].replace(".jpg",".tiff"),mBW)# Guarde la imagen BW
        except:
            print('Pozo no valido')
            

plt.figure()    
plt.imshow(mBW,cmap='gray')
plt.show()
            
    
TP_FP = np.array(TP_FP)
FN_TN = np.array(FN_TN)
#sen = TP_FP[0]/(TP_FP[0]+FN_TN[0])
#esp = FN_TN[1]/(FN_TN[1]+TP_FP[1])

t = np.arange(0.0,len(sen1),1)
l1 =  str("%.2f" % np.mean(sen1)) + ' ± ' + str("%.2f" % np.std(sen1))
l2 =  str("%.2f" % np.mean(esp1)) + ' ± ' + str("%.2f" % np.std(esp1))

plt.figure()
plt.hist(sen1,range=[0,1],label=l1)
plt.xlabel('Sensibilidad')
plt.ylabel('Pozos detectados')
plt.grid()
plt.legend()
plt.show()

plt.figure()
plt.hist(esp1,range=[0,1],label=l2)
plt.xlabel('Especificidad')
plt.ylabel('Pozos detectados')
plt.grid()
plt.legend()
plt.show()

d = {'TP':TP_FP[0,:], 'FP':TP_FP[1,:],'FN':FN_TN[0,:],'TN':FN_TN[1,:],
     'SEN': sen1,'ESP': esp1}
df = pd.DataFrame(data=d)

#tabla = []
#tabla.append(df)
with pd.ExcelWriter('CellCounter_05.04.2016' + '.xlsx') as writer:
            df.to_excel(writer, sheet_name='05.04.2016')

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
    if coordinates[0][1] < coordinates[1][1]:
        y = coordinates[0][0]-r_pozo-5
        x = coordinates[0][1]+r_pozo+5
    else:
        y = coordinates[1][0]-r_pozo-5
        x = coordinates[1][1]+r_pozo+5
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
    m = I.shape
    Im = np.zeros([m[0],m[1]])    
    n = [c[1]-r,c[1]+r,c[0]-r,c[0]+r]
    for i in range(n[0],n[1]):
        for j in range(n[2],n[3]):
            d = np.sqrt(abs((c[1]-i)**2+(c[0]-j)**2)) 
            if d < r:
                Im[i,j] = I[i,j]
    return Im


#def color(I,c,r):
#    for n in range(0,3):
#        I[:,:,n] = pozos2(I[:,:,n],c,r,prom)
##    prome = np.asarray(prom)#vuelvo arreglo la lista de listas prom
#    I_color = rgb2lab(I,illuminant='D65',observer='2')
#    promedio = [np.mean(I_color[:,:,1] ),np.mean(I_color[:,:,2])]
#    for i in range(0,n):
#        j = prom[i]
#        dist = np.linalg.norm(promedio-I_color[j[0],[1],1::])
#        if dist < 5:
#            IRGB[j[0],j[1]] = 1
#    IRGB = (1 - IRGB)> 0.7
#    I_fin = (I_gray + IRGB) > 0.9
#    return I_fin

def colorPro(I,umbral):
    I_color = rgb2lab(I,illuminant='D65',observer='2')
    m = np.shape(I_color[:,:,0])
    promedio = [ np.mean( I_color[:,:,1] ) , np.mean( I_color[:,:,2]) ]
    for i in range(0,m[0]):
        for j in range(0,m[1]):
            pix = I_color[i,j,1::]
            dist = np.linalg.norm(promedio - pix)
            if dist < umbral:
                I[i,j,0] = 0
                I[i,j,1] = 0
                I[i,j,2] = 0
    return I

def watershedDT(self,I):
    dist = distance_transform_edt(I)
    # Máximos locales hallados en una vecindad de 3x3
    local_maxi = peak_local_max(dist, indices=False, footprint=np.ones((3, 3)),
                                labels=I)
    # footprint es la vecindad para hallar máximos regionales
    markers = ndi.label(local_maxi)[0]# Lo convierte a una matriz de enteros
    # Se invierte para que así los máximos ahora sean mínimos (catch basins)
    labels = watershed(-dist, markers, mask=I)# Algoritmo basado en marcadores
    return labels