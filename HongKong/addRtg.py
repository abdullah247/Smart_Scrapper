import  requests
import bs4
import xlwings as xw

from HongKong.rtg_horse_id_Sheet_Handle import *



def FixRtg(address,userarg):


    filename = address
    wk = xw.Book(filename)

    sheet = xw.sheets["new data"]
    track = xw.sheets["Horse_Name_And_id"]

    updateRtg(sheet,track,userarg)


def  updateRtg(sheet,horseSheet,userag):
    last_cell = horseSheet.range("A1048575").end('up').row
    allRtg={}
    # get all the horse name and horse id from horsesheet and put them in dictionary
    dict=readRtgSheet(horseSheet.range("A2:B"+str(last_cell)).value)

    orignalurl="https://racing.hkjc.com/racing/information/english/Horse/Horse.aspx?HorseId="

    last_cell = sheet.range("A1048576").end('up').row
    rtg=sheet.range("L2:M"+str(last_cell)).value
    links = sheet.range("U2:V" + str(last_cell)).value

    raceNameAndIndex=sheet.range("A2:B"+str(last_cell)).value


    for index,value in enumerate(rtg):
        try:
            keyval=str(value[0]).lower().replace("none","").replace(" ","")

            if len(keyval)<1 or "http" in str(links[index][0]).lower():
                # check dict get id of the horse from dictoionar if it is not already present in dictionary it will add it

                # print(raceNameAndIndex[index][0])
                id=checkinDict(dict,raceNameAndIndex[index][0])
                url = orignalurl + id
                if id=="-1" :
                    rtg[index][0]="Not Found"
                    links[index][0]="Not Found"
                else:
                    print(url,raceNameAndIndex[index][0])
                    # 'get ratings here
                    arr=getCRTG(url,raceNameAndIndex[index][0],raceNameAndIndex[index][1],allRtg)
                    rtg[index][0] =arr[0]
                    links[index][0] = arr[1]
        except Exception as e:
            print(e,"Error on " +str(raceNameAndIndex[index][0]) + " race " + str(raceNameAndIndex[index][1]) + " url\n" +url)
    saveDict(horseSheet,dict)

    sheet.range("L2:M" + str(last_cell)).value = rtg
    sheet.range("U2:V" + str(last_cell)).value = links
