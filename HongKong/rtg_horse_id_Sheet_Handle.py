# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import xlwings as xw


def addChrVal(nn, dict):
    url = "https://racing.hkjc.com/racing/information/english/Horse/SelectHorsebyChar.aspx?ordertype=" + nn

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    anchors = soup.find_all('a', class_='table_eng_text')

    for index, a in enumerate(anchors):
        if not a.text in dict:
            dict[a.text] = str(a["href"]).split("=")[1]


def checkinDict(dict, name):
    if not name in dict:
        chrVal = name[0]
        addChrVal(chrVal, dict)
    if name in dict:
        return  dict[name]
    else:
        return "-1"




def saveDict(sheet, dict):
    items_list_array = [[k, v] for k, v in dict.items()]
    sheet.range("A2:B2").value = items_list_array


def readRtgSheet(arr):
    dict = {}
    for val in arr:
        dict[val[0]] = val[1]
    return dict



def getCRTG(url,horseName,raceNo:str,dict):
    url = url
    rtg="---"
    gear="---"
    key =str(horseName) + str(raceNo).strip()
    if key in dict:
        return dict[key]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    allRows = soup.find_all("tr")
    raceNo=str(raceNo).replace(".0","")
    for row in allRows:
        tds=row.find_all("td", class_='htable_eng_text')
        if len(tds)>8:
            rn0=str(tds[0].text).strip().replace("\n","")
            rtg0 = str(tds[8].text).strip().replace("\n", "")
            gear =str(tds[17].text).strip().replace("\n","")
            # print(str(tds[0]).strip(), tds[8].text)
            if len(rtg0)>0:
                dict[str(horseName) + rn0]=rtg0
            else:
                dict[str(horseName) + rn0] = "--"
            # no need to parse past data

            if rn0 == str(raceNo).zfill(3):
                return [dict[str(horseName) + rn0],gear]

    return rtg