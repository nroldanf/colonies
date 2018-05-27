# -*- coding: utf-8 -*-
"""
Created on Fri May 25 19:34:53 2018

@author: Nicolas
"""

# In[]
import matplotlib.pyplot as plt
import numpy as np
import os

import scipy

from scipy.signal import correlate2d
from scipy import ndimage as ndi
from skimage.io import imread
from skimage.filters.thresholding import threshold_otsu
from skimage.color import rgb2gray,rgb2lab
from skimage.measure import label
from skimage.feature import canny
from skimage.exposure import rescale_intensity
from skimage.morphology import remove_small_objects
#from skimage.transform import resize
#from skimage.morphology import erosion, dilation, opening, closing, white_tophat
#from skimage.morphology import disk

from skimage.feature import peak_local_max
from skimage.feature import match_template


#Carpetas con diferentes imágenes
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )



##---Obtención de la dimensión más pequeña
#heights = []
#widths=[]
#
#for i in range(0,len(folder_ids)):
#    for j in range(0,len(image_ids[i][:])):
#        PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
#        I = imread(PATH)
#        h,w,d = I.shape
#        heights.append(h)
#        widths.append(w)
#
##min_h = min(heights)
##min_w = min(widths)
#
#dim = [min(heights),min(widths)]

# In[]

t_name = 'template1'
r = 130

for i in range(0,len(folder_ids)):
    for j in range(0,len(image_ids[i][:])):
        PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
        I = imread(PATH)
        I_gray = rgb2gray(I)
        coord = corr2d(I_gray,t_name,folder_ids[i],image_ids[i][j],j)
        I_final = pozos(I_gray,coord,r)
        I_final = processing(I_gray,I_final)
        scipy.misc.imsave('Resultados/Metodo_uno/' + image_ids[i][j] +  '_re' + '.png' ,I_final)
    
# In[] Funciones

#----------Procesado de las imágenes-------------
def processing(I_gray,I_gray2):
    #Mejora de contraste en escala de grises
    I_gray = contrast_basic(I_gray,6)
    #Método de segmentación en escala de grises
    BW = otsu(I_gray,I_gray2)
    #Análisis de conectividad y etiquetado
#    mask = conectividad(BW,1)
    return BW
            

#---------------Correlación cruzada--------------
#--Entrada: Imagen en escala de grises I_gray y template para hacer la
#   correlación cruzada.
#-Salida: Coordenadas de los centros de la correlación cruzada.
#- Desplega la gráfica con la imagen original, el template y la correlación.
def corr2d(I_gray,t_name,folder,name,ind):
    template = imread(t_name + '.png')
    template_g = rgb2gray(template)
#    template_g = template_g -  np.mean(template_g)
    result = match_template(I_gray,template_g,pad_input = True)
    coordinates = peak_local_max(result, min_distance=125)
#    fig, (ax_orig, ax_template, ax_corr) = plt.subplots(1, 3)
#    ax_orig.imshow(I_gray, cmap='gray')
#    ax_orig.set_title('Original')
#    ax_orig.set_axis_off()
#    ax_template.imshow(template_g, cmap='gray')
#    ax_template.set_title('Template')
#    ax_template.set_axis_off()
#    ax_corr.imshow(result, cmap='gray')
#    ax_corr.set_title('Correlación cruzada')
#    ax_corr.set_axis_off()
#    for i in range(0,len(coordinates)):
#        ax_orig.plot(coordinates[i,1], coordinates[i,0], 'ro')
#    fig.show()
#    fig.savefig('Resultados_template/' + t_name + '/' + folder + '/' + name)
    return coordinates
#---------------Seccionamiento por pozo-------------------
#-Entradas: Imagen en escala de grises I_gray, coordenadas de los centros
#coordinates, las dimensiones más pequeñas dim como una lista de 2, y el radio.
#-Salidas: Imagen con los pozos seccionados I_new y grafica la imagen resultado.
def pozos(I_gray,coordinates,r):
    h,w = I_gray.shape
    I_new = np.zeros([h,w])
    r = 130
    for i in range(0,h):
        for j in range(0,w):
            x = coord[:,0] - i
            y = coord[:,1] - j
            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
            if any(d <= r):
                I_new[i,j] = I_gray[i,j]
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    ax1.axis('off')
#    ax1.imshow(I_new,cmap='gray')
    return I_new



#-----------Mejora de contraste------------------ CORREGIR
#- Entrada: Imagen en esquema RGB m_I y selector sel.
#- Salida: Imagen con la mejora de contraste elegida.
def contrast_basic(m_I,sel):
    if sel == 1:
        I_out = (m_I/255)**3
    elif sel == 2:
        I_out = (m_I/255)**2
    elif sel == 3:
        I_out = np.sqrt((m_I/255))
    elif sel == 4:
        I_out = np.exp(-(m_I/255))
    elif sel == 5:
        I_out = (m_I/255)*0.3 + 0.2
    elif sel == 6:
        I_out = rescale_intensity(m_I,in_range=(0.2,0.8))
    return I_out

#-------------Segmentación por Otsu--------
#- Entrada: Imagen en esquema escala de grises m_I
#- Salida: Mascara en blanco y negro.
def otsu(I_gray,I_gray2):
    prom = np.mean(I_gray)
    thresh = threshold_otsu(I_gray)*prom
    BW = I_gray2 > thresh
    return BW
#----------Segmentación con máscara Sobel -------------

def puntos(I_gray):
    Maxpix = max(np.ravel(I_gray))
    H = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
    I_sharpened = correlate2d(I_gray, H, mode = 'same')
    I_sharpened = I_sharpened > 0.9*Maxpix
    return I_sharpened

#--------Segmentación por color -------------
    

def cie(I):
    I_cie = rgb2lab(I,illuminant='D65',observer='2')  
    x = plt.ginput(1)
    color = I_cie[int(round(x[0][0])),int(round(x[0][1])),1::]
    m = np.shape(I_cie[:,:,0])
    umbral = 24
    IR = rgb2gray(I)
    IG = rgb2gray(I)
    IB = rgb2gray(I)
    IRGB = I
    for i in range(0,m[0]):
        for j in range(0,m[1]):
            pix = I_cie[i,j,1::]
            dist = np.linalg.norm(color-pix)
            if dist < umbral:
                IR[i,j] = I[i,j,0]
                IG[i,j] = I[i,j,1]
                IB[i,j] = I[i,j,2]
                
    IRGB[:,:,0] = IR   
    IRGB[:,:,1] = IG 
    IRGB[:,:,2] = IB
    return IRGB

#--------Segmentación por bordes--------------

def bordes(I_gray):
    I_edges = canny(I_gray)
    fill_I = ndi.binary_fill_holes(I_edges)
    label_objects, nb_labels = ndi.label(fill_I)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20
    mask_sizes[0] = 0
    I_clean = mask_sizes[label_objects]
    return I_clean


#------------Análisis por conectividad -------

def conectividad(m_BW,sel):
    cont = 0
    if sel == 1:
        labeled = label(m_BW,connectivity=2)
        BW2  = remove_small_objects(labeled,min_size=25,connectivity=8)
    elif sel == 2:
        labeled = label(m_BW,connectivity=2)
        BW2  = remove_small_objects(labeled,min_size=20,connectivity=8)
        labeled = label(BW2,connectivity=2)
        cont = max(labeled.ravel())
    else:
        pass
    return labeled,cont
