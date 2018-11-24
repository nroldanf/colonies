# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 22:21:46 2018

@author: Nicolás, Lizu, Mafesita
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

from skimage.io import imread 
from skimage.color import rgb2gray
from scipy.stats import skew,kurtosis
from skimage.exposure import rescale_intensity
# In[Carga de los nombres de las imágenes]
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )

i = 1;j = 2
PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
I = imread(PATH)
# In[]
plt.close('all')

I = imread(PATH)
I_gray = rgb2gray(I)
I_cont = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))

I = I.astype('float')
I = I/255

names = ['Rojo','Verde','Azul']
for i in range(0,5):
    if i==3:
        plt.figure()
        plt.hist(I_gray.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
        plt.title('Escala de grises')
    elif i==4:
        plt.figure()
        plt.hist(I_cont.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
        plt.title('Con mejora de contraste')
    else:
        hist,bins = np.histogram(I[:,:,i].ravel(),256,[0,1])
        plt.figure()
        plt.hist(I[:,:,i].ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
        plt.title('Plano '+ names[i])

# Halla las estadisticas de un arreglo
def stats(v_corr):
    mean = np.mean(v_corr)
    skewness = skew(v_corr)
    kurt = kurtosis(v_corr)
    maximum = max(v_corr)
    minimum = min(v_corr)
    std = np.std(v_corr)
    stats = np.array([mean,skewness,kurt,maximum,minimum,std])
    return stats