# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ABDULLAH\Desktop\FreeLancing\Fiver\Fiver Python\Fiver_Eric_Full_Scrapper\Settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(685, 478)
        Settings.setStyleSheet("*{\n"
"border: none;\n"
"background-color: transparent; \n"
"color: #fff;\n"
"}\n"
"#Settings{\n"
"background-color: #040f13;\n"
"}\n"
"\n"
".active{\n"
"     background-color: #007bff;\n"
"}\n"
"\n"
"#sidebar{\n"
"background-color: #071e26;\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton{\n"
"padding: 10px;\n"
"background-color: #040f13;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
" QPushButton:hover {\n"
"            background-color: #007bff;\n"
"  }\n"
"\n"
"#body{\n"
"background-color: #071e26;\n"
"border-radius: 10px;\n"
"}")
        self.label = QtWidgets.QLabel(Settings)
        self.label.setGeometry(QtCore.QRect(170, 140, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Settings)
        self.label_2.setGeometry(QtCore.QRect(170, 220, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Settings)
        self.label_3.setGeometry(QtCore.QRect(180, 320, 47, 13))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.label.setText(_translate("Settings", "TextLabel"))
        self.label_2.setText(_translate("Settings", "TextLabel"))
        self.label_3.setText(_translate("Settings", "TextLabel"))