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

from skimage.filters.thresholding import threshold_otsu,threshold_adaptive
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
r_small = 50

PATH = gen + folder_ids[1] + '/' + image_ids[1][4]
I = imread(PATH)
I_gray = rgb2gray(I)


template = circle(r_small)
edges = canny(I_gray,sigma=0.05)
centros = corr2d(edges,template,r_pozo)


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.axis('off')
ax1.imshow(I_gray,cmap='gray')

for i in range(0,len(centros)):
    ax1.plot(centros[i][0],centros[i][1],'ro')

fig.show()

# In[] Mejora de contraste
def seg_contraste(m_I,r,centros):
    '''
    m_I: Imagen en escala de grises.
    r: Radio del pozo.
    centros: Coordenadas de los centros de los pozos en un arreglo de numpy.
    
    Retorna la máscara con las colonias segmentadas.
    '''
    m_I = rescale_intensity(m_I,in_range=(0.25,0.4))
    m_I_crop = pozos2(1-m_I,centros,r)
    return m_I_crop



r_pozo = 145
I_gray2 = rescale_intensity(I_gray,in_range=(0.25,0.4))
I_crop = pozos2(1-I_gray2,centros,r_pozo)


fig, (ax_orig, ax_mask) = plt.subplots(1, 2)
ax_orig.imshow(I_gray2, cmap='gray')
ax_orig.set_title('Original')
ax_orig.set_axis_off()
ax_mask.imshow(I_crop, cmap='gray')
ax_mask.set_title('Máscara')
ax_mask.set_axis_off()
fig.show()   

# In[] Otsu por región.


def otsu_region(m_I,r,centros):
    '''
    Determina un umbral por pozo. Binariza la imagen con el respectivo pozo segmentado.
    Multiplica dicha imagen invertida (pozo negro,colonias blancas y demás blanco)
    por una matriz de 1's (blanca) para así, obtener la segmentación de los 6 pozos.
    Se hace uso de 6 umbrales diferentes, 1 por región.
    
    m_I: Imagen en escala de grises.
    r: radio del pozo en píxeles.
    centros: Coordenadas de los centros (x,y) en un arreglo de numpy.
    
    Retorna la máscara con las colonias segmentadas.
    '''
    m = np.shape(m_I)
    m_I = rescale_intensity(m_I,in_range=(0.1,0.8))
    m_BW = np.ones([m[0],m[1]])#Imagen blanca
    for k in range(0,len(centros)):
        m_I_pozo = pozos(m_I,centros[k],r)
        m_I_otsu = otsu(m_I_pozo,m_I,centros[k],r)
        m_BW = m_BW * m_I_otsu
    
    return m_BW
    
    

r_pozo = 145
m = np.shape(I_gray)
I_gray1 = rescale_intensity(I_gray,in_range=(0.1,0.8))
I_final = np.ones([m[0],m[1]])
for k in range(0,len(centros)):
#k = 0
    I_crop = pozos(I_gray1,centros[k],r_pozo)
    I_otsu = otsu(I_crop,I_gray1,centros[k],r_pozo)
    I_final = I_final * I_otsu
#I_crop = pozos(I_final,centros,r_pozo)

fig, (ax_orig, ax_mask) = plt.subplots(1, 2)
ax_orig.imshow(1-I_gray1, cmap='gray')
ax_orig.set_title('Original')
ax_orig.set_axis_off()
ax_mask.imshow(I_otsu, cmap='gray')
ax_mask.set_title('Máscara')
ax_mask.set_axis_off()
fig.show()  


# In[]

def otsu_and(m_I,r,centros):
    '''
    Determina un umbral por pozo. Binariza toda la imagen en escala de grises.
    Multiplica dicha imagen invertida (pozo negro,colonias blancas y demás blanco)
    por una matriz de 1's (blanca) para así, obtener la segmentación de los 6 pozos.
    Se hace uso de 6 umbrales diferentes, 1 por región.
    
    m_I: Imagen en escala de grises.
    r: radio del pozo en píxeles.
    centros: Coordenadas (x,y) de los centros de los pozos en un arreglo de
    numpy.
    
    Retorna m_I_pozo: Máscara con las colonias segmentadas en blanco.
    '''
    m = np.shape(m_I)
    m_I = rescale_intensity(I_gray,in_range=(0.1,0.8))
    m_BW = np.ones([m[0],m[1]])#Imagen blanca
    for k in range(0,len(centros)):
        m_I_otsu = otsu2(m_I,centros[k],r)
        m_BW = m_BW * m_I_otsu
    m_I_pozo = pozos2(m_BW,centros,r)
    return m_I_pozo


r_pozo = 145
m = np.shape(I_gray)
I_gray1 = rescale_intensity(I_gray,in_range=(0.1,0.8))
I_final = np.ones([m[0],m[1]])
for k in range(0,len(centros)):
    I_otsu = otsu2(I_gray1,centros[k],r_pozo)
    I_final = I_final * I_otsu
I_crop = pozos2(I_final,centros,r_pozo)

fig, (ax_orig, ax_mask) = plt.subplots(1, 2)
ax_orig.imshow(1-I_gray1, cmap='gray')
ax_orig.set_title('Original')
ax_orig.set_axis_off()
ax_mask.imshow(I_crop, cmap='gray')
ax_mask.set_title('Máscara')
ax_mask.set_axis_off()
fig.show() 
# In[]

def otsu(I_cro,I_gray2,centro,r):
    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
    prom = np.mean(I2)
    thresh = threshold_otsu(I2)*prom
    BW = I_cro > thresh
    BW = 1 - BW
    return BW

def otsu2(I_gray2,centro,r):
    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
    prom = np.mean(I2)
    thresh = threshold_otsu(I2)*prom
    BW = I_gray2 > thresh
    BW = 1 - BW
    return BW
# In[]
def adapt(I_gray):  
#    I = I_gray[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]  
    block_size = 13
    BW = threshold_adaptive(I_gray, block_size, offset=0.01)
    return BW



# In[] Correlación cruzada normalizada de skimage

#---OPCIONAL--- xd
#- Desplega la gráfica con la imagen original, el template y la correlación.
#Guarda las imágenes qué dieron como resultado del template empleado en la
# la dirección Resultados_template/nombre_folder/nombre_imagen

def corr2d(BW,template,r_pozo):
    '''
    Realiza la correlación cruzada normalizada [1] con una imagen template.
    
    BW: Imagen con los bordes segmentados.
    template: Imagen con el template para realizar la correlación.
    r_pozo: Radio del pozo en píxeles.
    
    
    Retorna centros: Arreglo de coordenadas (x,y) con los centros de los pozos
    ubicados en el siguiente orden.

    |0 2 4|
    |1 3 5|
    
    
    [1] J. P. Lewis, “Fast Normalized Cross-Correlation”,
    Industrial Light and Magic.    
    '''
    result = match_template(BW,template,pad_input = True)
    coordinates = peak_local_max(result, min_distance=160)#centro del pequeño 
    #podría reeemplazar el if-else:
#    coordinates = np.sort(coordinates, axis=1, kind='quicksort', order=None)
    if coordinates[0][1] < coordinates[1][1]:
        y = coordinates[0][0]-r_pozo
        x = coordinates[0][1]+r_pozo
    else:
        y = coordinates[1][0]-r_pozo
        x = coordinates[1][1]+r_pozo
    #coordenadas de los otros pozos por simetría
    centros = [[x,y],[x,y+2*r_pozo]]
    for i in range(0,2):
        centros.append([centros[i][0] + 2*r_pozo,centros[i][1] ])
        centros.append([centros[i][0] - 2*r_pozo,centros[i][1] ])
    
    centros = sorted(centros)
    centros = np.asarray(centros)#(x,y)
    
#    fig, (ax_orig, ax_template, ax_corr) = plt.subplots(1, 3)
#    fig = plt.figure()
#    ax_orig = fig.add_subplot(111)
##    ax_orig.imshow(I_gray, cmap='gray')
#    ax_orig.imshow(BW, cmap='gray')
#    ax_orig.set_title('Original')
#    ax_orig.set_axis_off()
##    ax_template.imshow(template, cmap='gray')
##    ax_template.set_title('Template')
##    ax_template.set_axis_off()
##    ax_corr.imshow(result, cmap='gray')
##    ax_corr.set_title('Correlación cruzada')
##    ax_corr.set_axis_off()
##    for i in range(0,len(coordinates)):
##        ax_orig.plot(coordinates[i,1], coordinates[i,0], 'ro')
#    for i in range(0,len(centros)):
#        ax_orig.plot(centros[i][0],centros[i][1],'ro')
#    fig.show()   
#    fig.savefig('Resultados_template/' + folder + '/' + name)
#    fig.savefig('Resultados_template/' + t_name + '/' + folder + '/' + name)
    return centros

# In[] Seccionamiento por medio de distancia euclideana


#-Entradas: Imagen en escala de grises I_gray, coordenadas de los centros
#coordinates, las dimensiones más pequeñas dim como una lista de 2, y el radio.
#-Salidas: Imagen con los pozos seccionados I_new y grafica la imagen resultado.
#Las coordenadas deben ser especificadas en la forma (x,y) en un arreglo de np.
#
def pozos2(m_I,centros,r):
    '''
    Secciona los pozos de forma tal que para todo píxel P(i,j) que se encuentre 
    a una distancia d menor o igual a r, donde d se evalua para todos los 
    centros de los pozos, se conserve su valor original en escala de grises.
    De lo contrario, se le asigna un valor de 0 (Blanco).
    
    m_I: Imagen de 1 dimensión.
    centros: Coordenadas de los centros de los pozos (x,y) en un arreglo de np.
    r: Radio del pozo en píxeles.
    
    Retorna I_new: Imagen con los pozos seccionados.
    
    '''
    h,w = m_I.shape
    I_new = np.ones([h,w])
    for i in range(0,h):
        for j in range(0,w):
            x = centros[:,0] - j
            y = centros[:,1] - i
            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
            if any(d <= r):
                I_new[i,j] = m_I[i,j]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.axis('off')
    ax1.imshow(I_new,cmap='gray')
    return I_new



def pozos(m_I,centro,r):
    '''
    
    Secciona 1 pozo de forma tal que para todo píxel P(i,j) que se encuentre 
    a una distancia d menor o igual a r, se conserve su valor original en 
    escala de grises, de lo contrario, se le asigna un valor de 0 (Blanco).
    
    m_I: Imagen de 1 dimensión.
    centros: Coordenadas de los centros de los pozos (x,y) en un arreglo de np.
    r: Radio del pozo en píxeles.
    
    Retorna I_new: Imagen con los pozos seccionados.
    
    '''
    h,w = m_I.shape
    I_new = np.zeros([h,w])
    for i in range(0,h):
        for j in range(0,w):
            d = np.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
            if d <= r:
                I_new[i,j] = m_I[i,j]

#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    ax1.axis('off')
#    ax1.imshow(I_new,cmap='gray')
    return I_new

# In[] 

def circle(r):
    '''
    Función que genera un template circular negro con radio r.
    r: radio del círculo en píxeles.
    
    Retorna: Matriz que describe un círculo con radio r píxeles.
    
    '''
    dim = r*2 + 10#dimensión de la matriz.
    Nigerrimo = np.zeros([dim,dim])
    centro = [dim/2,dim/2]
    for i in range(0,dim):
        for j in range(0,dim):
            d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
            if d > r:
                Nigerrimo[i,j] = 1
    return Nigerrimo


