# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_coloniasDef.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(986, 708)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setSizeGripEnabled(False)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(60, 90, 421, 121))
        self.groupBox_3.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.cbFolders = QtWidgets.QComboBox(self.groupBox_3)
        self.cbFolders.setGeometry(QtCore.QRect(40, 50, 350, 22))
        self.cbFolders.setObjectName("cbFolders")
        self.lblFolder = QtWidgets.QLabel(self.groupBox_3)
        self.lblFolder.setGeometry(QtCore.QRect(40, 20, 141, 21))
        self.lblFolder.setObjectName("lblFolder")
        self.lblLogo1 = QtWidgets.QLabel(Dialog)
        self.lblLogo1.setGeometry(QtCore.QRect(30, 10, 201, 61))
        self.lblLogo1.setText("")
        self.lblLogo1.setObjectName("lblLogo1")
        self.lblLogo2 = QtWidgets.QLabel(Dialog)
        self.lblLogo2.setGeometry(QtCore.QRect(870, 10, 81, 61))
        self.lblLogo2.setText("")
        self.lblLogo2.setObjectName("lblLogo2")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(60, 220, 421, 431))
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
        self.lblFolder_2 = QtWidgets.QLabel(self.groupBox_4)
        self.lblFolder_2.setGeometry(QtCore.QRect(40, 10, 141, 21))
        self.lblFolder_2.setObjectName("lblFolder_2")
        self.groupBox_5 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_5.setGeometry(QtCore.QRect(500, 220, 421, 431))
        self.groupBox_5.setStyleSheet("border-color: rgb(207, 207, 207);\n"
"")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.listImags2 = QtWidgets.QListWidget(self.groupBox_5)
        self.listImags2.setGeometry(QtCore.QRect(40, 50, 351, 351))
        self.listImags2.setDragDropOverwriteMode(False)
        self.listImags2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listImags2.setObjectName("listImags2")
        self.lblFolder_3 = QtWidgets.QLabel(self.groupBox_5)
        self.lblFolder_3.setGeometry(QtCore.QRect(40, 10, 141, 21))
        self.lblFolder_3.setObjectName("lblFolder_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(500, 90, 421, 121))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnLoad = QtWidgets.QPushButton(self.groupBox_2)
        self.btnLoad.setGeometry(QtCore.QRect(150, 20, 121, 31))
        self.btnLoad.setObjectName("btnLoad")
        self.btnProcess = QtWidgets.QPushButton(self.groupBox_2)
        self.btnProcess.setGeometry(QtCore.QRect(20, 60, 121, 31))
        self.btnProcess.setObjectName("btnProcess")
        self.btnRoot = QtWidgets.QPushButton(self.groupBox_2)
        self.btnRoot.setGeometry(QtCore.QRect(20, 20, 121, 31))
        self.btnRoot.setObjectName("btnRoot")
        self.btnDisplay = QtWidgets.QPushButton(self.groupBox_2)
        self.btnDisplay.setGeometry(QtCore.QRect(150, 60, 121, 31))
        self.btnDisplay.setObjectName("btnDisplay")
        self.btnAdd = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAdd.setGeometry(QtCore.QRect(360, 60, 51, 31))
        self.btnAdd.setObjectName("btnAdd")
        self.btnRemove = QtWidgets.QPushButton(self.groupBox_2)
        self.btnRemove.setGeometry(QtCore.QRect(290, 60, 51, 31))
        self.btnRemove.setObjectName("btnRemove")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ColonyCounter2001XD"))
        self.lblFolder.setText(_translate("Dialog", "Selección de carpeta"))
        self.lblFolder_2.setText(_translate("Dialog", "Imágenes disponibles"))
        self.lblFolder_3.setText(_translate("Dialog", "Imágenes seleccionadas"))
        self.btnLoad.setText(_translate("Dialog", "Cargar imágenes"))
        self.btnProcess.setText(_translate("Dialog", "Procesar imágenes"))
        self.btnRoot.setText(_translate("Dialog", "Seleccionar ubicación"))
        self.btnDisplay.setText(_translate("Dialog", "Ver imágenes"))
        self.btnAdd.setText(_translate("Dialog", ">>"))
        self.btnRemove.setText(_translate("Dialog", "<<"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

