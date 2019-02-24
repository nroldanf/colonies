# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_coloniasFin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from skimage.io import imread
import os
from GUI_coloniasRes import *
from clase import *
from scipy.misc import imsave
import datetime
import time
import pandas as pd
import numpy as np
from threading import Thread


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # *** Inicialización de variables de clase ***
#        self.PATH = ""
#        self.folder_ids = []
        self.images_PATH = []
        self.images = []
        self.cont = [0,0]
        self.conteo = []
        self.timing = []
        # *** Interfaz ***
        Dialog.setObjectName("Dialog")
        Dialog.resize(986, 675)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setSizeGripEnabled(False)
        Dialog.setWindowIcon(QtGui.QIcon('Logos/if_Microscope_379436.png'))
        self.lblLogo1 = QtWidgets.QLabel(Dialog)
        self.lblLogo1.setGeometry(QtCore.QRect(20, 20, 201, 51))
        self.lblLogo1.setText("")
        self.lblLogo1.setObjectName("lblLogo1")
        self.pixmap = QtGui.QPixmap('Logos/ESCUELA.jpg')
        self.lblLogo1.setPixmap(self.pixmap)
        self.lblLogo1.setScaledContents(True)
        self.lblLogo2 = QtWidgets.QLabel(Dialog)
        self.lblLogo2.setGeometry(QtCore.QRect(880, 20, 81, 61))
        self.lblLogo2.setText("")
        self.lblLogo2.setObjectName("lblLogo2")
        self.pixmap = QtGui.QPixmap('Logos/PROMISE.png')
        self.lblLogo2.setPixmap(self.pixmap)
        self.lblLogo2.setScaledContents(True)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 90, 661, 411))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lblImage = QtWidgets.QLabel(self.groupBox)
        self.lblImage.setGeometry(QtCore.QRect(10, 10, 639, 389))
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        # Imagen inicial en la interfaz
        self.pixmap = QtGui.QPixmap("Logos/rembrandt.jpg")
        self.lblImage.setPixmap(self.pixmap)
        self.lblImage.setScaledContents(True)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(280, 200, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.progressBar.setValue(self.cont[1])
        
        self.lblProcess = QtWidgets.QLabel(self.groupBox)
        self.lblProcess.setGeometry(QtCore.QRect(280, 180, 81, 16))
        self.lblProcess.setObjectName("lblProcess")
        self.lblProcess.setVisible(False)
        
        self.btnViewRes = QtWidgets.QPushButton(self.groupBox)
        self.btnViewRes.setGeometry(QtCore.QRect(280, 230, 91, 23))
        self.btnViewRes.setObjectName("btnViewRes")
        self.btnViewRes.clicked.connect(self.openRes)
        self.btnViewRes.setVisible(False)
        
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(690, 510, 271, 151))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 251, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnRoot = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnRoot.setObjectName("btnRoot")
        self.btnRoot.clicked.connect(self.getImages)
        self.gridLayout.addWidget(self.btnRoot, 0, 0, 1, 1)
        self.btnLoad = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnLoad.setObjectName("btnLoad")
        self.btnLoad.clicked.connect(self.viewImage)
        self.gridLayout.addWidget(self.btnLoad, 0, 1, 1, 1)
        
        self.btnLimpiar = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnLimpiar.setObjectName("btnLimpiar")
        self.gridLayout.addWidget(self.btnLimpiar,1, 1, 1, 1)
        self.btnLimpiar.clicked.connect(self.limpiar)
        
        
        self.btnProcess = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnProcess.setObjectName("btnProcess")
        self.btnProcess.setIcon(QtGui.QIcon('Logos/micro'))
        self.btnProcess.setIconSize(QtCore.QSize(24,24))
        self.btnProcess.clicked.connect(self.threadOne)
        
        self.gridLayout.addWidget(self.btnProcess, 1, 0, 1, 1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 110, 251, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnRemove = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnRemove.setObjectName("btnRemove")
        self.btnRemove.clicked.connect(self.left)
        self.horizontalLayout_2.addWidget(self.btnRemove)
        self.btnAdd = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.clicked.connect(self.right)
        self.horizontalLayout_2.addWidget(self.btnAdd)
        
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 510, 661, 151))
        self.groupBox_4.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.lblFolder_2 = QtWidgets.QLabel(self.groupBox_4)
        self.lblFolder_2.setGeometry(QtCore.QRect(10, 1, 141, 20))
        self.lblFolder_2.setObjectName("lblFolder_2")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_4)
        self.scrollArea.setGeometry(QtCore.QRect(10, 20, 641, 121))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 639, 119))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.listImags = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listImags.setGeometry(QtCore.QRect(10, 10, 621, 101))
        self.listImags.setDragEnabled(False)
#        self.listImags.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
#        self.listImags.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listImags.setObjectName("listImags")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ColonyCounter2001XD"))
        self.lblProcess.setText(_translate("Dialog", "Procesando..."))
        self.btnRoot.setText(_translate("Dialog", "Seleccionar imágenes"))
        self.btnLoad.setText(_translate("Dialog", "Previsualizar"))
        self.btnProcess.setText(_translate("Dialog", "Procesar imágenes"))
        self.btnLimpiar.setText(_translate("Dialog", "Limpiar"))
        self.btnRemove.setText(_translate("Dialog", "<<"))
        self.btnAdd.setText(_translate("Dialog", ">>"))
        self.btnViewRes.setText(_translate("Dialog", "Ver Resultados"))
        self.lblFolder_2.setText(_translate("Dialog", "Imágenes seleccionadas: " + str( len(self.images)) ))

    #Métodos asociados
    
    # Abrir nueva ventana para visualizar resultados
    def openRes(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog2()
        self.ui.setupUi2(self.window)
        self.window.show()

    # Abrir ventana de dialogo para seleccionar y mostrar los nombres en 
    # el list widget
    def getImages(self):
        self.limpiar()
        temp = QtWidgets.QFileDialog.getOpenFileNames()
        cont = 0
        for name in temp[0]:
            names = name.split('/')#separe la cadena
            # El último corresponde al nombre del archivo
            if not names[-1] in self.images:# Si el archivo ya fue agregado
                self.images.append(names[-1])
                self.images_PATH.append(temp[0][cont])                
            cont+=1
        self.listImags.clear()
        self.listImags.addItems(self.images)
        self.lblFolder_2.setText("Imágenes seleccionadas: " + str( len(self.images)) )
            
    # Limpia la listwidget y la lista de nombres de imágenes y de los PATHs
    def limpiar(self):
        self.images_PATH.clear()
        self.images.clear()
        self.listImags.clear()
        self.timing.clear()
        
        # 0 imágenes seleccionadas
        self.lblFolder_2.setText("Imágenes seleccionadas: " + str( len(self.images)) )
        # Limpie el label donde se muestra la imagen
        self.pixmap = QtGui.QPixmap("Logos/rembrandt.jpg")
        self.lblImage.setPixmap(self.pixmap)
        self.btnViewRes.setVisible(False)
        
    #Visualiza la imagen actual en el label
    def viewImage(self,num=0):
        try:
            self.pixmap = QtGui.QPixmap(self.images_PATH[num])
            self.lblImage.setPixmap(self.pixmap)
#            self.lblImage.setScaledContents(True)
        except:
            print("Debe seleccionar por lo menos una imagen.")
        
    # Incrementa el contador para visualizar la siguiente imagen en la lista
    def right(self):
        # si el contador es menor a la longitud de la lista de imágenes
        if self.cont[0] < len(self.images_PATH)-1:
            self.cont[0] += 1
        self.viewImage(self.cont[0])
    
    # Decrementa el contador para visualizar la siguiente imagen
    def left(self):
        if self.cont[0] > 0:
            self.cont[0] -= 1
        self.viewImage(self.cont[0])
        
    # Procesa una imagen
    def processOne(self,PATH,name,index):
        nameMono = name +'/'+ self.images[index]# Imagen BW
        nameColor = name + '/' + 'color_' + self.images[index]# Imagen pseudo
        start = time.time()# Para contar cuanto se demora
        I = imread(PATH)
        I_cla = Colonias(I)# Cree objeto
        Res,conteo,color = I_cla.processing()# Procese la imagen
        self.timing.append(time.time()-start)
        imsave(nameMono.replace('.jpg','.tiff'),Res)# Guarde la imagen BW
        imsave(nameColor.replace('.jpg','.tiff'),color)# Guarde la imagen pseudocolor
        print(self.timing)
        self.conteo.append(conteo)# Concatena a una matriz
        
        self.cont[1] += 1
        
    
    def processAll(self):
        self.threadTwo()
        # Reinicie la lista con las imágenes
        # Cree el directorio general para todos los resultados del programa 
        ansPath = 'Resultados_GUI'
        try:
            os.makedirs(ansPath)
        except:
            print('El directorio ya existe.')
            # REEMPLAZAR POR MENSAJE
        
        # Crea el directorio para las imágenes seleccionadas
        now = datetime.datetime.now()
        ansPath = 'Resultados_GUI/' + now.strftime("%Y-%m-%d")
        try:
            os.makedirs(ansPath)
        except:
            print('El directorio ya existe.')
        
        print('Comencé')# BARRA DE CARGA 
        # Procesamiento de cada una de las imágenes
        for i in range(0,len(self.images_PATH)):
            print(self.images[i])
            self.processOne(self.images_PATH[i],ansPath,i)
        
        # Guarda el conteo en un archivo excel al terminar
        df = pd.DataFrame(self.conteo,index=self.images)
        with pd.ExcelWriter('Resultados_GUI/'+ now.strftime("%Y-%m-%d") + '.xlsx') as writer:
            df.to_excel(writer, sheet_name='05.04.2016')


    # Método para incrementar barra de tareas
    def loadBar(self):
        # Haga invisible el label y visible la barra de progreso
        self.lblProcess.setVisible(True)
        self.progressBar.setVisible(True)
        self.lblImage.setVisible(False)
        #Deshabilite los botones mientras está procesando
        self.btnProcess.setEnabled(False)
        self.btnRoot.setEnabled(False)
        self.btnLoad.setEnabled(False)
        self.btnViewRes.setEnabled(False)
        self.btnLimpiar.setEnabled(False)
        
        while self.cont[1]/len(self.images) < 1:
            time.sleep(1)# necesario para que vaya a ejecutar otros hilos
            self.progressBar.setValue( np.around( (self.cont[1]/len(self.images))*100 ) )
        
        # Haga visible el label e invisible la barra de progreso
        self.progressBar.setVisible(False)        
        self.lblProcess.setVisible(False)
        self.lblImage.setVisible(True)
        self.pixmap = QtGui.QPixmap("Logos/picasso.jpg")
        self.lblImage.setPixmap(self.pixmap)
        # Habilite de nuevo los botones
        self.btnProcess.setEnabled(True)
        self.btnRoot.setEnabled(True)
        self.btnLoad.setEnabled(True)
        self.btnViewRes.setEnabled(True)
        self.btnLimpiar.setEnabled(True)
        self.btnViewRes.setVisible(True)
        
        self.cont[1] = 0

        
    # Hilo para el procesamiento de las imágenes
    def threadOne(self):
        self.run_thread = Thread(target=self.processAll)
        self.run_thread.start() # start the thread
        
    # Hilo para la barra de carga
    def threadTwo(self):
        self.run_thread = Thread(target=self.loadBar)
        self.run_thread.start() # start the thread
    
    
        
#            for i in range(0,len(self.conteo)):
#                self.conteo[i].to_excel(writer,sheet_name='05.04.2016')    
#**********COSAS A HACER*************
    '''
    -Agregar opción de remover los archivos escogidos por la persona(BTN)
    -Reconocer cuando la persona ya ha seleccionado una imagen (falta agregar un posible mensaje de alerta)
    Para ahorrar espacio, incluir una barra de herramientas con estas opciones
    *Ideas*
    -Si una imagen es seleccionada (solo se puede seleccionar una)
    que se visualice 
    ó
    - Destinar un espacio para mostrar el conteo(tipo tabla o en la misma interfaz o ambas):
        Tener la posibilidad de visualizarlo en la misma interfaz
        o exportarlo como archivo de excel.
    - Visualizar resultados desde memoria ?
    - Opción de previsualizar imágenes en la GUI principal (abrir otra ventana)
    - Opción de ver resultados (abrir otra ventana)
    - Opción de guardar conteo como archivo de excel o .csv e imágenes
    en determinado formato
    - No tener en cuenta aquellos pozos que se encuentren recortados (Reportarlo)
    - Agregar la posibilidad de que la persona pueda agregar aquellas
    colonias que no fueron detectadas mediante el algoritmo haciendo
    una selección de la región o del pixel (semilla) y efectuando
    region growing.
    - Opción de acercamiento
    
    '''
    #***********************************

    

#class myThread(threading.Thread,Ui_Dialog):#HERENCIA
#    def __init__(self,proc):
#        threading.Thread.__init__(self)
#        self.w = proc
#        self.count = 0
#    def run(self):
#        proc.processAll(self)
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

