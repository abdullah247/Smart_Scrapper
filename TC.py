# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ABDULLAH\Desktop\FreeLancing\Fiver\Fiver Python\Fiver_Eric_Full_Scrapper\TurfClub.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TurfClub(object):
    def setupUi(self, TurfClub):
        TurfClub.setObjectName("TurfClub")
        TurfClub.resize(685, 478)
        self.pushButton = QtWidgets.QPushButton(TurfClub)
        self.pushButton.setGeometry(QtCore.QRect(160, 170, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(TurfClub)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 260, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(TurfClub)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 330, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(TurfClub)
        QtCore.QMetaObject.connectSlotsByName(TurfClub)

    def retranslateUi(self, TurfClub):
        _translate = QtCore.QCoreApplication.translate
        TurfClub.setWindowTitle(_translate("TurfClub", "Form"))
        self.pushButton.setText(_translate("TurfClub", "PushButton"))
        self.pushButton_2.setText(_translate("TurfClub", "PushButton"))
        self.pushButton_3.setText(_translate("TurfClub", "PushButton"))
