# -*- coding: utf-8 -*-
"""
Created on Thu May 24 18:53:49 2018

@author: Nicolas
"""

import matplotlib.pyplot as plt
import os
import numpy as np
import scipy
import pandas as pd

from skimage.io import imread
from skimage.color import rgb2gray

from scipy.stats import skew,kurtosis

# In[] Análisis de las caracteristicas de las imágenes


gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
    
PATH = gen + folder_ids[0] + '/' + image_ids[0][1]
I = imread(PATH)
I_gray = rgb2gray(I)
#Planos
R = I[:,:,0]
G = I[:,:,1]
B = I[:,:,2]

fig,(ax_R, ax_G, ax_B) = plt.subplots(1, 3)
ax_R.imshow(R,cmap='gray')
ax_R.set_title('Plano Rojo')
#ax_R.set_axis_off()
ax_G.imshow(G,cmap='gray')
ax_G.set_title('Plano Verde')
#ax_G.set_axis_off()
ax_B.imshow(B,cmap='gray')
ax_B.set_title('Plano Azul')
#ax_B.set_axis_off()
fig.show()
# In[] Mejoras de contraste


# In[] Histogramas de la escala de grises y de cada plano 

hist,bins = np.histogram(R.ravel(),256,[0,255])
#hist1,bins1 = np.histogram(G.ravel(),256,[0,255])
#hist2,bins2 = np.histogram(B.ravel(),256,[0,255])
#
fig,(ax_R, ax_G, ax_B) = plt.subplots(3, 1)
ax_R.hist(R.ravel(),256,[0,256])
ax_R.set_title('Plano Rojo')
#ax_R.set_axis_off()
ax_G.hist(G.ravel(), 256,[0,256])
ax_G.set_title('Plano Verde')
#ax_G.set_axis_off()
ax_B.hist(B.ravel(),256,[0,256])
ax_B.set_title('Plano Azul')
#ax_B.set_axis_off()
fig.show()


#def planes_hist(m_I):
#    R = I[:,:,0]
#    G = I[:,:,1]
#    B = I[:,:,2]

#plt.figure()
#plt.hist(I_gray.ravel(),256,[0,256]); plt.show()

#fig= plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.plot(I_gray.ravel(),256,[0,256])
#plt.show()

#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.plot(bins3[:-1],histg)
#
#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.axis('off')
#ax1.imshow(I_gray,cmap='gray')
#


# In[] Estátisticos de las imágenes: Asimetría, Curtosis, Media, Máximo
# Ubicación del máximo (negro o blanco)

def stats(m_I,i):
    feat = list()
    feat.append( skew(m_I[:,:,i].ravel()) )
    feat.append( kurtosis(m_I[:,:,i].ravel()) ) 
    feat.append(np.mean(m_I[:,:,i].ravel()) )
    hist,bins = np.histogram(m_I[:,:,i].ravel(),256,[0,255])
    feat.append(np.argmax(hist)/255)
    return feat
        

d = {'Plano R': stats(I,0), 'Plano G':  stats(I,1), 'Plano B':  stats(I,2)}
df = pd.DataFrame(data=d)
df.index = ['Asimetría','Curtosis','Promedio','IndMáximo']
# In[] 

        