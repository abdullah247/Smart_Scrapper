# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ABDULLAH\Desktop\FreeLancing\Fiver\Fiver Python\Fiver_Eric_Full_Scrapper\SmartScrapper.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(912, 639)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
"border: none;\n"
"background-color: transparent; \n"
"color: #fff;\n"
"}\n"
"#centralwidget{\n"
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
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QFrame(self.centralwidget)
        self.header.setMinimumSize(QtCore.QSize(0, 50))
        self.header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.header)
        self.frame_4.setMinimumSize(QtCore.QSize(100, 0))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.menu = QtWidgets.QPushButton(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMaximumSize(QtCore.QSize(150, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/Icons.qrc/align-justify.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu.setIcon(icon)
        self.menu.setIconSize(QtCore.QSize(24, 24))
        self.menu.setObjectName("menu")
        self.horizontalLayout_3.addWidget(self.menu)
        self.horizontalLayout_2.addWidget(self.frame_4, 0, QtCore.Qt.AlignLeft)
        self.frame = QtWidgets.QFrame(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.header, 0, QtCore.Qt.AlignTop)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sideBar = QtWidgets.QFrame(self.frame_2)
        self.sideBar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sideBar.sizePolicy().hasHeightForWidth())
        self.sideBar.setSizePolicy(sizePolicy)
        self.sideBar.setMinimumSize(QtCore.QSize(0, 300))
        self.sideBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sideBar.setObjectName("sideBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sideBar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GrouppedButtons = QtWidgets.QFrame(self.sideBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GrouppedButtons.sizePolicy().hasHeightForWidth())
        self.GrouppedButtons.setSizePolicy(sizePolicy)
        self.GrouppedButtons.setMinimumSize(QtCore.QSize(0, 100))
        self.GrouppedButtons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GrouppedButtons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GrouppedButtons.setObjectName("GrouppedButtons")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.GrouppedButtons)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hk = QtWidgets.QPushButton(self.GrouppedButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hk.sizePolicy().hasHeightForWidth())
        self.hk.setSizePolicy(sizePolicy)
        self.hk.setMinimumSize(QtCore.QSize(0, 30))
        self.hk.setObjectName("hk")
        self.verticalLayout_3.addWidget(self.hk, 0, QtCore.Qt.AlignTop)
        self.tc = QtWidgets.QPushButton(self.GrouppedButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tc.sizePolicy().hasHeightForWidth())
        self.tc.setSizePolicy(sizePolicy)
        self.tc.setMinimumSize(QtCore.QSize(0, 30))
        self.tc.setObjectName("tc")
        self.verticalLayout_3.addWidget(self.tc, 0, QtCore.Qt.AlignTop)
        self.sc = QtWidgets.QPushButton(self.GrouppedButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sc.sizePolicy().hasHeightForWidth())
        self.sc.setSizePolicy(sizePolicy)
        self.sc.setMinimumSize(QtCore.QSize(0, 30))
        self.sc.setObjectName("sc")
        self.verticalLayout_3.addWidget(self.sc, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_2.addWidget(self.GrouppedButtons, 0, QtCore.Qt.AlignTop)
        self.frame_3 = QtWidgets.QFrame(self.sideBar)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.settings = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings.sizePolicy().hasHeightForWidth())
        self.settings.setSizePolicy(sizePolicy)
        self.settings.setMaximumSize(QtCore.QSize(16777215, 100))
        self.settings.setStyleSheet("color:white;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/settings.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings.setIcon(icon1)
        self.settings.setIconSize(QtCore.QSize(24, 24))
        self.settings.setObjectName("settings")
        self.horizontalLayout_5.addWidget(self.settings, 0, QtCore.Qt.AlignLeft)
        self.quit = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quit.sizePolicy().hasHeightForWidth())
        self.quit.setSizePolicy(sizePolicy)
        self.quit.setMaximumSize(QtCore.QSize(16777215, 100))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quit.setIcon(icon2)
        self.quit.setIconSize(QtCore.QSize(24, 24))
        self.quit.setObjectName("quit")
        self.horizontalLayout_5.addWidget(self.quit)
        self.verticalLayout_2.addWidget(self.frame_3, 0, QtCore.Qt.AlignBottom)
        self.horizontalLayout.addWidget(self.sideBar)
        self.body = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Source Serif Pro")
        font.setPointSize(10)
        self.body.setFont(font)
        self.body.setObjectName("body")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.body)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro")
        font.setPointSize(32)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.body)
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Scrapper"))
        self.menu.setText(_translate("MainWindow", "Menu"))
        self.label.setText(_translate("MainWindow", "Smart Scrapper"))
        self.hk.setText(_translate("MainWindow", "Hong Kong"))
        self.tc.setText(_translate("MainWindow", "TurfClub"))
        self.sc.setText(_translate("MainWindow", "SCMP"))
        self.settings.setText(_translate("MainWindow", "Settings"))
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.label_2.setText(_translate("MainWindow", "Welcome !"))
import icons_rc