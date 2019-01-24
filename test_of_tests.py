# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:08:36 2019

@author: Nicol
"""

import numpy as np
import math
import os
import matplotlib.pyplot as plt
import cv2 as cv

from funciones import*


from skimage.morphology import diamond
from skimage.io import imread 
from skimage.color import rgb2gray
from skimage.color import rgb2lab
from skimage.exposure import rescale_intensity, equalize_hist, equalize_adapthist
from skimage.feature import match_template,peak_local_max,canny
from skimage.morphology import diamond
from skimage.morphology import closing, watershed
from skimage.filters.thresholding import threshold_otsu
from skimage.measure import regionprops
from skimage.measure import label
from skimage.color import label2rgb
from sklearn.cluster import KMeans
from skimage.filters import gaussian, sobel
from skimage.util import invert
from skimage.filters import try_all_threshold


from scipy import ndimage as ndi


from skimage.transform import hough_circle, hough_circle_peaks
# In[]
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
#ID's de las imágenes
image_ids = list()
#Creacíon de una matriz que contenga todos los ids, donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )

PATH = gen + folder_ids[0] + '/' + image_ids[0][1]

I = imread(PATH)
Igray = rgb2gray(I)
# In[]
#Operación morfológica
r_small = 50# Radio de los círculos del recipiente
r_pozo = 140# Radio del pozo
template = circle(r_small)# Template para la correlación    

BW = canny(Igray,sigma=0.5)#Operación morfológica
BW = closing(BW,s)
result = match_template(BW,template,pad_input = True)
coordinates = peak_local_max(result, min_distance=160)#centro del pequeño 
centros = corr2d(coordinates,template,r_pozo)    

Inueva = pozos(Igray,centros,r_pozo)

plt.figure()
plt.axis('off')
plt.imshow(Inueva,cmap='gray')
plt.show()

# In[]
plt.close('all')
Ifilt = gaussian(Igray,sigma = 3)

plt.figure()
plt.axis('off')
plt.imshow(Ifilt,cmap='gray')
plt.show()

Ifinal = invert(Igray-Ifilt)

graficar(Ifinal)
histo(Ifinal)

# Máscara binaria de todos los pozos
#mask = pozos(Igray,centros,r_pozo)
# Ecualización de histograma
Ieq = equalize_hist(Igray, nbins=256)

histo(Ieq)
Ieq2 = equalize_adapthist(Igray)

histo(Ieq2)
graficar(Ieq2)
graficar(Igray)

Ieq3 = rescale_intensity(Igray,in_range=(0.2,0.8),out_range=(0,1))
histo(Ieq3)
fig,ax = try_all_threshold(Ieq3, figsize=(8, 5), verbose=True)

# In[]
s = diamond(4)# elemento estructurante

edges = canny(Igray, sigma=0.5)
edges = closing(edges,s)

plt.figure()
plt.axis('off')
plt.imshow(edges,cmap='gray')
plt.show()

# Detect two radii
hough_radii = np.arange(20, 35, 2)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 5 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=6)

plt.figure()
plt.axis('off')
plt.imshow(Igray,cmap='gray')
for l in range(0,6):
    plt.plot(cx[l],cy[l],'ro')

plt.show()

## Draw them
#fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
##image = color.gray2rgb(I)
#for center_y, center_x, radius in zip(cy, cx, radii):
#    circy, circx = circle_perimeter(center_y, center_x, radius)
#    I[circy, circx] = (220, 20, 20)
#
#ax.imshow(I, cmap=plt.cm.gray)
#plt.show()
# In[] Segmentación por Watershed
# Preprocesamiento

# Now we want to separate the two objects in image
# Generate the markers as local maxima of the distance to the background
distance = ndi.distance_transform_edt(Igray)

local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
                            labels=Igray)
markers = ndi.label(local_maxi)[0]
labels = watershed(distance, markers, mask=Igray)

fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(Igray, cmap=plt.cm.gray, interpolation='nearest')
ax[0].set_title('Overlapping objects')
ax[1].imshow(-distance, cmap=plt.cm.gray, interpolation='nearest')
ax[1].set_title('Distances')
ax[2].imshow(labels, cmap=plt.cm.nipy_spectral, interpolation='nearest')
ax[2].set_title('Separated objects')

for a in ax:
    a.set_axis_off()

fig.tight_layout()
plt.show()
# In[]

Ifilt = gaussian(Igray,sigma = 2)
graficar(Ifilt)
histo(Igray)
histo(Ifilt)

graficar(Ifilt < 0.46)


# In[] Region properties



labeled_image = label(M_filled,connectivity=2)
regions = regionprops(labeled_image)
prop_list = ['area','bbox_area','convex_area','eccentricity','major_axis_length','minor_axis_length','perimeter']
imgs_props = np.zeros([len(regions),len(prop_list)],dtype=float)
p = []
ind = 0
for props in regions:
        p.append(props.area)
        p.append(props.bbox_area)
        p.append(props.convex_area)
        p.append(props.eccentricity)
        p.append(props.major_axis_length)
        p.append(props.minor_axis_length)
        p.append(props.perimeter)
        imgs_props[ind][:] = p
        p = []
        ind += 1
        
imgs_props = pd.DataFrame(imgs_props)        
#Obtener  el vector objetivo por medio
#de las mascaras coordenada xy y e intensidad

# In[]


def pozos(m_I,centro,r):
    h,w = m_I.shape
    I_new = np.zeros([h,w])#matriz blanca
    for i in range(0,h):
        for j in range(0,w):
            x = centro[:,0] - j
            y = centro[:,1] - i
            d  = np.sqrt(abs( np.square(x) + np.square(y) ))
            if any (d <= r):
                I_new[i,j] = 1
    return I_new


def graficar(I):
    plt.figure()
    plt.axis('off')
    plt.imshow(I,cmap='gray')
    plt.show()


def histo(I):
    plt.figure()
    plt.hist(I.ravel(), bins=2048, range=(0.0,1.0), fc='k', ec='k')
    plt.title('Escala de grises')

