# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 20:29:56 2018

@author: Nicolas
"""

import numpy as np

from skimage.color import rgb2gray
from skimage.exposure import rescale_intensity
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import diamond
from skimage.morphology import closing


class Colonias:
    # Método constructor: Inicialización del objeto
    def __init__(self,image):
        self.image = image
        self.r_small = 50#Radio del círculo pequeño
        self.r_pozo = 140#Radio del pozo
        
        self.min_distance = 160# Distancia minima entre circulos del recipiente
        
        self.s = diamond(4)#elemento estructurante para el cierre
        self.template = self.__circle()#Template para la correlación
    
    def mejoraContraste(self): 
        I_gray = rgb2gray(self.image)# Conversión a escala de grises
        I_gray = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))
        return I_gray
    
    def Canny(self):
        BW = canny(self.mejoraContraste(),sigma=0.5)
        return BW

    def Closing(self):
        BW = closing(self.Canny(),self.s)
        return BW
    
    def crossCorrelation(self):        
        result = match_template(self.Closing(),self.template,pad_input = True)
        return result
    
    def __localMax(self):
        self.coordinates = peak_local_max(self.crossCorrelation(), min_distance=self.min_distance)
#        return coordinates
    
    def corr2d(self):
        '''
        Realiza la correlación cruzada normalizada [1] con una imagen template.
        
        BW: Imagen con los bordes segmentados.
        template: Imagen con el template para realizar la correlación.
        r_pozo: Radio del pozo en píxeles.
        
        
        Retorna centros: Arreglo de coordenadas (x,y) con los centros de los pozos
        ubicados en el siguiente orden.   
        '''
        #podría reeemplazar el if-else:
    #    coordinates = np.sort(coordinates, axis=1, kind='quicksort', order=None)
    
        self.__localMax()
    
        if self.coordinates[0][1] < self.coordinates[1][1]:
            y = self.coordinates[0][0]-self.r_pozo-5
            x = self.coordinates[0][1]+self.r_pozo+5
        else:
            y = self.coordinates[1][0]-self.r_pozo-5
            x = self.coordinates[1][1]+self.r_pozo+5
        #coordenadas de los otros pozos por simetría
        centros = [[x,y],[x,y+2*self.r_pozo + 10]]
        for i in range(0,2):
            centros.append([centros[i][0] + 2*self.r_pozo + 10 ,centros[i][1] ])
            centros.append([centros[i][0] - 2*self.r_pozo - 10,centros[i][1] ])
        
        centros = sorted(centros)
        centros = np.asarray(centros)#(x,y)
        
        return centros
    
    #Helpers
    def __circle(self):
        dim = self.r_small*2 + 15#dimensión de la matriz.
        Nigerrimo = np.zeros([dim,dim])
        centro = [dim/2,dim/2]
        for i in range(0,dim):
            for j in range(0,dim):
                d = np.sqrt(abs( (centro[0] - i)**2 + (centro[1] - j)**2 ))
                if d > self.r_small and d < self.r_small+4:
                    Nigerrimo[i,j] = 1
        return Nigerrimo

