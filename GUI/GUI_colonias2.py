# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 11:57:30 2019

@author: Nicol
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_colonias.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import os
import matplotlib.pyplot as plt
from skimage.io import imread
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        
        # Contador de seleccion dde carpeta
        self.cont_load = 0
        # Cargar nombres de carpetas
        self.gen = 'Imagenes/'
        self.folder_ids = os.listdir(self.gen)
        self.image_ids = list()#ID's de las imágenes
        # Creacíon de una matriz que contenga todos los ids, 
        # donde por cada fila hay 1 carpeta.
        for i in range(0,len(self.folder_ids)):
            self.image_ids.insert(i, os.listdir(self.gen + self.folder_ids[i] + '/') )
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(1124, 901)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(480, 210, 641, 71))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnLoad = QtWidgets.QPushButton(self.groupBox_2)
        self.btnLoad.setGeometry(QtCore.QRect(210, 20, 121, 31))
        self.btnLoad.setObjectName("btnLoad")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 20, 121, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.btnFolder = QtWidgets.QPushButton(self.groupBox_2)
        self.btnFolder.setGeometry(QtCore.QRect(80, 20, 121, 31))
        self.btnFolder.setObjectName("btnFolder")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(460, 20, 111, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.viewImages)
        
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(60, 90, 421, 201))
        self.groupBox_3.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.cbFolders = QtWidgets.QComboBox(self.groupBox_3)
        self.cbFolders.setGeometry(QtCore.QRect(40, 60, 350, 22))
        self.cbFolders.setObjectName("cbFolders")
        # Añada fila correspondiente a seleccionar todas
        
        # Añade los nombres de los folders disponibles
        self.cbFolders.addItems(self.folder_ids)
        # Añadir los nombres de las imagenes disponibles al List widget
        self.cbFolders.activated.connect(self.loadImageNames)
        
        
        
        self.lblFolder = QtWidgets.QLabel(self.groupBox_3)
        self.lblFolder.setGeometry(QtCore.QRect(40, 30, 141, 21))
        self.lblFolder.setObjectName("lblFolder")
        
        self.lblLogo1 = QtWidgets.QLabel(Dialog)
        self.lblLogo1.setGeometry(QtCore.QRect(30, 10, 201, 51))
        self.lblLogo1.setText("")
        self.lblLogo1.setObjectName("lblLogo1")
        self.lblLogo2 = QtWidgets.QLabel(Dialog)
        self.lblLogo2.setGeometry(QtCore.QRect(1010, 10, 81, 61))
        self.lblLogo2.setText("")
        self.lblLogo2.setObjectName("lblLogo2")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(60, 320, 421, 431))
        self.groupBox_4.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.listImags = QtWidgets.QListWidget(self.groupBox_4)
        self.listImags.setGeometry(QtCore.QRect(40, 50, 351, 351))
        self.listImags.setDragEnabled(False)
        self.listImags.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listImags.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listImags.setObjectName("listImags")
#        self.listImags.selectionMode()
        
        self.lblFolder_2 = QtWidgets.QLabel(self.groupBox_4)
        self.lblFolder_2.setGeometry(QtCore.QRect(20, 10, 141, 21))
        self.lblFolder_2.setObjectName("lblFolder_2")
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_5.setGeometry(QtCore.QRect(510, 320, 421, 431))
        self.groupBox_5.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.listImags_2 = QtWidgets.QListWidget(self.groupBox_5)
        self.listImags_2.setGeometry(QtCore.QRect(40, 50, 351, 351))
        self.listImags_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listImags_2.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listImags_2.setObjectName("listImags_2")
        self.lblFolder_3 = QtWidgets.QLabel(self.groupBox_5)
        self.lblFolder_3.setGeometry(QtCore.QRect(20, 10, 141, 21))
        self.lblFolder_3.setObjectName("lblFolder_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Conteo de Colonias LIMANI"))
        self.btnLoad.setText(_translate("Dialog", "Cargar imágenes"))
        self.pushButton_2.setText(_translate("Dialog", "Procesar imágenes"))
        self.btnFolder.setText(_translate("Dialog", "Seleccionar ubicación"))
        self.pushButton_3.setText(_translate("Dialog", "Ver imágenes"))
        self.lblFolder.setText(_translate("Dialog", "Selección de carpeta"))

        self.lblFolder_2.setText(_translate("Dialog", "Imágenes"))
        self.lblFolder_3.setText(_translate("Dialog", "Imágenes seleccionadas"))

    def loadImageNames(self):
        if self.cont_load > 0:
            self.listImags.clear()
        self.listImags.addItems(self.image_ids[self.cbFolders.currentIndex()])
        self.cont_load += 1
        
# View selected images
    def viewImages(self):
        # Para cada imagen seleccionada, repita
        print(self.listImags_2.count())
        items = []
        for index in range(0,self.listImags_2.count()):
            items.append(self.listImags_2.item(index).text())
        # PATH absoluto de la imagen
        PATH = self.gen + self.folder_ids[self.cbFolders.currentIndex()] + '/'+ self.image_ids[self.cbFolders.currentIndex()][0]
        # Load image
        I = imread(PATH)
        # Muestre la imagen en un externo de matplotlib
        plt.close('all')
        plt.figure()
        plt.axis('off')
        plt.title(self.image_ids[self.cbFolders.currentIndex()][0])
        plt.imshow(I)
        plt.show()
# WIth button rather than with dragDrop feature
#    def addImages(self):
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

