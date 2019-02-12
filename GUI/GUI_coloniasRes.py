# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_coloniasRes.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog2(object):
    def setupUi2(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(986, 675)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")
        Dialog.setSizeGripEnabled(False)
        Dialog.setWindowIcon(QtGui.QIcon('Logos/if_Microscope_379436.png'))
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 490, 661, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox_3)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 20, 641, 91))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 639, 89))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
#        QtWidgets.QTableWidget
        self.tableRes = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.tableRes.setGeometry(QtCore.QRect(10, 10, 621, 71))
        self.tableRes.setObjectName("tableRes")

        self.tableRes.setRowCount(10)
        self.tableRes.setColumnCount(2)
        
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 661, 461))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lblImRes = QtWidgets.QLabel(self.groupBox)
        self.lblImRes.setGeometry(QtCore.QRect(10, 10, 639, 369))
        self.lblImRes.setText("")
        self.lblImRes.setObjectName("lblImRes")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 400, 641, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.btnR = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.btnR.setObjectName("btnR")
        self.btnR.clicked.connect(self.addContent)
        self.btnR.clicked.connect(self.display)
        self.horizontalLayout_3.addWidget(self.btnR)
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ColonyCounter2001XD"))
        self.groupBox_3.setTitle(_translate("Dialog", "Resultados"))
        self.pushButton_3.setText(_translate("Dialog", "<<"))
        self.btnR.setText(_translate("Dialog", ">>"))

    def addContent(self):
#        Recibirá como entrada un diccionario con el conteo
        cont = {'Pozo 1':1,'Pozo 2':3,'Pozo 3':5,'Pozo 4':5,'Pozo 5':12,'Pozo 6':15}
        row = 0
        for key,value in cont.items():
            col = 0
            item=QtWidgets.QTableWidgetItem(key)
            self.tableRes.setItem(row,col,item)
            col += 1
            item=QtWidgets.QTableWidgetItem(str(value) + 'colonias')
            self.tableRes.setItem(row,col,item)
            row += 1

    def display(self):
        self.pixmap = QtGui.QPixmap('Final.jpg')
        self.lblImRes.setPixmap(self.pixmap)
        self.lblImRes.setScaledContents(True)
        
        
        
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog2()
    ui.setupUi2(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

