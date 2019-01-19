# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 19:38:48 2018

@author: Nicolás
"""
# In[]

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from scipy.spatial.distance import cdist
from sklearn import metrics
from skimage.io import imread
from skimage.color import rgb2gray, rgb2lab
import matplotlib.pyplot as plt
from scipy.misc import imsave

import numpy as np
import os

# In[Carga de los nombres de las imágenes]
gen = 'Imagenes/'
folder_ids = os.listdir(gen)
image_ids = list()#ID's de las imágenes
# Creacíon de una matriz que contenga todos los ids, 
# donde por cada fila hay 1 carpeta.
for i in range(0,len(folder_ids)):
    image_ids.insert(i, os.listdir(gen + folder_ids[i] + '/') )
# In[] All images in dataset
n_colors = 3

for folder in range(1,len(folder_ids)):# Para cada carpeta
    for image in range(1,len(image_ids[folder])):# Para cada imagen
        
        PATH = gen + folder_ids[folder] + '/' + image_ids[folder][image]
        I = imread(PATH)# ndarray
        I_gray = rgb2gray(I) 
        size = I.shape
        
        Ilab = rgb2lab(I,illuminant='D65',observer='2')
        # Feature matrix of cromatic planes
        #croma = # Cromatic planes a and b
        I_plane = np.reshape(Ilab[:,:,1:3],(size[0]*size[1],2))
        # Cluster the pixel intensities
        clt = KMeans(init = "k-means++",n_clusters = n_colors,n_init = 10)
        clt.fit(I_plane)
        y = clt.fit_predict(I_plane)#iimagendices de cada muestra
        # Label image result of clustering
        pixel_labels = np.reshape(clt.labels_,(size[0],size[1]))
        # Centers of each cluster
        centers = clt.cluster_centers_
        # Save the image
        for k in range(0,n_colors):
            color = np.copy(I)
            # Mask of each cluster
            mask = pixel_labels == k
            # Where false, make them black (0)
            color[~mask] = 0
            
            imsave('Resultados_kmeans/' + folder_ids[folder] + '/' + image_ids[folder][image] + '/' + 'Cluster'+ str(k) +'.jpg',color)
        
        
        # Plot the k-clusters and its centers
        plt.figure()
        plt.title("Clusters de color mediante K-means")
        plt.xlabel("Plano cromatico a")
        plt.ylabel("Plano cromatico b")
        plt.scatter(Ilab[:,:,1],Ilab[:,:,2],c=y)
        plt.scatter(clt.cluster_centers_[:,0],clt.cluster_centers_[:,1])
        plt.savefig('Resultados_kmeans/'+ folder_ids[folder] + '/' + image_ids[folder][image] + '/' + 'Clusters' + '.jpg')
# In[] Just for one image
PATH = gen + folder_ids[1] + '/' + image_ids[1][1]
I = imread(PATH)# ndarray
I_gray = rgb2gray(I)

plt.figure()
plt.axis('off')
plt.imshow(I)
# Number of clusters to be used
n_colors = 4
#Reshaping to a vector
size = I.shape
#I_plane = np.reshape(I,(size[0]*size[1],3))
# In[] Clustering with cromatic planes of L*a*b space
Ilab = rgb2lab(I,illuminant='D65',observer='2')
# Feature matrix of cromatic planes
#croma = # Cromatic planes a and b
I_plane = np.reshape(Ilab[:,:,1:3],(size[0]*size[1],2))
# Cluster the pixel intensities
clt = KMeans(init = "k-means++",n_clusters = n_colors,n_init = 10)
clt.fit(I_plane)
y = clt.fit_predict(I_plane)#iimagendices de cada muestra
# In[] Labeled 
plt.close('all')
plt.figure()
plt.axis('off')
plt.imshow(I)
# Label image result of clustering
pixel_labels = np.reshape(clt.labels_,(size[0],size[1]))
# Centers of each cluster
centers = clt.cluster_centers_
#marker = ['o', 's', 'D', 'v', '^', 'p', '*', '+']
# Show every cluster in the original RGB image
for k in range(0,n_colors):
    color = np.copy(I)
    # Mask of each cluster
    mask = pixel_labels == k
    # Where false, make them black (0)
    color[~mask] = 0
    plt.figure()
    plt.axis('off')
    plt.imshow(color)

# Plot the k-clusters and its centers
plt.figure()
plt.title("Clusters de color mediante K-means")
plt.xlabel("Plano cromatico a")
plt.ylabel("Plano cromatico b")
plt.scatter(Ilab[:,:,1],Ilab[:,:,2],c=y)
plt.scatter(clt.cluster_centers_[:,0],clt.cluster_centers_[:,1])
plt.show()
# In[] Elbow method for evaluating the best K
mean_distort = []
K = range(1,10)
# Cluster the pixel intensities
for k in K:
    clt = KMeans(init = "k-means++",n_clusters = k,n_init = 10)
    clt.fit(I_plane)
    mean_distort.append(sum(np.min(cdist(I_plane, clt.cluster_centers_, 'euclidean'),axis=1)) / I_plane.shape[0])
# Plot of the cost function vs K used         
plt.plot(K,mean_distort,'bx-')
plt.xlabel('K')
plt.ylabel('Distorsión promedio')
plt.title('Selección de K mediante el método del codo')
plt.show()
# In[] PCA ( Obj: reduce time of clustering and another methods)

# Each image corresponds to a feature vector (2D) of M*N dimension.
# PCA for represent the image in terms of their principal components

# Create matrix of vector of every image in the training set

pca = PCA(n_components=200)
I_plane = I_plane.astype('float32')
X_train_reduced = pca.fit_transform(np.transpose(I_plane))
# In[]


#imsave('Resultados_kmeans/' + folder_ids[0] + '/' + image_ids[0][0] + '/' + 'Resultadin.jpg',I)


plt.figure()
plt.axis('off')
plt.imshow(I)
plt.savefig('Resultados_kmeans/'+ folder_ids[0] + '/' + image_ids[0][0] + '/' + 'Cluster'+ str(0) +'.jpg')