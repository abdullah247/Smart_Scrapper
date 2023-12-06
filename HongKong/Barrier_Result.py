import os
import re
import sys

import requests
import xlwings as xw
from bs4 import BeautifulSoup
from xlwings.constants import Direction


def getDates(s,userag):
    url="https://racing.hkjc.com/racing/information/english/Horse/BTResult.aspx"
    counterfl =0
    array=[]
    # print("ww")
    while counterfl<4:
        try:
            r = s.get(str(url).strip(), headers={'User-Agent': userag})
            parsedWebPage = BeautifulSoup(r.content, "html.parser")
            dates = parsedWebPage.find("select", {"id": "selectId"})
            array=str(dates.text).split("\n")
            # print("aw")
            while ("" in array):
                array.remove("")
            counterfl=4
        except Exception as e:
            counterfl=counterfl+1

    return array

    pass

def add(s):
    return  str(s).replace("\n","").strip()


def extractTableValues(table,AllTable,date,course):

    batch=""
    track=""
    distance=""
    video=""
    allvals=[]
    for tblId, tb in enumerate(AllTable):
        if tb == table:
            alltex=str(AllTable[tblId - 2].find("td").text)
            arr =alltex.split("-")
            batch=add(arr[0])
            track=add(arr[1]).upper().replace(course,"")
            distance=add(re.findall("\d+M",alltex.upper())[0])
            try:

                video="https://racing.hkjc.com" + AllTable[tblId - 2].find_all("td")[1].find("a")["href"]
                # print(video)
            except:
                pass

            going=str(AllTable[tblId - 1].find("td").text).upper().replace("GOING:","").replace("\n","").strip()

            newr=AllTable[tblId - 1].find_all("tr")
            firstrow=newr[0].find_all("td")
            time=str(firstrow[len(firstrow)-1].text).upper().replace("TIME:","").replace("\n","").strip().replace(".",":",1)
            sectiontime=str(newr[1].find("td").text).upper().replace("SECTIONAL TIME:","").replace("\n","").strip()

    rows=table.find_all("tr")
    if len(rows)>2:
        for index, row in enumerate(rows):
            if index>=1:
                cols=row.find_all("td")
                name=str(cols[0].find("a").text).strip()
                try:
                    if index==1:
                        car=[date,course,batch,track,going,distance,time,sectiontime,name,add(cols[1].text),
                             add(cols[2].text),add(cols[3].text),add(cols[4].text),add(cols[5].text),
                             add(cols[6].text),add(cols[7].text).replace(".",":",1),add(cols[8].text),add(cols[9].text),video]
                    else:

                        car=[date,course,batch,track,going,distance,time,"-",name,add(cols[1].text),
                             add(cols[2].text),add(cols[3].text),add(cols[4].text),add(cols[5].text),
                             add(cols[6].text),add(cols[7].text).replace(".",":",1),add(cols[8].text),add(cols[9].text),video]

                    allvals.append(car)
                except:
                    pass

                # print(index ,cols[0].find("a").text)

    return allvals


# def extract(s,url,counter,newdate,userag):
#     r = s.get(str(url).strip(), headers={'User-Agent': userag})
#     parsedWebPage = BeautifulSoup(r.content, "html.parser")
#     maindiv = parsedWebPage.find("div", {"id": "divBtresult"})
#
#     bigborders = maindiv.find_all("table", {"class": "bigborder"})
#     AllTable = maindiv.find_all("table")
#
#     course = str(maindiv.find("div", {"class": "btrcheader"}).text).upper().replace("BARRIER TRIAL", "").replace(
#         "\n", "").strip()
#
#     if len(bigborders) > 1:
#         for index, table in enumerate(bigborders):
#             allvals = extractTableValues(table, AllTable, newdate, course)
#             addrow = len(allvals)
#             sh.range("A" + str(counter) + ":" + "S" + str(counter + addrow)).value = allvals
#             counter = counter + addrow
#
#
#
#     else:
#         allvals = extractTableValues(bigborders[0], AllTable, newdate, course)
#         addrow = len(allvals)
#         sh.range("A" + str(counter) + ":" + "S" + str(counter + addrow)).value = allvals
#         counter = counter + addrow
#
#     return counter

def hkGetBarrierResult(address,userag):

    dateurl="https://racing.hkjc.com/racing/information/english/Horse/Btresult.aspx#Date="
    s = requests.Session()

    sheetName="Results"
    filename = address


    # filename= sys.argv[1]
    # print(filename)
    # sheetName= sys.argv[2]
    #
    # if len(sys.argv)>=4:
    #     url=dateurl
    #     if sys.argv[3].lower()=="all":
    dates = getDates(s,userag)
    #     else:
    #         dates = [sys.argv[3]]
    # else:
    #     da = getDates(s)
    #     # print(da)
    #     ar = da[0].split("/")
    #     newdate = ar[2] + "/" + ar[1] + "/" + ar[0]
    #     dates=[newdate]


    wb = xw.Book(filename)
    # print(sheetName)
    print(filename)
    print(sheetName)
    sh = xw.sheets[sheetName]
    # print(getDates(s))
    counter = 2

    # dates=["19/06/2023","19/06/2023"]
    if len(dates)>1:
        for dat in dates:
            ar=dat.split("/")
            newdate= ar[2] +"/" + ar[1] +"/" + ar[0]
            url = "https://racing.hkjc.com/racing/information/english/Horse/BTResult.aspx?Date=" +newdate
            print(url)
            r = s.get(str(url).strip(), headers={'User-Agent': userag})
            parsedWebPage = BeautifulSoup(r.content, "html.parser")
            maindiv = parsedWebPage.find("div", {"id": "divBtresult"})

            bigborders = maindiv.find_all("table", {"class": "bigborder"})
            AllTable = maindiv.find_all("table")

            course = str(maindiv.find("div", {"class": "btrcheader"}).text).upper().replace("BARRIER TRIAL", "").replace(
                "\n", "").strip()

            if len(bigborders)>0:
                for index,table in enumerate(bigborders):
                    allvals=[]
                    allvals=extractTableValues(table,AllTable,newdate,course)
                    addrow=len(allvals)
                    sh.range("A"+str(counter)+":"+"S"+str(counter+addrow)).value=allvals
                    counter=counter+addrow



            else:
                allvals = extractTableValues(bigborders[0], AllTable, newdate, course)
                addrow = len(allvals)
                sh.range("A" + str(counter) + ":" + "S" + str(counter + addrow)).value = allvals
                counter = counter + addrow

    # elif len(dates)==1:
    #     url = "https://racing.hkjc.com/racing/information/english/Horse/Btresult.aspx#Date=" + dates[0]
    #     counter=extract(s, url, counter,dates[0])

    print("Finish")





