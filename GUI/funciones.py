# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 18:00:07 2018

@author: Nicolás, Liz, Mafius
"""

import math
import numpy as np
from skimage.color import rgb2lab
from skimage.color import rgb2gray
from skimage.filters.thresholding import threshold_otsu
from skimage.measure import label
from skimage.measure import regionprops


def circle(r):
    '''
    Genera un template circular negro con radio r.
    Args:
        r: int con el radio del círculo en píxeles.
    Retorna: 
        Matriz que describe un círculo con radio r píxeles.
    '''
    dim = r*2 + 15#dimensión de la matriz.
    Nigerrimo = np.zeros([dim,dim])
    centro = [dim/2,dim/2]
    for i in range(0,dim):
        for j in range(0,dim):
            d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
            if d > r and d < r+4:
                Nigerrimo[i,j] = 1
    return Nigerrimo

def corr2d(coordinates,template,r_pozo):
    '''
    Realiza la correlación cruzada normalizada [1] con una imagen template y
    retorna los centros de obtenidos de la correlación.
    
    Args:
        coordinates: Coordenadas de los centros de los circulos del
        recipiente.
        template: Imagen con el template para realizar la correlación.
        r_pozo: Radio del pozo en píxeles.
    
    Retorna: 
        centros: Arreglo de coordenadas (x,y) con los centros de los pozos
        ubicados en el siguiente orden .   
    '''
    #podría reeemplazar el if-else:
#    coordinates = np.sort(coordinates, axis=1, kind='quicksort', order=None)
    if coordinates[0][1] < coordinates[1][1]:
        y = coordinates[0][0]-r_pozo-5
        x = coordinates[0][1]+r_pozo+5
    else:
        y = coordinates[1][0]-r_pozo-5
        x = coordinates[1][1]+r_pozo+5
    #coordenadas de los otros pozos por simetría
    centros = [[x,y],[x,y+2*r_pozo + 10]]
    for i in range(0,2):
        centros.append([centros[i][0] + 2*r_pozo + 10 ,centros[i][1] ])
        centros.append([centros[i][0] - 2*r_pozo - 10,centros[i][1] ])    
    centros = sorted(centros)
    centros = np.asarray(centros)#(x,y)    
    return centros

def pozo(m_I,centro,r):
    '''
    Secciona 1 pozo de forma tal que para todo píxel P(i,j) que se encuentre 
    a una distancia d menor o igual a r, se conserve su valor original en 
    escala de grises, de lo contrario, se le asigna un valor de 0 (Blanco).
    
    Args: 
        m_I: Imagen de 1 dimensión.
        centros: Coordenadas de los centros de los pozos (x,y) en 
        un arreglo de np.
        r: Radio del pozo en píxeles.

    Retorna I_new: Imagen con el pozo seccionado.
    '''
    h,w = m_I.shape
    I_new = np.zeros([h,w])
    for i in range(0,h):
        for j in range(0,w):
            d = math.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
            if d <= r:
                I_new[i,j] = m_I[i,j]
    return I_new

def otsu(I_cro,I_gray2,centro,r):
    """
    Binariza una imagen acorde a un umbral determinado por Otsu y escalado
    por un factor igual al promedio de la imagen.
    
    Args:
        I_cro: Imagen donde uno de los pozos está seccionado por distancia
        euclidiana.
        I_gray: Imagen en escala de grises.
        centro: Coordenadas del centro del pozo de la forma (y,x)
        r: Radio del pozo en pixeles.
    
    Retorna:
        BW: Imagen binarizada de un pozo mediante el método de Otsu. 
    """
    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
    prom = np.mean(I2)
    thresh = threshold_otsu(I2)*prom
    BW = I_cro > thresh
    BW = 1 - BW
    return BW

def reg_seg(Iseg):
    """
    Elimina aquellas regiones que no cumplen con ciertas propiedades de región
    
    Args:
        Iseg: Imagen segmentada por medio del método de Otsu escalado y a la
        cual se le ha aplicado la máscara de los bordes por color.
            
    Retorna:
        Iseg: Imagen con las colonias que cumplian con condiciones de
        propiedades geométricas de area convexa y excentricidad.
    """
    labeled = label(Iseg,neighbors=8, background=0)
    i = 1
    # Tomar imágenes con areas mayores a X
    for region in regionprops (labeled):
        # Numero de pixeles dentro de la envolvente convexa
        area_convexa = region.convex_area 
        #Razon entre pixeles de la region y pixeles de la envolvente
#        solidez = region.solidity 
        eje_mayor = region.major_axis_length
        eje_menor = region.minor_axis_length 
        if   eje_menor != 0:            
            axes_ratio = eje_mayor/eje_menor
        else:
            axes_ratio = 0
            
        if area_convexa < 7 and axes_ratio < 1 or area_convexa > 80: 
            Iseg[labeled == i] = 0

        i += 1
    return Iseg

def pozo_anillo(m_I,centro,r):
    """
    Secciona todos un anillo correspondiente a los bordes de los pozos de 
    forma tal que para todo píxel P(i,j) que se encuentre a una distancia d 
    menor o igual a r, se conserve su valor original en escala de grises, de 
    lo contrario, se le asigna un valor de 0 (Blanco) dados los centros de 
    la forma (x,y).
    
    Args: 
        m_I: Imagen de bi-dimensional.
        centro: Coordenadas de los centros de los pozos (x,y) en 
        un arreglo de numpy.
        r: Radio del pozo en píxeles.
    
    Retorna:
        I_new: Imagen con un anillo de los bordes seccionado.
        prom: Coordenadas de los pixeles del borde del pozo dentro de la img.
    """
    h,w = m_I.shape
    I_new = np.ones([h,w])
    prom = []
    for i in range(0,h):
        for j in range(0,w):
            d = math.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
            if d <= r and d >= r-20:
                I_new[i,j] = m_I[i,j]
                prom.append([i,j])
    return I_new,prom

def color(I,I_gray,centro,r_pozo):
    """
    Obtención de la máscara de los bordes por distancia euclidiana en el
    espacio de color CIE L*a*b
    
    Args:
        I: Imagen en esquema de codificación RGB.
        I_gray: Imagen en esquema de codificación de escala de grises.
        centro: Coordenadas del centro de un pozo.
        r_pozo: Radio del pozo en pixeles.
        
    Retorna:
        I_fin: Máscara de binaria de las colonias en los bordes.
    """
    I_bordes,prom = pozo_anillo(I_gray,centro,r_pozo)
    I2 = np.copy(I)
    #por plano se toman los anillos
    I2[:,:,0],prom = pozo_anillo(I[:,:,0],centro,r_pozo)
    I2[:,:,1],prom = pozo_anillo(I[:,:,1],centro,r_pozo)
    I2[:,:,2],prom = pozo_anillo(I[:,:,2],centro,r_pozo)
    promcito = np.asarray(prom)#vuelvo arreglo la lista de listas prom
    I_color = rgb2lab(I2,illuminant='D65',observer='2')
    m = np.shape(I_color[:,:,0])
    promedio = [
        np.mean( I_color[promcito[:,0],promcito[:,1],1] ), 
        np.mean( I_color[promcito[:,0],promcito[:,1],2] ) 
    ]
    IRGB = rgb2gray(I)
#IRGB = pozos2(IRGB,centros,r_pozo) 
#for umbral in umbral:
    umbral = 5
    for i in range(0,m[0]):
        for j in range(0,m[1]):
            pix = I_color[i,j,1::]
            dist = np.linalg.norm(promedio - pix)
            if dist < umbral:
                IRGB[i,j] = 1
            
    IRGB = 1 - IRGB
    IRGB = IRGB > 0.7    
    I_fin = (I_bordes + IRGB) > 0.9
    return I_fin