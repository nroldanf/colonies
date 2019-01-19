# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_colonias.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!


from clase import Colonias
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import os
from skimage.io import imread
from scipy.misc import imsave
from skimage.measure import label
from skimage.color import label2rgb

import numpy as np


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        
        
        # Contador de seleccion dde carpeta
        self.cont_load = 0
        # Contador de la barra de progreso
        self.cont_prog = 0
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
        Dialog.setWindowIcon(QtGui.QIcon('if_Microscope_379436.png'))
        
        
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(70, 90, 551, 461))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lblImage = QtWidgets.QLabel(self.groupBox)
        self.lblImage.setGeometry(QtCore.QRect(30, 30, 501, 361))
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(70, 580, 551, 71))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnLoad = QtWidgets.QPushButton(self.groupBox_2)
        self.btnLoad.setGeometry(QtCore.QRect(150, 20, 101, 31))
        self.btnLoad.setObjectName("btnLoad")
        
        self.btnLoad.clicked.connect(self.loadImage)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 20, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update)
        
        
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(220, 220, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        
        self.progressBar.setVisible(False)
        
        
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(660, 90, 411, 151))
        self.groupBox_3.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.cbFolders = QtWidgets.QComboBox(self.groupBox_3)
        self.cbFolders.setGeometry(QtCore.QRect(30, 30, 350, 22))
        self.cbFolders.setObjectName("cbFolders")
        # Añade los nombres de los folders disponibles
        self.cbFolders.addItems(self.folder_ids)
        # Al seleccionar una de ellas se cargan los nombres al comboBox
        self.cbFolders.activated.connect(self.loadImageNames)

        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 90, 350, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        
        self.comboBox_2.addItems(self.image_ids[self.cont_load])
        
        
        self.lblLogo1 = QtWidgets.QLabel(Dialog)
        self.lblLogo1.setGeometry(QtCore.QRect(30, 10, 201, 51))
        self.lblLogo1.setText("")
        self.lblLogo1.setObjectName("lblLogo1")
        self.pixmap = QPixmap('ESCUELA.jpg')
        self.lblLogo1.setPixmap(self.pixmap)
        self.lblLogo1.setScaledContents(True)
        
        
        self.lblLogo2 = QtWidgets.QLabel(Dialog)
        self.lblLogo2.setGeometry(QtCore.QRect(1010, 10, 81, 61))
        self.lblLogo2.setText("")
        self.lblLogo2.setObjectName("lblLogo2")
        self.pixmap = QPixmap('PROMISE.png')
        self.lblLogo2.setPixmap(self.pixmap)
        self.lblLogo2.setScaledContents(True)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ColonyCounter2001XD"))
        self.btnLoad.setText(_translate("Dialog", "Cargar imagen"))
        self.pushButton_2.setText(_translate("Dialog", "Procesar imagen"))
        
    def loadImageNames(self):
        if self.cont_load > 0:
            self.comboBox_2.clear()
        self.comboBox_2.addItems(self.image_ids[self.cbFolders.currentIndex()])
        self.cont_load += 1
        
    def loadImage(self):        
        # PATH de la imagen
        PATH = self.gen + self.folder_ids[self.cbFolders.currentIndex()] + '/'+ self.image_ids[self.cbFolders.currentIndex()][self.comboBox_2.currentIndex()]
        # Instancia de la clase_Colonias
        self.I = Colonias(imread(PATH))
        self.pixmap = QPixmap(PATH)
        self.lblImage.setPixmap(self.pixmap)
        self.lblImage.setScaledContents(True)
        
    def update(self):
        self.lblImage.setVisible(False)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(self.cont_prog)
        
        I_gray = self.I.mejoraConstraste()
        centros = self.I.corr2d()
        m_BW = np.zeros([self.I.shape[0],self.I.shape[1]])#Imagen negra de la misma dimensión
        self.cont_prog += 5
        self.progressBar.setValue(self.cont_prog)
        
        for k in range(0,len(centros)):
#            # Seccionamiento de 1 pozo
            I_seg = self.I.pozo(centros[k],I_gray)
#            # Otsu por pozo
            I_otsu = self.I.otsu(I_seg,I_gray,centros[k])
#            # Mascara color para los bordes
            I_color = self.I.color(I_gray,centros[k])
#            # Aplicación de las propiedades de region
            I_props = self.I.reg_seg(I_otsu*I_color)
#            # Etiquetado y conteo de las colonias
#            # 8-conectividad, fondo negro
#            labeled,num = label(
#                I_props, neighbors=8, background=0,
#                return_num=True
#            )
##            # Guarda el conteo por pozo en un diccionario
##            dic[ list(dic.keys())[k] ].append(num)
#            # Suma el resultado del pozo a una imagen negra (ceros)
            m_BW = m_BW + I_props
            self.cont_prog += 30
            self.progressBar.setValue(self.cont_prog)
#            
#        labeled = label(m_BW, neighbors=8, background=0)
#        labeled_RGB = label2rgb(labeled, image=self.image)#image = imagen original
        
        self.cont_prog += 5
        self.progressBar.setValue(self.cont_prog)
        self.progressBar.setVisible(False)
        self.cont_prog = 0
        self.lblImage.setVisible(True)
        
        imsave('resultado.jpg',m_BW)
        self.pixmap = QPixmap('resultado.jpg')
        self.lblImage.setPixmap(self.pixmap)
        self.lblImage.setScaledContents(True)
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
