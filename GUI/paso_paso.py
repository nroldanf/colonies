"""
Created on Sun Jun 10 16:20:43 2018

@authors: Nicolás, Liz, Mafius
"""


import os
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy.misc import imsave
from skimage.io import imread
from skimage.color import label2rgb
from skimage.exposure import rescale_intensity
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import closing
from skimage.morphology import diamond
from funciones2 import *


# In[Carga de los nombres de las imágenes]
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
image_ids = list()#ID's de las imágenes
# Creacíon de una matriz que contenga todos los ids, 
# donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
r_small = 50#Radio del círculo pequeño
r_pozo = 140#Radio del pozo
template = circle(r_small)#Template para la correlación
s = diamond(4)#elemento estructurante para el cierre
# In[Procesamiento por imagen]
for folder in range(1,len(folder_ids)):# Para cada carpeta
    for image in range(1,len(image_ids[folder])):# Para cada imagen
        # Diccionario donde se guarda el conteo
        dic = {
            'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],
            'Pozo 4':[],'Pozo 5':[],'Pozo 6':[]
        }
        # PATH de la imagen
        PATH = gen + folder_ids[folder] + '/' + image_ids[folder][image]
        # Imagen original
        I = imread(PATH)
        # Conversión a escala de grises
        I_gray = rgb2gray(I)
        # Mejora de contraste
        I_gray = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))
        # Máscara por Canny
        BW = canny(I_gray,sigma=0.5)
        #Operación morfológica
        BW = closing(BW,s)
        # Correlación Cruzada
        result = match_template(BW,template,pad_input = True)
        # Encontrar máximos locales correspondiente a los centros
        coordinates = peak_local_max(result, min_distance=160)
        # Encontrar los centros de los pozos por ubicación
        centros = corr2d(coordinates, template, r_pozo)
        # *** Seccionamiento y segmentación ***
        m = np.shape(I_gray)# Dimensión de la imagen
        m_BW = np.zeros([m[0],m[1]])#Imagen negra de la misma dimensión
        print('Empece por los pozos')
        # Para cada pozo 
        for k in range(0,len(centros)):
            print('Pozo'+str(k))
            # Seccionamiento de 1 pozo
            I_seg = pozo(I_gray, centros[k], r_pozo)
            # Otsu por pozo
            I_otsu = otsu(I_seg, I_gray, centros[k], r_pozo)
            print('Otsu')
            # Mascara color para los bordes
            I_color = color(I, I_gray, centros[k], r_pozo)
            print('Color aplicado')
            # Aplicación de las propiedades de region
            I_props = reg_seg(I_otsu*I_color)
            print('Propiedades de la región')
            # Etiquetado y conteo de las colonias
            # 8-conectividad, fondo negro
            labeled,num = label(
                I_props, neighbors=8, background=0,
                return_num=True
            )
            # Guarda el conteo por pozo en un diccionario
            dic[ list(dic.keys())[k] ].append(num)
            # Suma el resultado del pozo a una imagen negra (ceros)
            m_BW = m_BW + I_props

        print('Termine los pozos')
        plt.figure()
        plt.axis('off')
        plt.imshow(m_BW,cmap='gray')
        plt.title('Colonias segmentadas')
        # Etiquetado
        labeled = label(m_BW, neighbors=8, background=0)
        labeled_RGB = label2rgb(labeled, image=I)#image = imagen original

        plt.figure()
        plt.axis('off')
        plt.imshow(labeled_RGB,cmap='gray')
        plt.title('Etiquetado final')
        # Conversión del diccionario a dataframe de Pandas para visualizarlo
        # de mejor forma y poder guardar como .csv posteriormente.
        frame_test = pd.DataFrame(dic,index=image_ids[i])
        # Guarda el conteo como archivo .csv
#        frame_test.to_csv(
#            'Resultados finales/' + folder_ids[i] + '/' + 
#            image_ids[folder][image] + '/' + 'Conteo' + '.csv'
#        )