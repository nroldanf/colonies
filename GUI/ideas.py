# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 10:59:53 2019

@author: Nicolas
"""

from skimage.io import imread
from scipy.ndimage.morphology import distance_transform_edt
from skimage.morphology import watershed
from skimage.color import rgb2gray
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
from skimage.morphology import white_tophat, black_tophat, opening, closing
from skimage.morphology import disk,ball,diamond
from skimage import exposure
from skimage.filters.thresholding import threshold_otsu, try_all_threshold
from scipy.misc import imsave
from funciones import*
from skimage.feature import peak_local_max

import matplotlib.pyplot as plt
import numpy as np

import os
# In[] Preprocesamiento

def loadImages(gen='Imagenes/'):
    
    folder_ids = os.listdir(gen)
    image_ids = list()#ID's de las imágenes
    #Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
    for i in range(0,len(folder_ids)):
        image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
        
    return folder_ids,image_ids

def plot_comparison(original, filtered, filter_name):

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filter_name)
    ax2.axis('off')

def hist_comparison(original,modified,name):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.hist(original.ravel(),256,[0,1])
    ax1.set_title('original')
    ax2.hist(modified.ravel(),256,[0,1])
    ax2.set_title(name)
    
def displayIMG(I,name):
    plt.figure()
    plt.axis('off')
    if len(I.shape) < 3:
        plt.imshow(I,cmap='gray')# One channel
    else:
        plt.imshow(I)# Multichannel
    plt.title()
    plt.show()
    
# In[]
# Proceso:
'''
Corrección gamma: Mejora de contraste, desplaza el histograma
Apertura: Define mejor las colonias y remueve ruido (une algunas)
Black Top Hat (I-cierre): Corrige la iluminación
Mejora de contraste: Para separar el histograma (bimodal)
Binarización Otsu
'''    
    
plt.close('all')
s1 = diamond(1)# Elemento estructurante para la apertura
s2 = diamond(6)# Elemento estructurante para el black Top Hat
I = imread('IM_supah.jpg')
Igray = rgb2gray(I)
Ieq = exposure.adjust_gamma(Igray,0.4)# Mejora de contraste
# Comparación de la mejora de contraste
plot_comparison(Igray,Ieq,'Corrección gamma')
hist_comparison(Igray,Ieq,'Corrección gamma')

Iop = opening(Ieq,s1)
plot_comparison(Ieq,Iop,'Apertura')
hist_comparison(Ieq,Iop,'Apertura')
# Retorna lo que sea más pequeño que el elemento estructurante
# Podría ser un parámetro definido por el usuario, basado en 
# la colonia más grande
If = black_tophat(Iop,s2)
plot_comparison(Iop,If,'Black Top Hat')
hist_comparison(Ieq,If,'Black Top Hat')
If2 = exposure.adjust_gamma(If,0.7)# Mejora de contraste
plot_comparison(If,If2,'Separación del histograma')
hist_comparison(If,If2,'Separación del histograma')
# Binarización
thresh = threshold_otsu(If2)
BW = If > thresh
plot_comparison(I,BW,'Binarización Otsu')

# In[] Watershed segmentation with distance transform
'''
Determinación de marcadores con transformada de distancia y máximos locales
Aplicación de segmentación por watershed basada en marcadores
'''
I = imread('IMTEST.png')# Imagen binaria: Blanco-Objetos, Negro-Fondo
# Transformada de distancia euclidiana:
# Asigna a cada pixel el valor de la distancia euclidiana al pixel de fondo
# más cercano.
dist = distance_transform_edt(I)
plot_comparison(I,dist,'Transformada de distancia')
# Máximos locales hallados en una vecindad de 3x3
local_maxi = peak_local_max(dist, indices=False, footprint=np.ones((3, 3)),
                            labels=I)
# footprint es la vecindad para hallar máximos regionales
plot_comparison(dist,local_maxi,'Máximos regionales')
markers = ndi.label(local_maxi)[0]# Lo convierte a una matriz de enteros
# Se invierte para que así los máximos ahora sean mínimos (catch basins)
labels = watershed(-dist, markers, mask=I)# Algoritmo basado en marcadores

plt.figure()
plt.axis('off')
plt.imshow(labels,  cmap=plt.cm.nipy_spectral, interpolation='nearest')
plt.title('Watershed')
plt.show()