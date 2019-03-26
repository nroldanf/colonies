# -*- coding: utf-8 -*-
"""
Created on Wed May 23 10:54:20 2018

@author: Nicolas
"""
import matplotlib.pyplot as plt
import os
import numpy as np
import scipy

from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize

#--AGREGAR AL CÓDIGO ORIGINAL--
from skimage.feature import peak_local_max
from skimage.feature import match_template

#from skimage.transform import resize
from skimage.filters.thresholding import threshold_otsu
from skimage.exposure import rescale_intensity



# In[]
plt.close('all')
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()

t_name = 'template1'#Nombre del template a usar
r = 130#radio escogido del pozo

#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
    
    
#for i in range(0,len(folder_ids)):
i = 1#número del folder
for j in range(0,len(image_ids[i][:])):
    PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
#    offset = 150
    I = imread(PATH)
    I_gray = rgb2gray(I)
    coord = corr2d(I_gray,t_name,folder_ids[i],image_ids[i][j],j)



#PATH = gen + folder_ids[0] + '/' + image_ids[0][7]
#I = imread(PATH)
#I_gray = rgb2gray(I)
#print(np.mean(I_gray[:]))
#I_gray = I_gray - np.mean(I_gray)

# In[] Correlación cruzada normalizada de skimage
#template = imread('template_re2.png')
#template_g = rgb2gray(template)
#template_g = template_g -  np.mean(template_g)
#
#result = match_template(I_gray,template_g,pad_input = True)
###máximos locales de la correlación cruzada para encontrar otras coincidencias
#coordinates = peak_local_max(result, min_distance=125)
##
#fig, (ax_orig, ax_template, ax_corr) = plt.subplots(1, 3)
#ax_orig.imshow(I_gray, cmap='gray')
#ax_orig.set_title('Original')
#ax_orig.set_axis_off()
#ax_template.imshow(template_g, cmap='gray')
#ax_template.set_title('Template')
#ax_template.set_axis_off()
#ax_corr.imshow(result, cmap='gray')
#ax_corr.set_title('Correlación cruzada')
#ax_corr.set_axis_off()
#for i in range(0,len(coordinates)):
#    ax_orig.plot(coordinates[i,1], coordinates[i,0], 'ro')
#fig.show()


#--Entrada: Imagen en escala de grises I_gray y template para hacer la
#   correlación cruzada.
#-Salida: Coordenadas de los centros de la correlación cruzada.
#- Desplega la gráfica con la imagen original, el template y la correlación.
#Guarda las imágenes qué dieron como resultado del template empleado en la
# la dirección Resultados_template/nombre_folder/nombre_imagen
    
def corr2d(I_gray,t_name,folder,name,ind):
    template = imread(t_name + '.png')
    template_g = rgb2gray(template)
#    template_g = template_g -  np.mean(template_g)
    result = match_template(I_gray,template_g,pad_input = True)
    coordinates = peak_local_max(result, min_distance=125)
    fig, (ax_orig, ax_template, ax_corr) = plt.subplots(1, 3)
    ax_orig.imshow(I_gray, cmap='gray')
    ax_orig.set_title('Original')
    ax_orig.set_axis_off()
    ax_template.imshow(template_g, cmap='gray')
    ax_template.set_title('Template')
    ax_template.set_axis_off()
    ax_corr.imshow(result, cmap='gray')
    ax_corr.set_title('Correlación cruzada')
    ax_corr.set_axis_off()
    for i in range(0,len(coordinates)):
        ax_orig.plot(coordinates[i,1], coordinates[i,0], 'ro')
    fig.show()
    fig.savefig('Resultados_template/' + t_name + '/' + folder + '/' + name)
    return coordinates

    
# In[] Seccionamiento por medio de distancia euclideana
#I_gray = rgb2gray(I)
#I_new = np.zeros([636,944])
#proms = list()
#r = 130
#for k in range(0,6):
#    centro = coordinates[k][:]
#    for i in range(0,635):
#        for j in range(0,943):
#            d = np.sqrt( abs( (centro[0] - i)**2 + (centro[1] - j)**2 ) ) 
#            if d <= r:
#                I_new[i,j] = I_gray[i,j]
#            
#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.axis('off')
#ax1.imshow(I_new,cmap='gray')

#-Entradas: Imagen en escala de grises I_gray, coordenadas de los centros
#coordinates, las dimensiones más pequeñas dim como una lista de 2, y el radio.
#-Salidas: Imagen con los pozos seccionados I_new y grafica la imagen resultado.

def pozos(I_gray,coordinates,r):
    h,w = I_gray.shape
    I_new = np.zeros([h,w])
    for k in range(0,len(coordinates)):
        centro = coordinates[k][:]
        for i in range(0,h):
            for j in range(0,w):
                d = np.sqrt( abs( (centro[0] - i)**2 + (centro[1] - j)**2 ) ) 
                if d <= r:
                    I_new[i,j] = I_gray[i,j]
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    ax1.axis('off')
#    ax1.imshow(I_new,cmap='gray')
    return I_new

#I_gray = resize(I_gray,dim)
#I_new = pozos(I_gray,coord,r)


# In[] Promedio de ensambles
#Mínima dimensión de las imágenes (CORREGIR)
min_h = 606
min_w = 914

I_ensamble = np.zeros([606,914])
#for i in range(0,len(folder_ids)):
for j in range(0,len(image_ids[1][:])):
    PATH = gen + folder_ids[1] + '/' + image_ids[1][j]
    I = imread(PATH)
    I_gray = rgb2gray(I)
    I_gray = resize(I_gray,(min_h,min_w))        
    I_ensamble = I_ensamble + I_gray
    
I_ensamble = I_ensamble/28

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.axis('off')
ax1.imshow(I_ensamble,cmap='gray')

print(np.mean(I_ensamble[:]))

scipy.misc.imsave('Resultados/Promedio1.png' ,I_ensamble)
