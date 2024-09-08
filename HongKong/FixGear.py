import requests
import xlwings as xw
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from bs4 import BeautifulSoup
from xlwings.constants import Direction

from HongKong.addRtg import updateRtg


def getRTG(url,val1,val2,s,userag):
    r = s.get(str(url).strip(), headers={'User-Agent': userag})
    parsedWebPage = BeautifulSoup(r.content, "html.parser")
    table = parsedWebPage.find("table", {"class": "bigborder"})
    rows = table.find_all("tr")
    for row in rows:
        try:
            cols = row.find_all("td")
            if len(cols) > 0:
                if int(val1) == int(str(cols[0].text).strip()) and int(val2) == int(str(cols[1].text).strip()):
                    return str(cols[17].text).strip()
                    break
        except Exception as e:
            print(f"Fix Gear Error {e}  on cell ")
            pass


    return url



def hkFixGear(address,userag):
    filename=address
    wb = xw.Book(filename)
    sh = xw.sheets["new data"]
    track = xw.sheets["Horse_Name_And_id"]
    endRow = sh.cells(1048576, 1).end(Direction.xlUp).row
    raceIndex = sh.range("B2:C" + str(endRow)).value
    links= sh.range("U2:U" + str(endRow)).value

    updateRtg(sh, track, userag)

    # s = requests.Session()
    # # print(links)
    #
    # for  index,val in enumerate(links):
    #     try:
    #     # print(val)
    #         if "http" in str(val):
    #             sh.range("U2").offset(index,0).value=getRTG(val,raceIndex[index][0],raceIndex[index][1],s,userag)
    #             # if index %10 ==0:
    #             #     print("Working Line "+str(index))
    #     except Exception as e:
    #         print(f"Fix Gear Error {e}  on cell U{index-2}  ",val,raceIndex[index][0],raceIndex[index][1])





    # print(links)
    # sh.range("U2:U" + str(endRow)).value=links


