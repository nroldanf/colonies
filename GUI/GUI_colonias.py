# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_colonias.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!


from clase_Colonias import Colonias
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import os
from skimage.io import imread
from scipy.misc import imsave


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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Conteo de Colonias LIMANI"))
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
        imsave('resultado.jpg',self.I.Closing())
        
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
