
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QMainWindow, QDialog, QPushButton, \
    QLineEdit, QLabel, QRadioButton
from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys

from BakupCreation import CreateBackup
from HongKong.Barrier_Result import hkGetBarrierResult
from HongKong.FixGear import hkFixGear
from HongKong.Main_HandiCap_Populate import hkHandiCap
from HongKong.Main_Populate_Class import HkPopulateClass
from HongKong.New_Html_Solver_For_Latest import HkHtmlSolver
from HongKong.addRtg import FixRtg
from HongKong.customApi import ScrapLatest
from SCMP.SCMP_PawTime import getSCMPPAWTIME
from SCMP.ScmpScrapper import SCARP_SCMP
from Save_File import importData, SAVEDATA, Browse, GetSC, GetTC, GetHK, GetBR
from Settings import Ui_Settings
from  TC import Ui_TurfClub
from Styles import *
from TurfClub.Turf_Club_Hadicap import TURFHANDICAP
from TurfClub.Turf_Club_HtmlSolver import TurfClubHTMLSOLVER
from TurfClub.Turf_Club_Populate_Class import TurfCLUBPopulateClass
from TurfClub.Turf_Club_Scrapper_Module import SCRAP_Turf_Club_Data

USERARG='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77'

class MyButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("QPushButton { background-color: #bbb; }")
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet("QPushButton { background-color: #007bff; }")

    def leaveEvent(self, event):
        self.setStyleSheet("QPushButton { background-color: #bbb; }")


def Activate(hk,b1,b2,b3):
    b1.setStyleSheet(BUTTONUNSELECTED)
    b2.setStyleSheet(BUTTONUNSELECTED)
    b3.setStyleSheet(BUTTONUNSELECTED)
    hk.setStyleSheet(BUTTONSELECTED)
    pass





class UI(QMainWindow):

    def __init__(self):
        super(UI ,self).__init__()
        uic.loadUi(os.path.join(os.getcwd(),"SmartScrapper.ui") ,self)

        # self.btn1.clicked.connect(self.browse1)
        # self.btn2.clicked.connect(self.browse2)
        # self.btn3.clicked.connect(self.getImages)
        # self.btn4.clicked.connect(self.importImages)
        # self.btn5.clicked.connect(self.analysis)
        # self.btn6.clicked.connect(self.browse3)
        self.quit.clicked.connect(self.close)
        self.setMouseTracking(True)
        self.quit.setStyleSheet(BUTTONSTYLERED)
        self.stackedWidget.setCurrentIndex(4)
        self.menu.clicked.connect(self.toggle)
        self.hk.clicked.connect(self.hkClick)
        self.tc.clicked.connect(self.tcClick)
        self.sc.clicked.connect(self.scClick)

        #TurfClub Buttons
        self.turfHandicapButton.clicked.connect(self.turfHandicapFunction)
        self.turfHtmlSolverButton.clicked.connect(self.turfHtmlSolverFunction)
        self.turfScrapperButton.clicked.connect(self.turfScrapperFunction)
        self.turfPopulateClassButton.clicked.connect(self.turfPopulateClassFunction)





        # Settings Function
        self.settings.clicked.connect(self.settingsClick)
        self.SaveAddress.clicked.connect(self.SaveAll)
        # Browse Function
        self.tc_browse.clicked.connect(self.Browse_tc)
        self.sc_browse.clicked.connect(self.Browse_sc)
        self.hk_browse.clicked.connect(self.Browse_hk)
        self.br_browse.clicked.connect(self.Browse_br)

        # SCMP Buttons
        self.scmpSCRAPBUTTON.clicked.connect(self.scrapSCMPDATA)
        self.scmpPawTimeButton.clicked.connect(self.ScmpPawTimeFunction)

        # Hk Buttons Functions
        self.hkBarrerResultButton.clicked.connect(self.hkBarrerResultFunction)
        self.hkFixLinksButton.clicked.connect(self.hkFixLinksFunction)
        self.hkHandicapButton.clicked.connect(self.hkHandicapFunction)
        self.hkScrapperButton.clicked.connect(self.hkScrapperFunction)
        self.hkPopulateClassButton.clicked.connect(self.hkPopulateClassFunction)
        # self.hkFixRtgButton.clicked.connect(self.hkFixRtgButtonFunction)
        self.hkHtmlSolverButton.clicked.connect(self.hkHtmlSolverFunction)

        self.show()




    # Hk Barrer Functions

    def hkBarrerResultFunction(self):
        try:
            add = GetBR()
            if len(add) > 0 and os.path.exists(add):
                hkGetBarrierResult(add, USERARG)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def hkFixLinksFunction(self):
        try:
            add = GetHK()
            if len(add) > 0 and os.path.exists(add):
                hkFixGear(add, USERARG)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def hkHandicapFunction(self):
        try:
            add = GetHK()
            if len(add) > 0 and os.path.exists(add):
                hkHandiCap(add, USERARG,self.url.text(),int(self.ttlHorses.text()))
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def hkScrapperFunction(self):
        try:
            add = GetHK()
            if len(add) > 0 and os.path.exists(add):
                CreateBackup(add)
                ScrapLatest(add, USERARG,self.url.text())
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def hkPopulateClassFunction(self):
        try:
            add = GetHK()
            if len(add) > 0 and os.path.exists(add):
                HkPopulateClass(add, USERARG)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    # def hkFixRtgButtonFunction(self):
    #     try:
    #         add = GetHK()
    #         if len(add) > 0 and os.path.exists(add):
    #             FixRtg(add, USERARG)
    #         else:
    #             QMessageBox.about(self, 'Finished', f"Error {add} not found")
    #         QMessageBox.about(self, 'Finished', 'Completed Execution !')
    #     except Exception as e:
    #         print(e)
    #     pass


    def hkHtmlSolverFunction(self):
        try:
            add = GetHK()
            if len(add) > 0 and os.path.exists(add):
                HkHtmlSolver(add)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass



    # Turf Club Functions
    def turfHandicapFunction(self):
        try:
            add=GetTC()
            if len(add)>0 and os.path.exists(add):
                TURFHANDICAP(add,USERARG,self.handicapHorseTurf.text())
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def turfHtmlSolverFunction(self):
        try:
            add=GetTC()
            if len(add)>0 and os.path.exists(add):
                TurfClubHTMLSOLVER(add)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def turfScrapperFunction(self):
        try:
            add=GetTC()
            if len(add)>0 and os.path.exists(add):
                CreateBackup(add)
                SCRAP_Turf_Club_Data(add,USERARG)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass

    def turfPopulateClassFunction(self):
        try:
            add=GetTC()
            if len(add)>0 and os.path.exists(add):
                TurfCLUBPopulateClass(add,userag=USERARG)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)
        pass



    # Other Functions
    def toggle(self):
        is_visible = self.sideBar.isVisible()

        # Toggle the visibility of the panel
        self.sideBar.setVisible(not is_visible)

    def hkClick(self):
        try:

            Activate(self.hk,self.tc,self.sc,self.settings)
            self.stackedWidget.setCurrentIndex(1)
        # Add the 'active' class to the 'HK' button

        except Exception as e:
            print(e)


    def scClick(self):
        try:

            Activate(self.sc,self.hk,self.tc,self.settings)
            self.stackedWidget.setCurrentIndex(3)
        # Add the 'active' class to the 'HK' button

        except Exception as e:
            print(e)


    def tcClick(self):
        try:

            Activate(self.tc,self.hk,self.sc,self.settings)
            self.stackedWidget.setCurrentIndex(2)
        # Add the 'active' class to the 'HK' button

        except Exception as e:
            print(e)

    def SaveAll(self):
        try:

            a=str(self.hk_Address.text()).strip()
            b=str(self.tc_Address.text()).strip()
            c=str(self.sc_Address.text()).strip()
            d = str(self.br_Address.text()).strip()

            SAVEDATA(a,b,c,d)
        except Exception as e:
            print(e)


    def settingsClick(self):
        try:
            data=importData()
            Activate(self.settings, self.hk, self.sc, self.tc)
            # self.body.setCurrentWidget(secondpage)
            print(data)
            self.tc_Address.setText(data["TCADDRESS"])
            self.sc_Address.setText(data["SCADDRESS"])
            self.hk_Address.setText(data["HKADDRESS"])
            self.br_Address.setText(data["BRADDRESS"])

            self.stackedWidget.setCurrentIndex(0)
            QApplication.processEvents()
        except Exception as e:
            print(e)
    # def enterEvent(self, event):
    #     self.quit.setStyleSheet("QPushButton { background-color: #007bff; }")
    #
    #
    # def leaveEvent(self, event):
    #     self.quit.setStyleSheet("QPushButton { background-color: #bbb; }")


    #SCMP Functions
    def scrapSCMPDATA(self):
        try:
            add=GetSC()
            if len(add)>0 and os.path.exists(add):
                CreateBackup(add)
                SCARP_SCMP(add)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)

    #
    def ScmpPawTimeFunction(self):
        try:
            add = GetSC()
            if len(add) > 0 and os.path.exists(add):
                CreateBackup(add)
                getSCMPPAWTIME(add)
            else:
                QMessageBox.about(self, 'Finished', f"Error {add} not found")
            QMessageBox.about(self, 'Finished', 'Completed Execution !')
        except Exception as e:
            print(e)

    # Browse Functions
    def Browse_tc(self):
        Browse(self.tc_Address)
    def Browse_sc(self):
        Browse(self.sc_Address)
    def Browse_hk(self):
        Browse(self.hk_Address)
    def Browse_br(self):
        Browse(self.br_Address)
    # def

#
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    UIWindow = UI()
    # widget = QtWidgets.QStackedWidget()
    # settings=Ui_Settings()
    # widget.addWidget(settings)  # create an instance of the first page class and add it to stackedwidget
    # secondpage = Ui_TurfClub()
    # widget.addWidget(secondpage)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing")
