import os
import re
import sys

import requests
import xlwings as xw
from xlwings.constants import Direction
import re


# Press the green button in the gutter to run the script.
trackStart={
    "sc":4,
    "lc":14,
    "py":28
}


def getrate(cl,toCourse,dist,track,flag=False):
    # print(cl,toCourse,dist)
    try:
        dist =int(str(dist).replace("M",""))
        mclass = str(cl).lower().strip().replace(" ", "").replace(".0","")
        toCourse=str(toCourse).lower().replace("none","py")
        st = trackStart[toCourse] - 1

        trak = -1
        for i in range(2, len(track[0]), 4):
            # print(st,i,track, str(trackVariance.cell((st - 2), i).value).replace(" ","").strip().lower(), mclass, trackVariance.cell(st, i).value)
            val = track[st - 2][i]
            if type(val) == float:
                val = str(int(val))
            if str(val).replace(" ", "").replace(".0","").strip().lower() == mclass:
                trak = i + 2
                break

        for i in range(0, 75):
            # if not flag:
            #     if int(float(track[st + i][2])) == int(dist):
            #         return track[st + i][trak]
            # else:
            if str(track[st + i][2]) == "None":
                return 0
            elif int(float(track[st + i][2])) >= int(dist):
                # print(cl, toCourse, dist , track[st + i][trak])
                return track[st + i][trak]
    except Exception as e:
        print("Track Error" ,e)
        return 0



def getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse, res, track, row1, row3):
    toCourse = str(toCourse).lower()

    changeable = ["5", "op m", "m", "r", "nov"]

    if not (toCourse == "sc" or toCourse == "lc"):
        toCourse = "py"



    nclass = fromClass

    res[1] = ""
    if str(fromClass).replace(".0", "").strip().lower() in changeable and str(toclass).replace(".0", "").strip() in changeable:
        nclass = toclass

    try:
        res[0] = round(getrate(nclass, toCourse, todist, track, False)) - round(getrate(fromClass, fromCourse, fromdist, track))
    except Exception as e:
        print("ww", e)


    try:
        res[1] = round(row1 + res[0]) if round(row1 + res[0]) > 0 else "Nil"
    except:
        pass


    try:
        res[2] = round(row3 + res[0]) if round(row3 + res[0]) > 0 else "Nil"
    except:
        pass



def export(sheet,horses,data,courseData,track,noOfHorses,csh2):

    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row
    sh =  sheet.range("A2:BJ" + str(endRow)).value

    horsesrow = {}
    for hors in horses:
        horsesrow[hors] = []
    for index,row in enumerate(sh):
        if str(row[13]).strip() in horses:
            horsesrow[row[13]].append(index)
            if len(horsesrow[row[13]]) > noOfHorses:
                a = horsesrow[row[13]].pop(0)


    counter=2

    csh2.range("A2:BJ90000").clear()
    sh2 = csh2.range("A2:BJ90000").value

    for key in data:
        toclass = courseData[key][0]
        todist = courseData[key][1]
        toCourse = courseData[key][2]
        sh2[counter][2] = f"Class :{courseData[key][0]} Distance : {courseData[key][1]} Course : {courseData[key][2]}"
        counter=counter+2

        # print(data,key)
        for horse in data[key]:

            for row in horsesrow[horse]:
                flag = True
                for i in range(0, len(sh[0])):
                    # print(counter,i,row,sh[row][i])
                    if i==27  or i==30 :
                            sh2[counter][i] ="'" +str(sh[row][i])

                    else:
                        sh2[counter][i] = sh[row][i]

                res=[sh2[counter][45],sh2[counter][46],sh2[counter][47]]
                try:
                    getMAtch(toclass, todist, toCourse, sh2[counter][3], sh2[counter][9],sh2[counter][8], res, track, sh2[counter][41], sh2[counter][44])
                except Exception as e:
                    print(e)

                sh2[counter][45]=res[0]
                sh2[counter][46]=res[1]
                sh2[counter][47]=res[2]

                counter = counter + 1

            if flag:
                counter += 1


            counter=counter+3






    csh2.range("A2:BJ90000").value = sh2
    csh2.range("S2:S90000").number_format = "mm:ss.00"
    csh2.range("X2:X90000").number_format = "mm:ss.00"

def TURFHANDICAP(ADDRESS,userag,noofhorses=5):





    dateurl="https://api.turfclub.com.sg/api/v1/racing/stc/getHandicapsDatelist/8"



    s = requests.Session()
    r = s.get(dateurl, headers={'User-Agent': userag})
    datelistjson = r.json()
    mdate = datelistjson["Data"]
    racedate=mdate[0]["racedate"]
    # racedate="2023-09-16"
    mainHeaderUrl = f"https://api.turfclub.com.sg/api/v1/racing/stc/getHandicapsByRace/en/{racedate}"
    r = s.get(mainHeaderUrl, headers={'User-Agent': userag})
    datelistjson = r.json()
    races=datelistjson["Data"]

    allHorses=[]
    horses={}
    details={}
    for index ,race in enumerate(races):
        toclass=str(race["raceclass"]).lower().replace("class","").replace("group","g").replace(" ","").strip().replace("openmaiden","op m")
        if "restricted" in toclass:
            toclass="r"
        tocourse=race["course"]
        if tocourse ==None:
            tocourse="py"
        todist=str(race["racedist"]).lower().replace("m","")
        details[index] = [toclass, todist, tocourse]
        print(toclass,tocourse,todist)
        for rows in race["racefield"]:
            allHorses.append(rows["horsename"])
            if index in horses:
                horses[index].append(rows["horsename"])

                # print(horses[index],index)
            else:
                horses[index] =[rows["horsename"]]

    filename = ADDRESS
    wk = xw.Book(filename)

    sheet=xw.sheets["Database"]
    track = xw.sheets["track variance"].range("A1:CT100").value


    counter = 2

    csh2 = xw.sheets["raceList"]
    export(sheet, allHorses, horses, details, track,noofhorses,csh2)

    # print("Finish")





