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
from skimage.feature import peak_local_max,canny
from skimage.feature import match_template

from skimage.filters.thresholding import threshold_otsu
from skimage.exposure import rescale_intensity


# In[]
#plt.close('all')
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()


#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
    
    
#for i in [3,5]:
##i = 1#número del folder
#    for j in range(0,len(image_ids[i][:])):
#        PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
#        #    offset = 150
#        I = imread(PATH)
#        I_gray = rgb2gray(I)
#        coord = corr2d(I_gray,t_name,folder_ids[i],image_ids[i][j],j)

#template = imread(t_name + '.png')
#template_g = rgb2gray(template)
#
    
    
r_pozo = 150

PATH = gen + folder_ids[0] + '/' + image_ids[0][7]
I = imread(PATH)
I_gray = rgb2gray(I)


template = circle(r_small)
edges = canny(I_gray,sigma=0.05)
result = match_template(edges,template,pad_input = True)
coordinates = peak_local_max(result, min_distance=160)#centro del pequeño 


y = coordinates[0][0]-r_pozo
x = coordinates[0][1]+r_pozo
#coordenadas de los otros pozos por simetría
centros = [[x,y],[x,y+2*r_pozo]]
for i in range(0,2):
    centros.append([centros[i][0] + 2*r_pozo,centros[i][1] ])
    centros.append([centros[i][0] - 2*r_pozo,centros[i][1] ])



fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.axis('off')
ax1.imshow(I_gray,cmap='gray')

for i in range(0,len(coordinates)):
    ax1.plot(coordinates[i,1], coordinates[i,0], 'ro')    
for i in range(0,len(centros)):
    ax1.plot(centros[i][0],centros[i][1],'ro')

fig.show()

# In[] Correlación cruzada normalizada de skimage


#--Entrada: Imagen en escala de grises I_gray y template para hacer la
#   correlación cruzada.
#-Salida: Coordenadas de los centros de la correlación cruzada.
#- Desplega la gráfica con la imagen original, el template y la correlación.
#Guarda las imágenes qué dieron como resultado del template empleado en la
# la dirección Resultados_template/nombre_folder/nombre_imagen
    
def corr2d(BW,template,folder,name,ind):
#    template = imread(t_name + '.png')
#    template_g = rgb2gray(template)
#    template_g = template_g -  np.mean(template_g)
    result = match_template(BW,template,pad_input = True)
    coordinates = peak_local_max(result, min_distance=160)
    
    y = coordinates[0][0]-r_pozo
    x = coordinates[0][1]+r_pozo
    #coordenadas de los otros pozos por simetría
    centros = [[x,y],[x,y+2*r_pozo]]
    for i in range(0,2):
        centros.append([centros[i][0] + 2*r_pozo,centros[i][1] ])
        centros.append([centros[i][0] - 2*r_pozo,centros[i][1] ])

    
    
    fig, (ax_orig, ax_template, ax_corr) = plt.subplots(1, 3)
    ax_orig.imshow(BW, cmap='gray')
    ax_orig.set_title('Original')
    ax_orig.set_axis_off()
    ax_template.imshow(template, cmap='gray')
    ax_template.set_title('Template')
    ax_template.set_axis_off()
    ax_corr.imshow(result, cmap='gray')
    ax_corr.set_title('Correlación cruzada')
    ax_corr.set_axis_off()
    for i in range(0,len(coordinates)):
        ax_orig.plot(coordinates[i,1], coordinates[i,0], 'ro')
    for i in range(0,len(centros)):
        ax_orig.plot(centros[i][0],centros[i][1],'ro')
    
    fig.show()
#    fig.savefig('Resultados_template/' + t_name + '/' + folder + '/' + name)
    return coordinates

coord = corr2d(edges,template,folder_ids[0],image_ids[0][7],7)

# In[] Seccionamiento por medio de distancia euclideana


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


#h,w = I_gray.shape
#I_new = np.zeros([h,w])
#r = 130
#for i in range(0,h):
#    for j in range(0,w):
#        x = coord[:,0] - i
#        y = coord[:,1] - j
#        d  = np.sqrt(abs( np.square(x) + np.square(y) ))
#        if any(d <= r):
#            I_new[i,j] = I_gray[i,j]
            
            
#list comprehension

#>>> [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]


#d  = np.sqrt(abs(centro-dim))
#I_gray = resize(I_gray,dim)
I_new = pozos(I_gray,coord,r)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.axis('off')
ax1.imshow(I_new,cmap='gray')


# In[]

r = 50
def circle(r):
    dim = r*2 + 10
    Nigerrimo = np.zeros([dim,dim])
    centro = [dim/2,dim/2]
    for i in range(0,dim):
        for j in range(0,dim):
            d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
            if d > r:
                Nigerrimo[i,j] = 1
    return Nigerrimo

c = circle(r)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
ax.imshow(I_gray,cmap='gray')

