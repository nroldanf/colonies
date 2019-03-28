# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:42:04 2019

@author: Nicol
"""
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.color import rgb2gray,rgb2hsv
from skimage.color import rgb2lab
from skimage.exposure import rescale_intensity, adjust_gamma
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import diamond, disk
from skimage.morphology import opening, black_tophat, closing
from skimage.filters.thresholding import threshold_otsu
from skimage.measure import regionprops
from skimage.measure import label
from skimage.color import label2rgb
from sklearn.cluster import KMeans
from scipy.ndimage.morphology import distance_transform_edt
from skimage.morphology import watershed
from scipy import ndimage as ndi






class Colonias:
    def __init__(self,image):
        self.image = image
        self.shape = self.image.shape
        self.r_small = 50
        self.r_pozo = 140
        self.min_distance = 160
        self.s = diamond(4)
        self.s1 = diamond(1)# Elemento estructurante para la apertura
        self.s2 = diamond(6)# Elemento estructurante para el black Top Hat
        self.template = self.__circle()
        self.centros = 0
    
    # Helpers    
    def mejoraConstraste(self):
        I_gray = rgb2gray(self.image)
        I_gray = rescale_intensity(I_gray,in_range=(0.2,0.8),out_range=(0,1))
        return I_gray
    
    
    # 3. P
    def preprocess(self):
        Igray = rgb2gray(self.image)
        Ieq = adjust_gamma(Igray,0.4)
        Iop = opening(Ieq,self.s1)
        # Retorna lo que sea más pequeño que el elemento estructurante
        # Podría ser un parámetro definido por el usuario, basado en 
        # la colonia más grande
        If = black_tophat(Iop,self.s2)
        If2 = adjust_gamma(If,0.8)# Mejora de contraste
#        self.hist_comparison(If,If2,'gamma 0.8')
#        self.hist_comparison(If,If3,'gamma 0.7')
        # Binarización
        thresh = threshold_otsu(If2)
        BW = If > thresh
        return BW,If2
    
    
    # 1. Umbralización con el plano de value
    def preprocessHSV_value(self):
        I = np.copy(self.image)
        for i in range(0,3):
            I[:,:,i] = adjust_gamma(I[:,:,i],0.4)
            I[:,:,i] = opening(I[:,:,i],self.s1)
            I[:,:,i] = black_tophat(I[:,:,i],self.s2)
            I[:,:,i] = adjust_gamma(I[:,:,i],0.8)
            
        hsv = rgb2hsv(I)        
        thresh = threshold_otsu(hsv[:,:,2])
        BW = hsv[:,:,2] > thresh
        
        return hsv[:,:,2],BW# retorne plano de value (intensidad)
    
    # 2. Umbralización con el plano de saturation
    def preprocessHSV_saturation(self):
        I = np.copy(self.image)
        hsv = rgb2hsv(I)
        thresh = threshold_otsu(hsv[:,:,1])
        BW = hsv[:,:,1] > thresh
        return hsv[:,:,1],BW# retorne plano de value (intensidad)
        
    
        
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
        self.centros= centros
        
        return centros
    
    def pozo(self,c,m_I):
#        m_I = self.mejoraConstraste()
        I_new = np.zeros([self.shape[0],self.shape[1]])
        n = [c[1]-self.r_pozo,c[1]+self.r_pozo,c[0]-self.r_pozo,c[0]+self.r_pozo]
        for i in range(n[0],n[1]):
            for j in range(n[2],n[3]):
                d = np.sqrt(abs((c[1]-i)**2+(c[0]-j)**2)) 
                if d < self.r_pozo:
                    I_new[i,j] = m_I[i,j]
        return I_new
    
    def pozos2(self,I,c,P):
        I_new = np.zeros([self.shape[0],self.shape[1]])
        n = len(P)
        for i in range(0,n):
            j = P[i]
            d  = np.sqrt(abs(np.square(c[0]-j[1])+np.square(c[1]-j[0])))
            if (d<= self.r_pozo and d>= self.r_pozo-20):
                I_new[j[0],j[1]] = I[j[0],j[1]]
        return I_new
    
        
    
    def otsu(self,I_pozo,I_gray,centro):
        I = I_gray[(centro[1]-self.r_pozo):(centro[1]+self.r_pozo),(centro[0]-self.r_pozo):(centro[0]+self.r_pozo)]
        thresh = threshold_otsu(I)
        BW = I_pozo > thresh
        return BW
    
    def otsuMean(self,I_pozo,I_gray,centro):
        I = I_gray[(centro[1]-self.r_pozo):(centro[1]+self.r_pozo),(centro[0]-self.r_pozo):(centro[0]+self.r_pozo)]
        prom = np.mean(I)
        thresh = threshold_otsu(I)*prom
        BW = I_pozo > thresh
        return BW
    
    def pozo_anillo(self,m_I,c):
        
        I_new = np.ones([self.shape[0],self.shape[1]])
        prom = []
        n = [c[1]-self.r_pozo,c[1]+self.r_pozo,c[0]-self.r_pozo,c[0]+self.r_pozo]
        for i in range(n[0],n[1]):
            for j in range(n[2],n[3]):
                d = math.sqrt( abs( (c[1] - i)**2 + (c[0] - j)**2 ) ) 
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
            area = region.area
            ecc = region.eccentricity
            #Razon entre pixeles de la region y pixeles de la envolvente
    #        solidez = region.solidity 
            eje_mayor = region.major_axis_length
            eje_menor = region.minor_axis_length 
            if   eje_menor != 0:            
                axes_ratio = eje_mayor/eje_menor
            else:
                axes_ratio = 0
                
            if area_convexa < 7 or ecc > 0.9 or area_convexa > 80: 
                Iseg[labeled == i] = 0
    
            i += 1
        return Iseg
        
    def color(self,I_gray,c):
        IRGB = rgb2gray(self.image)
        I_gray,prom = self.pozo_anillo(I_gray,c)
        I = np.copy(self.image)
        for n in range(0,3):
            I[:,:,n] = self.pozos2(self.image[:,:,n],c,prom)
        
        prome = np.asarray(prom)#vuelvo arreglo la lista de listas prom
        I_color = rgb2lab(I,illuminant='D65',observer='2')
        promedio = [np.mean(I_color[prome[:,0],prome[:,1],1] ),
                    np.mean(I_color[prome[:,0],prome[:,1],2])]
        n = [c[1]-self.r_pozo,c[1]+self.r_pozo,c[0]-self.r_pozo,c[0]+self.r_pozo]
        n = len(prom)
        for i in range(0,n):
            j = prom[i]
            dist = np.linalg.norm(promedio-I_color[j[0],[1],1::])
            if dist < 5:
                IRGB[j[0],j[1]] = 1
        IRGB = (1 - IRGB)> 0.7
        I_fin = (I_gray + IRGB) > 0.9
        return I_fin
    



#    def clustering(self):
#        # Number of clusters to be used
#        n_colors = 4
#        #Reshaping to a vector
#        size = self.image.shape
#        #Clustering with cromatic planes of L*a*b space
#        Ilab = rgb2lab(self.image,illuminant='D65',observer='2')
#        # Feature matrix of cromatic planes
#        #croma = # Cromatic planes a and b
#        I_plane = np.reshape(Ilab[:,:,1:3],(size[0]*size[1],2))
#        # Cluster the pixel intensities
#        clt = KMeans(init = "k-means++",n_clusters = n_colors,n_init = 10)
#        clt.fit(I_plane)
#        y = clt.fit_predict(I_plane)#iimagendices de cada muestra
        
        

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
        BW,I_gray = self.preprocess()
        
#        Ivalue = self.preprocessHSV()
#        I_gray = rgb2gray(self.image)
        
        centros = self.corr2d()        
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
#        conteo = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],
#        'Pozo 5':[],'Pozo 6':[]}# Diccionario donde se guarda el conteo
        conteo = []
        for k in range(0,len(centros)):
            try:
                # Seccionamiento de 1 pozo
                I_seg = self.pozo(centros[k],I_gray)
                # Otsu por pozo
                I_otsu = self.otsu(I_seg,I_gray,centros[k])
                # Mascara color para los bordes
                I_color = self.color(I_gray,centros[k])
                # Aplicación de las propiedades de region
                I_props = self.reg_seg(I_otsu)
                # Watershed
                I_wa = self.watershedDT(I_props)
                I_wa[I_wa>0]=1
                # Etiquetado y conteo de las colonias
                # 8-conectividad, fondo negro
                labeled,num = label(
                    I_wa, neighbors=8, background=0,
                    return_num=True
                )
                
    #            # Guarda el conteo por pozo en un diccionario
#                conteo[ list(conteo.keys())[k] ].append(num)
                
                # Guarda el conteo en un arreglo
                conteo.append(num)
                
                # Suma el resultado del pozo a una imagen negra (ceros)
                m_BW = m_BW + I_wa
            except:
                print('Pozo no viable')

        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        color = self.addColor(self.image,m_BW)
        
        return m_BW,conteo,color
    
    
    def processing2(self):
        BW,I_gray = self.preprocessHSV_saturation()
        
#        Ivalue = self.preprocessHSV()
#        I_gray = rgb2gray(self.image)
        
        centros = self.corr2d()        
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
#        conteo = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],
#        'Pozo 5':[],'Pozo 6':[]}# Diccionario donde se guarda el conteo
        conteo = []
        for k in range(0,len(centros)):
            try:
                # Seccionamiento de 1 pozo
                I_seg = self.pozo(centros[k],I_gray)
                # Otsu por pozo
                I_otsu = self.otsu(I_seg,I_gray,centros[k])
                # Mascara color para los bordes
#                I_color = self.color(I_gray,centros[k])
                # Aplicación de las propiedades de region
                I_props = self.reg_seg(I_otsu)
                # Watershed
                I_wa = self.watershedDT(I_props)
                I_wa[I_wa>0]=1
                # Etiquetado y conteo de las colonias
                # 8-conectividad, fondo negro
                labeled,num = label(
                    I_wa, neighbors=8, background=0,
                    return_num=True
                )
                
    #            # Guarda el conteo por pozo en un diccionario
#                conteo[ list(conteo.keys())[k] ].append(num)
                
                # Guarda el conteo en un arreglo
                conteo.append(num)
                
                # Suma el resultado del pozo a una imagen negra (ceros)
                m_BW = m_BW + I_wa
            except:
                print('Pozo no viable')

        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        color = self.addColor(self.image,m_BW)
        
        return m_BW,conteo,color
    
    def processing3(self):
        BW,I_gray = self.preprocessHSV_saturation()
        
#        Ivalue = self.preprocessHSV()
#        I_gray = rgb2gray(self.image)
        
        centros = self.corr2d()        
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
#        conteo = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],
#        'Pozo 5':[],'Pozo 6':[]}# Diccionario donde se guarda el conteo
        conteo = []
        for k in range(0,len(centros)):
            try:
                # Seccionamiento de 1 pozo
                I_seg = self.pozo(centros[k],BW)
                # Otsu por pozo
#                I_otsu = self.otsu(I_seg,I_gray,centros[k])
                # Mascara color para los bordes
#                I_color = self.color(I_gray,centros[k])
                # Aplicación de las propiedades de region
                I_props = self.reg_seg(I_seg)
                # Watershed
                I_wa = self.watershedDT(I_props)
                I_wa[I_wa>0]=1
                # Etiquetado y conteo de las colonias
                # 8-conectividad, fondo negro
                labeled,num = label(
                    I_wa, neighbors=8, background=0,
                    return_num=True
                )
                
    #            # Guarda el conteo por pozo en un diccionario
#                conteo[ list(conteo.keys())[k] ].append(num)
                
                # Guarda el conteo en un arreglo
                conteo.append(num)
                
                # Suma el resultado del pozo a una imagen negra (ceros)
                m_BW = m_BW + I_wa
            except:
                print('Pozo no viable')

        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        color = self.addColor(self.image,m_BW)
        
        return m_BW,conteo,color
    
# Local
    def processing4(self):
        BW,I_gray = self.preprocessHSV_value()
        
        centros = self.corr2d()        
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
#        conteo = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],
#        'Pozo 5':[],'Pozo 6':[]}# Diccionario donde se guarda el conteo
        conteo = []
        for k in range(0,len(centros)):
            try:
                # Seccionamiento de 1 pozo
                I_seg = self.pozo(centros[k],I_gray)
                # Otsu por pozo
                I_otsu = self.otsu(I_seg,I_gray,centros[k])
                # Mascara color para los bordes
#                I_color = self.color(I_gray,centros[k])
                # Aplicación de las propiedades de region
                I_props = self.reg_seg(I_otsu)
                # Watershed
                I_wa = self.watershedDT(I_props)
                I_wa[I_wa>0]=1
                # Etiquetado y conteo de las colonias
                # 8-conectividad, fondo negro
                labeled,num = label(
                    I_wa, neighbors=8, background=0,
                    return_num=True
                )
                
    #            # Guarda el conteo por pozo en un diccionario
#                conteo[ list(conteo.keys())[k] ].append(num)
                
                # Guarda el conteo en un arreglo
                conteo.append(num)
                
                # Suma el resultado del pozo a una imagen negra (ceros)
                m_BW = m_BW + I_wa
            except:
                print('Pozo no viable')

        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        color = self.addColor(self.image,m_BW)
        
        return m_BW,conteo,color
    
# Global
    def processing5(self):
        BW,I_gray = self.preprocessHSV_value()
        
        centros = self.corr2d()        
        m_BW = np.zeros([self.shape[0],self.shape[1]])#Imagen negra de la misma dimensión
#        conteo = {'Pozo 1':[],'Pozo 2':[],'Pozo 3':[],'Pozo 4':[],
#        'Pozo 5':[],'Pozo 6':[]}# Diccionario donde se guarda el conteo
        conteo = []
        for k in range(0,len(centros)):
            try:
                # Seccionamiento de 1 pozo
                I_seg = self.pozo(centros[k],BW)
                # Otsu por pozo
#                I_otsu = self.otsu(I_seg,I_gray,centros[k])
                # Mascara color para los bordes
#                I_color = self.color(I_gray,centros[k])
                # Aplicación de las propiedades de region
                I_props = self.reg_seg(I_seg)
                # Watershed
                I_wa = self.watershedDT(I_props)
                I_wa[I_wa>0]=1
                # Etiquetado y conteo de las colonias
                # 8-conectividad, fondo negro
                labeled,num = label(
                    I_wa, neighbors=8, background=0,
                    return_num=True
                )
                
    #            # Guarda el conteo por pozo en un diccionario
#                conteo[ list(conteo.keys())[k] ].append(num)
                
                # Guarda el conteo en un arreglo
                conteo.append(num)
                
                # Suma el resultado del pozo a una imagen negra (ceros)
                m_BW = m_BW + I_wa
            except:
                print('Pozo no viable')

        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        color = self.addColor(self.image,m_BW)
        
        return m_BW,conteo,color
    
    
#    I_seg = pozo(If2,centros[k],r_pozo)# Se recorta un pozo
#    #            plot_comparison(I,I_seg,'Binarización Otsu')
#            BW = otsuNew(I_seg,If2,centros[k],r_pozo)
#            I_color = color(I,centros[k],r_pozo)
#            I_bor = (BW * I_color)
#            I_props = reg_seg(I_bor)
#            I_wa = watershedDT(I_bor)
#            I_wa[I_wa>0]=1
#            labeled,num = label(I_wa,neighbors=8, background=0,return_num=True,connectivity=10)#etiquetado y conteo
#    #            print('Hay ' + str(num) + ' colonias en el pozo ' + str(k) + '.')
#            # LLena el diccionario con cada conteo, por cada uno de los pozos k
#            dic[ list(dic.keys())[k] ].append(num)
#    #            plot_comparison(If2,BW,'Binarización Otsu')
#            m_BW = m_BW + I_wa
#            #'''''''''''''''''''''''
#            I_segfin = I_segfin + I_seg
#            I_otsufin = I_otsufin + BW
#            I_propsfin = I_propsfin + I_props
#            I_colorfin = I_colorfin + I_color
    
    def watershedDT(self,I):
        dist = distance_transform_edt(I)
        # Máximos locales hallados en una vecindad de 3x3
        local_maxi = peak_local_max(dist, indices=False, footprint=np.ones((3, 3)),
                                    labels=I)
        # footprint es la vecindad para hallar máximos regionales
        markers = ndi.label(local_maxi)[0]# Lo convierte a una matriz de enteros
        # Se invierte para que así los máximos ahora sean mínimos (catch basins)
        labels = watershed(-dist, markers, mask=I)# Algoritmo basado en marcadores
        return labels
    #conncomponents
    
    def addColor(self,I,BW):
        R = I[:,:,0]
        G = I[:,:,1]
        B = I[:,:,2]
        s = BW.shape
        for i in range(0,s[0]):
            for j in range(0,s[1]):
                if BW[i,j] == 1:
                    R[i,j] = 255
                    G[i,j] = 0
                    B[i,j] = 0        
        I[:,:,0] = R
        I[:,:,1] = G
        I[:,:,2] = B
        return I
    
    def hist_comparison(self,original,modified,name):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                       sharey=True)
        ax1.hist(original.ravel(),256,[0,1])
        ax1.set_title('original')
        ax2.hist(modified.ravel(),256,[0,1])
        ax2.set_title(name)