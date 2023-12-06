import os
import requests
import xlwings as xw
from bs4 import BeautifulSoup
from xlwings.constants import Direction
import re

userag='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77'
trackStart={
    "st":4,
    "hv":16,
    "awt":28
}

def getrate(cl,toCourse,dist,track,flag=False):
    # print(cl,toCourse,dist)
    try:
        dist =int(str(dist).replace("M","").replace(".0",""))
        mclass = str(cl).lower().strip().replace(" ", "").replace(".0","")
        st = trackStart[toCourse] - 1

        trak = -1
        for i in range(2, len(track[0]), 3):
            # print(st,i,track, str(trackVariance.cell((st - 2), i).value).replace(" ","").strip().lower(), mclass, trackVariance.cell(st, i).value)
            val = track[st - 2][i]
            ssss="|" + str(mclass) + "|"
            if ssss  in str(val).replace(" ", "").strip().lower()   or  ssss  == str(val).replace(" ", "").strip().lower():
                trak = i
                break

        for i in range(0, 75):
            # if not flag:
            #     if int(float(track[st + i][2])) == int(dist):
            #         return track[st + i][trak]
            # else:
            if str(track[st + i][1]) == "None":
                return 0
            elif int(float(track[st + i][1])) >= int(float(dist)):
                # print(cl, toCourse, dist , track[st + i][trak])
                return track[st + i][trak+1]
    except Exception as e:
        print("Track Error" ,e)
        return 0


def getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse, res, track, row1, row3):
    toCourse = str(toCourse).lower().strip()
    changeable = ["5", "op m", "m", "r", "nov"]




    for index, cl in enumerate(fromClass):

        if not str(fromCourse[index][0]).lower().strip() == "ch":
            nclass = cl
            res[index][1] = ""
            if str(cl).replace(".0", "").strip().lower() in changeable and str(toclass).replace(".0",
                                                                                                "").strip() in changeable:
                nclass = toclass

            if str(fromCourse[index][0]).lower().strip() == "st":
                fcourse = "st"
                if not str(fromCourse[index][1]).lower().strip() == "turf":
                    fcourse = "awt"
            else:
                fcourse="hv"

            try:
                # if not toCourse == fromCourse[index]:
                #  print(getrate(nclass,toCourse,todist,track ,False),getrate(cl,fromCourse[index],fromdist[index],track))
                res[index][0] = round(getrate(nclass, toCourse, todist, track, False)) - round(
                    getrate(cl, fcourse, fromdist[index], track))

            # if not toCourse == fromdist[index]:
            #     res[index][1] =  round(getrate(cl, toCourse, todist, track,False)) -round(getrate(cl, fromCourse[index], fromdist[index], track))

            except Exception as e:
                print("ww", e)

            try:
                # print(row1[index], res[index][1],"  ",row3[index],int(res[index][1]))
                res[index][1] = round(row1[index] + res[index][0]) if round(row1[index] + res[index][0]) > 0 else "Nil"

            except:
                pass

            try:

                res[index][2] = round(row3[index] + res[index][0]) if round(row3[index] + res[index][0]) > 0 else "Nil"
            except:
                pass


def clearSheeets(xw):

    for key in range(1,13):
        xw.sheets[f"r{key}"].range("A2:BJ500").clear()


def export(sheet,horses,data,courseData,track):

    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row
    sh =  sheet.range("A2:BJ" + str(endRow)).value

    flag=False
    horsesrow = {}
    for hors in horses:
        horsesrow[hors] = []
    for index,row in enumerate(sh):
        if str(row[0]).strip() in horses:
            horsesrow[row[0]].append(index)
            if len(horsesrow[row[0]]) > 5:
                a = horsesrow[row[0]].pop(0)

    for key in data:
        csh2=xw.sheets[key]

        sh2=csh2.range("A2:BJ1000").value
        counter = 0
        # print(data,key)

        for horse in data[key]:

            for row in horsesrow[horse]:
                flag = True
                for i in range(0, len(sh[0])):
                    # print(counter,i,row,sh[row][i])
                    if i==11  or i==14 :
                            sh2[counter][i] ="'" +str(sh[row][i])

                    else:
                        sh2[counter][i] = sh[row][i]

                counter = counter + 1

            if flag:
                counter += 1
        csh2.range("A2:BJ1000").value = sh2
        csh2.range("S2:S1000").number_format = "mm:ss.00"
        csh2.range("X2:X1000").number_format = "mm:ss.00"
        endRow = csh2.cells(1048576, 1).end(Direction.xlUp).row
        csh2.range("AL" + str(endRow + 3)).value = f"Class :{courseData[key][0]} Distance : {courseData[key][1]} Course : {courseData[key][2]}"

        try:

            toclass = courseData[key][0]
            todist = courseData[key][1]
            toCourse = courseData[key][2]

            endRow = csh2.cells(1048576, 1).end(Direction.xlUp).row
            fromClass = csh2.range("J2:J" + str(endRow)).value
            fromdist = csh2.range("H2:H" + str(endRow)).value
            fromCourse = csh2.range("E2:F" + str(endRow)).value
            res = csh2.range("AN2:AP" + str(endRow)).value
            row1 = csh2.range("AH2:AH" + str(endRow)).value
            row3 = csh2.range("AL2:AL" + str(endRow)).value

            try:
                getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse, res, track, row1, row3)
                csh2.range("AN2:AP" + str(endRow)).value = res
            except Exception as e:
                print(e)

        except Exception as e:
            print("Error 2", e)



def HkPopulateClass(address,userag):

    url="https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx"
    s = requests.Session()

    data={}
    courseData={}

    filename = address
    wk = xw.Book(filename)

    sheet=xw.sheets["new data"]
    track = xw.sheets["track variance"].range("A1:CT100").value

    clearSheeets(xw)
    counter = 2


    flag=True

    counter=1
    allHorses=[]
    horses=[]
    while(True):

        r = s.get(str(url).strip(), headers={'User-Agent': userag})




        parsedWebPage = BeautifulSoup(r.content, "html.parser")

        if flag :
            allLink = parsedWebPage.find("table", {"class": "js_racecard"}).find("tr").find_all("a",href=True)

            arryAnchor=[ anchor['href'] for anchor in allLink]
            # print(arryAnchor)
        tbl = parsedWebPage.find("table", {"id": "racecardlist"}).find("table")


        names=tbl.find_all("tr")
        for i ,val in enumerate(names):
            if i>0:
                horseName=val.find_all("td")[3].find("a").text
                horses.append(horseName)
                allHorses.append(horseName)


        maintr=str(parsedWebPage.find("div", {"class": "f_fs13"}).prettify().lower().strip().replace("\n",""))

        allvals=maintr.split(",")
        toclass= str(allvals[len(allvals)-1]).lower().strip().replace("class","").replace("restricted","r").replace(" ","").replace("</div>","").replace("(","").replace(")","")
        toclass=toclass.replace("groupthree","g3").replace("grouptwo","g2").replace("groupone","g1")
        # print(toclass)
        todist=re.findall("\d+m",maintr)[0].replace("m","").strip()

        tocourse=str(parsedWebPage.find("table", {"class": "js_racecard"}).find("td").find("span").text).lower().replace(" ","")
        if "shatin" in tocourse:
            tocourse="st"
            if not "turf" in maintr:
                tocourse="awt"
        else:
            tocourse="hv"


        print(todist,tocourse,toclass)

        data["r" + str(counter)]=horses
        courseData["r" + str(counter)]=[toclass,todist,tocourse]
        horses=[]

        flag=False
        if counter<len(arryAnchor)+1:
            url="https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx" + str(arryAnchor[counter-1])
            print(url)
        else:
            export(sheet, allHorses, data, courseData, track)
            break
        counter = counter + 1
    export(sheet,allHorses,data,courseData,track)

    # clearing redundant sheet
    for i in range(1,13):
        key=f"r{i}"
        if not key in data:
            csh2=xw.sheets[key]
            csh2.range("A2:BJ1000").clear()

    print("Finish")





