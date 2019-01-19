# -*- coding: utf-8 -*-
"""
Created on Wed May 23 10:54:20 2018

@author: Nicolas, Liz, Mafe
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import numpy as np
import pandas as pd
#import scipy
from skimage.io import imread
from skimage.color import rgb2gray,rgb2lab
from scipy.ndimage import gaussian_filter
from skimage.feature import match_template,peak_local_max,canny
from skimage.filters.thresholding import threshold_otsu,threshold_yen,threshold_isodata,threshold_li
from skimage.filters.thresholding import threshold_mean,threshold_triangle,threshold_niblack,threshold_sauvola
from skimage.exposure import rescale_intensity
from skimage.measure import label,regionprops
from skimage.morphology import dilation, closing
from skimage.morphology import remove_small_objects,binary_dilation,disk
from skimage.color import label2rgb
#PCA e ICA
from numpy import linalg as LA
from pandas import Series,DataFrame
# In[]
#plt.close('all')
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )

r_small = 50
r_pozo = 140
template = circle(r_small)
# In[]
#-------------------------------------# 
#plt.close('all')
#for i in range(1,len(folder_ids)):
i = 1
j = 10
#    dic = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],'Pozo 5':[],'Pozo 6':[]}
#    for j in range(0,len(image_ids[i])):
#        plt.close('all')
PATH = gen + folder_ids[i] + '/' + image_ids[i][j]
I = imread(PATH)
I_gray = rgb2gray(I)
edges = canny(I_gray,sigma=0.05)
s = disk(6)
edges = closing(edges,s)
centros = corr2d(edges,template,r_pozo)

#fig, (ax_or,ax_fin) = plt.subplots(2,1)
#ax_or.imshow(I,cmap = 'gray')
#ax_or.set_title('Original')
#ax_or.axis('off')
#ax_fin.imshow(edges,cmap='gray')
#ax_fin.set_title('Procesada')
#for i in range(0,len(centros)):
#    ax_or.plot(centros[i,0], centros[i,1], 'ro')
#
#ax_fin.axis('off')

I_final,dic,labeled_RGB = metodo_uno(I,I_gray,140,centros,dic)
#    I_labeled,num = label(I_final,neighbors=8, background=0,return_num=True,connectivity=2)#, connectivity=2)

fig, (ax_or,ax_fin) = plt.subplots(2,1)
ax_or.imshow(labeled_RGB,cmap = 'gray')
ax_or.set_title('Original')
ax_or.axis('off')
ax_fin.imshow(I_final,cmap='gray')
ax_fin.set_title('Procesada')
ax_fin.axis('off')

for l in range(0,len(centros)):
    ax_or.plot(centros[l][0],centros[l][1],'ro')
fig.show()
#        fig.savefig('Resultados/' + 'Metodo_uno/' + folder_ids[i] + '/' + image_ids[i][j])
#print(i)
#    frame_test = pd.DataFrame(dic,index=image_ids[i])
#    frame_test.to_csv('Resultados/' + folder_ids[i] + '.csv')


# In[]
def metodo_uno(I,m_I,r,centros,d):
    m = np.shape(m_I)
    m_I = rescale_intensity(m_I,in_range=(0.2,0.8),out_range=(0,1))
    

    m_BW = np.zeros([m[0],m[1]])#Imagen blanca
    for k in range(0,len(centros)):
        m_I_pozo = pozos(m_I,centros[k],r)
        m_I_otsu = otsu(m_I_pozo,m_I,centros[k],r)#mascara por pozo
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.axis('off')
        ax1.imshow(m_I_otsu,cmap='gray')
        
#        #etiquetado, regionprops y conteo
#        labeled,num = label(m_I_otsu,neighbors=8, background=0,return_num=True)
        I_seg = intento(m_I_otsu)#aplicación de las propiedades de region
        labeled,num = label(I_seg,neighbors=8, background=0,return_num=True)#etiquetado y conteo
        
#        fig = plt.figure()
#        ax1 = fig.add_subplot(111)
#        ax1.axis('off')
#        ax1.imshow(I_seg,cmap='gray')
#        
        print('Hay ' + str(num) + ' colonias en el pozo ' + str(k) + '.')
        
        d[ list(d.keys())[k] ].append(num)
##        colonias += num
        m_BW = m_BW + I_seg
#    print('Hay ' + str(colonias) + ' colonias en total.')
        
    labeled = label(m_BW,neighbors=8, background=0)#etiquetado y conteo
    labeled_RGB = label2rgb(labeled,image = I)#image = imagen original
    
    return m_BW,d,labeled_RGB




def metodo_dos(m_I,m_I_gray,r,centros,d):
    m = np.shape(m_I_gray)
    I_seg = rescale_intensity(m_I_gray,in_range=(0.25,0.4),out_range=(0,1))
    I_seg = 1 - I_seg
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.axis('off')
    ax1.imshow(I_seg,cmap='gray')
    
    m_BW = np.zeros([m[0],m[1]])
    #conto por pozo
    for k in range(0,len(centros)):
        m_I_pozo = pozos(I_seg,centros[k],r)#1 pozo con colonias segmentadas
        I_seg2 = intento(m_I_pozo)#aplicación de propiedades de region
        labeled,num = label(I_seg2,neighbors=8, background=0,return_num=True)#etiquetado y conteo
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.axis('off')
        ax1.imshow(m_I_pozo,cmap='gray')
       
        print('Hay ' + str(num) + ' colonias en el pozo ' + str(k) + '.')
        
        d[ list(d.keys())[k] ].append(num)
##        colonias += num
        m_BW = m_BW + I_seg2
        
    labeled = label(m_BW,neighbors=8, background=0)#etiquetado y conteo
    labeled_RGB = label2rgb(labeled,image = m_I)#image = imagen original
    return m_BW,d,labeled_RGB
    

def metodo_tres(m_I,m_I_gray,r,centros,d):
    m = np.shape(m_I_gray)
    m_BW = np.zeros([m[0],m[1]])
    



# In[] Region props
#props = regionprops(I_labeled,intensity_image=I_final, cache=True)
#p = ["eccentricity","major_axis_length","minor_axis_length","solidity","euler_number","coords"]#lista de propiedades
#p2 = list()
#for i in p:
#    l = list()
#    for j in range(0,num):
#        l.append(props[j][i])
#    p2.append(l)
#

#for k in range(0,num):
#    print(str( p2[k]["solidity"] ))
#para solidez < 0.5 -> blanco
#for in range()


#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.axis('off')
#ax1.imshow(I_final,cmap='gray')

#for i in range(0,len(centros)):
#    ax1.plot(centros[i][0],centros[i][1],'ro')
#fig.show()

# In[]
def intento(Iseg):
#    Iseg2 = np.copy(Iseg)
    labeled = label(Iseg,neighbors=8, background=0)
#    labeled = label(Iseg)#image_1 = imagen sin artefactos 
    # Remueve los objetos que tengan menos de 7 pixeles
#    Iseg2  = remove_small_objects(labeled,min_size=7,connectivity=8)
#    labeled = label(Iseg2,connectivity = 2)
#    labeled_RGB = label2rgb(labeled,image = I_rgb)#image = imagen original
    i = 1
#    I_axes = np.copy(labeled)
    # Tomar imágenes con areas mayores a X
    for region in regionprops (labeled):
#        minr,minc,maxr,maxc = region.bbox #bounding box
#        caja = mpatches.Rectangle((minc,minr),maxc-minc,maxr-minr,fill=False,edgecolor='red',linewidth=2)
        # Graficar cajas        
#        area_caja = region.bbox_area #Numero de pixeles de la caja
#        H,J = region.convex_image #Envolvente binarizada (mismo tamaño que bbox)
        area_convexa = region.convex_area # Numero de pixeles dentro de la envolvente convexa
        solidez = region.solidity #Razon entre pixeles de la region y pixeles de la envolvente
        eje_mayor = region.major_axis_length
        eje_menor = region.minor_axis_length 
        if   eje_menor != 0:            
            axes_ratio = eje_mayor/eje_menor
        else:
            axes_ratio = 0
            
        if area_convexa < 7 and axes_ratio < 1 or area_convexa > 80: 
            Iseg[labeled == i] = 0
#            axes_ratio < 1 
#        if area_convexa < 7:
#            I_axes[labeled == i] = 0 
#        if solidez < 0.54:
#            I_axes[labeled == i] = 0
        i += 1
    
#    fig,(ax1,ax2) = plt.subplots(1,2)
#    ax1.imshow(Iseg2,cmap='gray')
#    ax1.axis('off')
#    ax2.imshow(Iseg,cmap='gray')
#    ax2.axis('off')
#    plt.show()
    
#    print('conteo inicial:', num)  
#    num = max(I_axes.ravel())
#    I_axesRGB = label2rgb(I_axes,image = I_gray)

    
#    fig,ax = plt.subplots(1)b
#    ax.imshow(labeled_RGB,cmap='gray')
#    ax.add_patch(caja)
#    ax.set_axis_off()
#    plt.tight_layout()
#    plt.title('Etiquetado de la imagen original')
#    plt.show()
    
    return Iseg

#lol,num = intento(I,BW)
#
#
#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.axis('off')
#ax1.imshow(lol,cmap='gray')
#
#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.axis('off')
#ax1.imshow(BW,cmap='gray')
#
#print(num)

##I_final = otsu_region()
##I_axes,I_areaConv,I_solid = intent(I,I_crop)
## Marcación 
#I_axesRGB = label2rgb(I_axes,image = I_gray)
#I_areaConvRGB = label2rgb(I_axes,image = I_gray)
#I_solidRGB = label2rgb(I_axes,image = I_gray)
## Conteo total
#print('conteo 1:', max(np.ravel(I_axes)))
#print('conteo 2:', max(np.ravel(I_areaConv)))
#print('conteo 3:', max(np.ravel(I_solid)))
#
##I_final = I_axes * I_areaConv * I_solid
#I_finalRGB = label2rgb(I_final,image = I_gray)
#fig,ax = plt.subplots(1)
##ax.imshow(I_axesRGB,cmap='gray')
#ax.imshow(I_finalRGB,cmap='gray')
#ax.set_axis_off()
#plt.tight_layout()
#plt.title('Etiquetado final')
#plt.show()
    

# In[] Funciones
def PCA(m_I):
    '''
    Función que realiza PCA mediante SDV (Singular Decomposition Value) para
    obtener el plano de mayor información en una imagen.
    
    m_I: Imagen en RGB.
    
    Retorna IMG: Imagen de igual dimensión que contienen la mayor información
    escalada entre 0-1.
    '''
    dim = m_I.shape
    X = np.asarray([m_I[:,:,0].ravel(),m_I[:,:,1].ravel(),m_I[:,:,2].ravel()])#1 canal por fila
    S = np.cov(X)
    U,V = LA.eig(S)
    V2 = V[np.argmax(U),:]
    Y = np.matmul(V2,X)
    IMG = ( 1- np.reshape(Y,(dim[0],dim[1])) )/256
    return IMG

#NO SIEMPRE HAY QUE INVERTIRLA, ¿CÓMO SABER LA FASE?
    
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

def otsu_region(I,m_I,r,centros,d):
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
#    colonias = 0
    m = np.shape(m_I)
    m_I = rescale_intensity(m_I,in_range=(0.2,0.8),out_range=(0,1))
    m_BW = np.ones([m[0],m[1]])#Imagen blanca
    for k in range(0,len(centros)):
        m_I_pozo = pozos(m_I,centros[k],r)
        m_I_otsu = otsu(m_I_pozo,m_I,centros[k],r)
#        #etiquetado, regionprops y conteo
#        labeled,num = label(m_I_otsu,neighbors=8, background=0,return_num=True)
        I_axes,num = intento(I,m_I_otsu)
        
#        fig = plt.figure()
#        ax1 = fig.add_subplot(111)
#        ax1.axis('off')
#        ax1.imshow(I_axes,cmap='spectral')
#        
        print('Hay ' + str(num) + ' colonias en el pozo ' + str(k) + '.')
        
        d[ list(d.keys())[k] ].append(num)
##        colonias += num
        m_BW = m_BW * I_axes
#    print('Hay ' + str(colonias) + ' colonias en total.')
    
    return m_BW,d



def otsu(I_cro,I_gray2,centro,r):
    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
    prom = np.mean(I2)
#    prom = np.median(I2)
    thresh = threshold_otsu(I2)*prom
    BW = I_cro > thresh
    BW2 = 1 - BW
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.axis('off')
    ax1.imshow(BW2,cmap='gray')
    
    return BW2

def otsu2(I_gray2,centro,r):
    I2 = I_gray2[(centro[1]-r):(centro[1]+r),(centro[0]-r):(centro[0]+r)]
    prom = np.mean(I2)
    thresh = threshold_otsu(I2)*prom
    BW = I_gray2 > thresh
    BW = 1 - BW
    return BW

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
        y = coordinates[0][0]-r_pozo-2
        x = coordinates[0][1]+r_pozo+2
    else:
        y = coordinates[1][0]-r_pozo-2
        x = coordinates[1][1]+r_pozo+2
    #coordenadas de los otros pozos por simetría
    centros = [[x,y],[x,y+2*r_pozo + 5]]
    for i in range(0,2):
        centros.append([centros[i][0] + 2*r_pozo+3,centros[i][1] ])
        centros.append([centros[i][0] - 2*r_pozo-3,centros[i][1] ])
    
    centros = sorted(centros)
    centros = np.asarray(centros)#(x,y)
    
    return centros

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
#            else:
#                I_new[i,j] = 0

#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    ax1.axis('off')
#    ax1.imshow(BW,cmap='gray')
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
#            else:
#                I_new[i,j] = 0
            
    return I_new



def circle(r):
    '''
    Función que genera un template circular negro con radio r.
    r: radio del círculo en píxeles.
    
    Retorna: Matriz que describe un círculo con radio r píxeles.
    
    '''
    dim = r*2 + 15#dimensión de la matriz.
    Nigerrimo = np.zeros([dim,dim])
    centro = [dim/2,dim/2]
    for i in range(0,dim):
        for j in range(0,dim):
            d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
            if d > r and d < r+5:
                Nigerrimo[i,j] = 1
    return Nigerrimo



# In[]
#def cie(I):
I = imread(PATH)
# In[]
I2 = np.copy(I)
I2[:,:,0] = pozos2(I[:,:,0],centros,r_pozo) 
I2[:,:,1] = pozos2(I[:,:,1],centros,r_pozo) 
I2[:,:,2] = pozos2(I[:,:,2],centros,r_pozo) 

I_cie = rgb2lab(I2,illuminant='D65',observer='2') 

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.axis('off')
ax1.imshow(I2,cmap='gray')    

x = plt.ginput(1)
color = I_cie[int(round(x[0][0])),int(round(x[0][1])),1::]
m = np.shape(I_cie[:,:,0])
umbral = 25
IRGB = np.copy(rgb2gray(I))
IRGB = pozos2(IRGB,centros,r_pozo) 

for i in range(0,m[0]):
    for j in range(0,m[1]):
        pix = I_cie[i,j,1::]
        dist = np.linalg.norm(color-pix)
        if dist < umbral:
                IR[i,j] = I[i,j,0]
                IG[i,j] = I[i,j,1]
                IB[i,j] = I[i,j,2]
#            IRGB[i,j] = 1

#IRGB = 1-IRGB     
#IRGB = IRGB > 0.7
   
    IRGB[:,:,0] = IR   
    IRGB[:,:,1] = IG 
    IRGB[:,:,2] = IB
#    return IRGB


#color = cie(I)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.axis('off')
ax2.imshow(IRGB,cmap='gray')
