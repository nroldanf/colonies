# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:07:31 2019

@author: Nicol
"""

# In[]

from clase import Colonias

from skimage.io import imread
import matplotlib.pyplot as plt
# In[]
# Prueba
plt.close('all')
I = imread('im_test.jpg')
Im = Colonias(I)
centros = Im.corr2d()


result = Im.processing()
#a = Im.pozo(centros[0])
#a = Im.otsu(a,Im.mejoraConstraste(),centros[0])
#b,prom = Im.pozo_anillo(Im.mejoraConstraste(),centros[0])

b = Im.color(Im.mejoraConstraste(),centros[0])

# I: Imagen en esquema de codificación RGB.
#        I_gray: Imagen en esquema de codificación de escala de grises.
#        centro: Coordenadas del centro de un pozo.
#        r_pozo: Radio del pozo en pixeles.

plt.figure()
plt.axis('off')    
plt.imshow(result,cmap='gray')
plt.show()

#for i in range(0,len(centros)):
#    I_seg = Im.pozo(centros[i])
#    plt.figure()
#    plt.axis('off')    
#    plt.imshow(I_seg)
    
    