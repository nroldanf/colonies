# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:42:04 2019

@author: Nicol
"""
import numpy as np
import math
from skimage.color import rgb2gray
from skimage.color import rgb2lab
from skimage.exposure import rescale_intensity
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import diamond
from skimage.morphology import closing
from skimage.filters.thresholding import threshold_otsu
from skimage.measure import regionprops
from skimage.measure import label
from skimage.color import label2rgb
from sklearn.cluster import KMeans



class Colonias:
    def __init__(self,image):
        self.image = image
        self.shape = self.image.shape
        self.r_small = 50
        self.r_pozo = 140
        self.min_distance = 160
        self.s = diamond(4)
        self.template = self.__circle()
    
    # Helpers    
    def mejoraConstraste(self):
        I_gray = rgb2gray(self.image)
        I_gray = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))
        return I_gray
        
    def __canny(self):
        BW = canny(self.mejoraConstraste(),sigma=0.5)
        return BW
    
    def __closing(self):
        BW = closing(self.__canny(),self.s)
        return BW
    
    def __crossCorrelation(self):
        result = match_template(self.__closing(),self.template,pad_input = True)
        return result
    
    def corr2d(self):
        coordinates = peak_local_max(self.__crossCorrelation(), min_distance=self.min_distance)
        
        if coordinates[0][1] < coordinates[1][1]:
            y = coordinates[0][0]-self.r_pozo-5
            x = coordinates[0][1]+self.r_pozo+5
        else:
            y = coordinates[1][0]-self.r_pozo-5
            x = coordinates[1][1]+self.r_pozo+5
        #coordenadas de los otros pozos por simetría
        centros = [[x,y],[x,y+2*self.r_pozo + 10]]
        for i in range(0,2):
            centros.append([centros[i][0] + 2*self.r_pozo + 10 ,centros[i][1] ])
            centros.append([centros[i][0] - 2*self.r_pozo - 10,centros[i][1] ])
        
        centros = sorted(centros)
        centros = np.asarray(centros)#(x,y)
        
        return centros
    
    def pozo(self,centro,m_I):
#        m_I = self.mejoraConstraste()
        I_new = np.zeros([self.shape[0],self.shape[1]])
        for i in range(0,self.shape[0]):
            for j in range(self.shape[1]):
                d = math.sqrt(abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) )
                if d <= self.r_pozo:
                    I_new[i,j] = m_I[i,j]
        return I_new
    
    
    def otsu(self,I_pozo,I_gray,centro):
        I = I_gray[(centro[1]-self.r_pozo):(centro[1]+self.r_pozo),(centro[0]-self.r_pozo):(centro[0]+self.r_pozo)]
        prom = np.mean(I)
        thresh = threshold_otsu(I)*prom
        BW = I_pozo > thresh
        BW = 1-BW
        return BW
    
    def pozo_anillo(self,m_I,centro):
        I_new = np.ones([self.shape[0],self.shape[1]])
        prom = []
        for i in range(0,self.shape[0]):
            for j in range(0,self.shape[1]):
                d = math.sqrt( abs( (centro[1] - i)**2 + (centro[0] - j)**2 ) ) 
                if d <= self.r_pozo and d >= self.r_pozo-20:
                    I_new[i,j] = m_I[i,j]
                    prom.append([i,j])
        return I_new,prom

    def reg_seg(self,Iseg):
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
        
    def color(self,I_gray,centro):
        I_bordes,prom = self.pozo_anillo(I_gray,centro)
        I2 = np.copy(self.image)
        #por plano se toman los anillos
        I2[:,:,0],prom = self.pozo_anillo(self.image[:,:,0],centro)
        I2[:,:,1],prom = self.pozo_anillo(self.image[:,:,1],centro)
        I2[:,:,2],prom = self.pozo_anillo(self.image[:,:,2],centro)
        promcito = np.asarray(prom)#vuelvo arreglo la lista de listas prom
        I_color = rgb2lab(I2,illuminant='D65',observer='2')
        m = np.shape(I_color[:,:,0])
        promedio = [
            np.mean( I_color[promcito[:,0],promcito[:,1],1] ), 
            np.mean( I_color[promcito[:,0],promcito[:,1],2] ) 
        ]
        IRGB = rgb2gray(self.image)
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
    

    def clustering(self):
        # Number of clusters to be used
        n_colors = 4
        #Reshaping to a vector
        size = self.image.shape
        #Clustering with cromatic planes of L*a*b space
        Ilab = rgb2lab(self.image,illuminant='D65',observer='2')
        # Feature matrix of cromatic planes
        #croma = # Cromatic planes a and b
        I_plane = np.reshape(Ilab[:,:,1:3],(size[0]*size[1],2))
        # Cluster the pixel intensities
        clt = KMeans(init = "k-means++",n_clusters = n_colors,n_init = 10)
        clt.fit(I_plane)
        y = clt.fit_predict(I_plane)#iimagendices de cada muestra
        
        

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
    
    
    def processing(self):
        I_gray = self.mejoraConstraste()
        centros = self.corr2d()
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
        
        for k in range(0,len(centros)):
            # Seccionamiento de 1 pozo
            I_seg = self.pozo(centros[k],I_gray)
            # Otsu por pozo
            I_otsu = self.otsu(I_seg,I_gray,centros[k])
            # Mascara color para los bordes
            I_color = self.color(I_gray,centros[k])
            # Aplicación de las propiedades de region
            I_props = self.reg_seg(I_otsu*I_color)
            # Etiquetado y conteo de las colonias
            # 8-conectividad, fondo negro
            labeled,num = label(
                I_props, neighbors=8, background=0,
                return_num=True
            )
#            # Guarda el conteo por pozo en un diccionario
#            dic[ list(dic.keys())[k] ].append(num)
            # Suma el resultado del pozo a una imagen negra (ceros)
            m_BW = m_BW + I_props

        labeled = label(m_BW, neighbors=8, background=0)
        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        
        return labeled_RGB
    
    
    #conncomponents