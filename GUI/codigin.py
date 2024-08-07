"""
Created on Sun Jun 10 16:20:43 2018
@authors: Nicolás, Lizeth, María Fernanda
"""
#Librerias
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import numpy as np
import pandas as pd
import math

from skimage.io import imread 
from skimage.color import rgb2gray,rgb2lab
from skimage.exposure import rescale_intensity
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import dilation, closing
from skimage.morphology import remove_small_objects,binary_dilation
from skimage.morphology import disk,ball,diamond
from skimage.filters.thresholding import threshold_otsu
from skimage.color import label2rgb
from skimage.measure import label
from skimage.measure import regionprops

from funciones import *

# In[Carga de los nombres de las imágenes]
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )

r_small = 50# Radio de los círculos del recipiente
r_pozo = 140# Radio del pozo
template = circle(r_small)# Template para la correlación
s = diamond(4)# elemento estructurante
# In[]
#plt.close('all')
#i = 1
#j = 3
for i in range(0,len(folder_ids)):# Para cada carpeta
#    dic = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],'Pozo 5':[],'Pozo 6':[]}
    for j in range(0,len(image_ids[i])):# Para cada imagen
        PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
        I = imread(PATH)
        I_gray = rgb2gray(I)
        I_gray = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))
        BW = canny(I_gray,sigma=0.5)
        #Operación morfológica
        BW = closing(BW,s)
        result = match_template(BW,template,pad_input = True)
        coordinates = peak_local_max(result, min_distance=160)#centro del pequeño 
        centros = corr2d(coordinates,template,r_pozo)
        # *** Seccionamiento y segmentación ***
        m = np.shape(I_gray)
        m_BW = np.zeros([m[0],m[1]])# Imagen negra
        for k in range(0,len(centros)):# Para cada uno de los centros
            I_seg = pozos(I_gray,centros[k],r_pozo)
            I_otsu = otsu(I_seg,I_gray,centros[k],r_pozo)#mascara por pozo
            I_props = intento(I_otsu)#aplicación de las propiedades de region
            
            fig = plt.figure()
            ax1 = fig.add_subplot(111)      
            ax1.axis('off')
            ax1.imshow(I_props,cmap='gray')
    #remoción de bordes
#    I_color = color(I,I_gray,centros[k],r_pozo)

    
#    I_fin = I_props * I_color

#    labeled,num = label(I_fin,neighbors=8, background=0,return_num=True,connectivity=10)#etiquetado y conteo
#    print('Hay ' + str(num) + ' colonias en el pozo ' + str(k) + '.')
#    dic[ list(dic.keys())[k] ].append(num)

#            m_BW = m_BW + I_props
#            I_color = color(I,I_gray,centros,r_pozo)
#            m_BW = m_BW * I_color

#labeled = label(m_BW,neighbors=8, background=0)#etiquetado y conteo
#labeled_RGB = label2rgb(labeled,image = I)#image = imagen original


#        fig = plt.figure()
#        ax1 = fig.add_subplot(111)      
#        ax1.axis('off')
#        ax1.imshow(m_BW,cmap='gray')#,cmap='gray')
        #        for l in range(0,len(centros)):
        #            ax1.plot(centros[l][0],centros[l][1],'ro')
        #        for l in range(0,len(coordinates)):
        #            ax1.plot(coordinates[l][1],coordinates[l][0],'ro')
#        fig.show()
#        fig.savefig('Resultados/' + folder_ids[i] + '/' + image_ids[i][j])
#frame_test = pd.DataFrame(dic,index=image_ids[i])
#frame_test.to_csv('Resultados/' + folder_ids[i] + '.csv')

# In[Funciones]

#def circle(r):
#    '''
#    Función que genera un template circular negro con radio r.
#    r: radio del círculo en píxeles.
#    
#    Retorna: Matriz que describe un círculo con radio r píxeles.
#    
#    '''
#    dim = r*2 + 15#dimensión de la matriz.
#    Nigerrimo = np.zeros([dim,dim])
#    centro = [dim/2,dim/2]
#    for i in range(0,dim):
#        for j in range(0,dim):
#            d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
#            if d > r and d < r+4:
#                Nigerrimo[i,j] = 1
#    return Nigerrimo
#
#def corr2d(coordinates,template,r_pozo):
#    '''
#    Realiza la correlación cruzada normalizada [1] con una imagen template.
#    
#    BW: Imagen con los bordes segmentados.
#    template: Imagen con el template para realizar la correlación.
#    r_pozo: Radio del pozo en píxeles.
#    
#    
#    Retorna centros: Arreglo de coordenadas (x,y) con los centros de los pozos
#    ubicados en el siguiente orden.   
#    '''
#    #podría reeemplazar el if-else:
##    coordinates = np.sort(coordinates, axis=1, kind='quicksort', order=None)
#    if coordinates[0][1] < coordinates[1][1]:
#        y = coordinates[0][0]-r_pozo-5
#        x = coordinates[0][1]+r_pozo+5
#    else:
#        y = coordinates[1][0]-r_pozo-5
#        x = coordinates[1][1]+r_pozo+5
#    #coordenadas de los otros pozos por simetría
#    centros = [[x,y],[x,y+2*r_pozo + 10]]
#    for i in range(0,2):
#        centros.append([centros[i][0] + 2*r_pozo + 10 ,centros[i][1] ])
#        centros.append([centros[i][0] - 2*r_pozo - 10,centros[i][1] ])
#    
#    centros = sorted(centros)
#    centros = np.asarray(centros)#(x,y)
#    
#    return centros
#
#
#def pozos(m_I,centro,r):
#    '''
#    Secciona 1 pozo de forma tal que para todo píxel P(i,j) que se encuentre 
#    a una distancia d menor o igual a r, se conserve su valor original en 
#    escala de grises, de lo contrario, se le asigna un valor de 0 (Blanco).
#    
#    m_I: Imagen de 1 dimensión.
#    centros: Coordenadas de los centros de los pozos (x,y) en un arreglo de np.
#    r: Radio del pozo en píxeles.
#    
#    Retorna I_new: Imagen con los pozos seccionados.
#    '''
#    h,w = m_I.shape
#    I_new = np.zeros([h,w])
#    for i in range(0,h):
#        for j in range(0,w):
#            d = math.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
#            if d <= r:
#                I_new[i,j] = m_I[i,j]
#    return I_new
#
#
#
#def otsu(I_cro,I_gray2,centro,r):
#    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
#    prom = np.mean(I2)
#    thresh = threshold_otsu(I2)*prom
#    BW = I_cro > thresh
#    BW = 1 - BW
#    return BW
#
#
#def intento(Iseg):
#    labeled = label(Iseg,neighbors=8, background=0)
#    i = 1
#    # Tomar imágenes con areas mayores a X
#    for region in regionprops (labeled):
#        area_convexa = region.convex_area # Numero de pixeles dentro de la envolvente convexa
##        solidez = region.solidity #Razon entre pixeles de la region y pixeles de la envolvente
#        eje_mayor = region.major_axis_length
#        eje_menor = region.minor_axis_length 
#        if   eje_menor != 0:            
#            axes_ratio = eje_mayor/eje_menor
#        else:
#            axes_ratio = 0
#            
#        if area_convexa < 7 and axes_ratio < 1 or area_convexa > 80: 
#            Iseg[labeled == i] = 0
#
#        i += 1
#
#    
#    return Iseg

#
#def pozos3(m_I,centro,r):
#    h,w = m_I.shape
#    I_new = np.ones([h,w])#matriz blanca
#    prom = []
#    for i in range(0,h):
#        for j in range(0,w):
#            x = centros[:,0] - j
#            y = centros[:,1] - i
#            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
#            if any ( np.logical_and(d <= r,d >= r - 20) ):
#                I_new[i,j] = m_I[i,j]
#                prom.append([i,j])
#    return I_new,prom
##
#
#
##    h,w = m_I.shape
##    I_new = np.zeros([h,w])
##    prom = []
##    for i in range(0,h):
##        for j in range(0,w):
##            d = math.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
##            if d <= r and d >= r-20:
##                I_new[i,j] = m_I[i,j]
##                prom.append([i,j])
##    return I_new,prom
#
#
##def pozos3(m_I,centro,r):
#
##    h,w = m_I.shape
##    I_new = np.ones([h,w])#matriz blanca
##    prom = []
##    for i in range(0,h):
##        for j in range(0,w):
##            x = centros[:,0] - j
##            y = centros[:,1] - i
##            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
##            if any ( np.logical_and(d <= r,d >= r - 20) ):
##                I_new[i,j] = m_I[i,j]
##                prom.append([i,j])
##    return I_new,prom
#
## In[]
#    
#def color(I,I_gray,centros,r_pozo):
#    I_bordes,prom = pozos3(I_gray,centros,r_pozo)
#    I2 = np.copy(I)
#    I2[:,:,0],prom = pozos3(I[:,:,0],centros,r_pozo)
#    I2[:,:,1],prom = pozos3(I[:,:,1],centros,r_pozo)
#    I2[:,:,2],prom = pozos3(I[:,:,2],centros,r_pozo)
#
#    promcito = np.asarray(prom)#vuelvo arreglo la lista de listas prom
#
#    I_color = rgb2lab(I2,illuminant='D65',observer='2')
#    m = np.shape(I_color[:,:,0])
#    promedio = [ np.mean( I_color[promcito[:,0],promcito[:,1],1] ) , np.mean( I_color[promcito[:,0],promcito[:,1],2] ) ]
#    IRGB = rgb2gray(I)
#
#    umbral = 5
#    for i in range(0,m[0]):
#        for j in range(0,m[1]):
#            pix = I_color[i,j,1::]
#            dist = np.linalg.norm(promedio - pix)
#            if dist < umbral:
#                IRGB[i,j] = 1
#            
#    IRGB = 1 - IRGB
#    IRGB = IRGB > 0.7
#    I_fin = (I_bordes + IRGB) > 0.9
#
#
#    return I_fin

#I_def = color(I,I_gray,centros,r_pozo)
#
#fig = plt.figure()
#ax1 = fig.add_subplot(111)      
#ax1.axis('off')
#ax1.imshow(I_def,cmap='gray')

#I_lol = color(I,I_gray,centros)
