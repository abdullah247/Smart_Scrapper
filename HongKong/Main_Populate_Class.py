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
HVDISTANCE=[1000,1200,1650,1800,2200]
AWTDISTANCE=[1200, 1650, 1800, 2000, 2200, 2400]
STDISTANCE=[1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
def filterDistance(ff:str):
    try:
        return int(ff.lower().replace(".0","").replace("m","").strip())
    except Exception as e:
        print("Distance Filter error",e)
        return None



def find_closest_value(firstArray, secondArray, target_value):
    # Find common values present in both AWT and ST
    common_values = list(set(firstArray) & set(secondArray))

    # If no common values are found, return None
    if not common_values:
        return None

    # Find the closest value to the target_value
    closest_value = min(common_values, key=lambda x: abs(x - target_value))

    return closest_value


def AddTime(SpeedTime,timeVal,flag):
    try:
        timeVal=float(timeVal)
        SpeedTime=str(SpeedTime)
        fval=SpeedTime[0]
        tim =float(SpeedTime[2:])
        if flag:
            tim=tim +timeVal
        else:
            tim=tim-timeVal

        if tim >60:
            tim =tim % 60
            fval=str(int(SpeedTime[0])+1)
        elif tim<0:
            tim = tim % 60
            fval = str(int(SpeedTime[0]) - 1)
        return fval +"." + "{:05.2f}".format(tim)
    except Exception as e:
        print("Add Time Error",e,SpeedTime,timeVal)
    pass


def getCoresspondingValue(currentSheet, SpeedTime, fromdist,todist,column):
    row = 1
    try:
        if int(fromdist)<int(todist):
            flag=True
        else:
            flag=False

        TopRow = currentSheet[0]
        currentDistance = filterDistance(str(TopRow[column]))
        while currentDistance != todist:
            if flag:
                column = column + 3
                # previous value of next column
                SpeedTime= AddTime(SpeedTime,currentSheet[0][column-2],flag)
            else:
                column = column - 3
                # next value of previous column
                SpeedTime = AddTime(SpeedTime, currentSheet[0][column + 1], flag)
            currentDistance = filterDistance(str(TopRow[column]))

        if currentDistance == todist:
            row = 1

            orginalspeedTime = float(SpeedTime[::-1].replace('.', '', 1)[::-1])
            cval = currentSheet[row][column - 1]
            cval=float(cval[::-1].replace('.', '', 1)[::-1])
            while row < len(currentSheet) and cval < orginalspeedTime:
                row = row + 1
                cval = currentSheet[row][column - 1]
                if currentSheet[row][column - 1] is None:
                    return currentSheet[row-1][column]
                cval = float(cval[::-1].replace('.', '', 1)[::-1])

            if cval == orginalspeedTime or row==1:
                return currentSheet[row][column]
            else:
                previousVal=currentSheet[row-1][column]
                previousVal = float(previousVal[::-1].replace('.', '', 1)[::-1])
                if abs(previousVal - orginalspeedTime) < abs(cval -orginalspeedTime):
                    return currentSheet[row - 1][column]
                else:
                    return currentSheet[row + 1][column]

    except Exception as e:
        print("Corresspondance Error",e,SpeedTime,row,column,cval,previousVal)
    pass

# Only gets row and column of current rating the corresponding function convert it to corresponding rate
def getrate(currentSheet,fromdist,todist,FinalRating):
    try:

        if fromdist == todist : return FinalRating
        column=1
        row = 1
        TopRow=currentSheet[0]
        currentDistance = filterDistance(str(TopRow[column]))


        while int(currentDistance) != int(fromdist) :
            column=column+3
            currentDistance = filterDistance(str(TopRow[column]))
            if column>len(TopRow):
                break
            # should only run if condition below is true
        if currentDistance == fromdist:
            row=1
            while row <  len(currentSheet) and not currentSheet[row][column] is None and int(currentSheet[row][column]) >int(FinalRating):
                row=row+1

                if row>len(currentSheet) or  currentSheet[row][column] is None:
                    row =row-1
                    break


        if row<len(currentSheet):
            if row>1 and (abs(currentSheet[row-1][column] -FinalRating) < abs(FinalRating - currentSheet[row][column]) ):
                return getCoresspondingValue(currentSheet, currentSheet[row-1][column - 1],  fromdist,todist,column)
            else:
                return getCoresspondingValue(currentSheet,currentSheet[row][column-1],fromdist,todist,column)




    except Exception as e:
        print("Track Error" ,e,str(currentDistance),str(fromdist),str(currentSheet[row][column]))
        return 0


def getTrackPars(trackPar, courseConversion, todist, cl,value:float):

    try:
        if cl is None or todist is None:
            return  value


        column=2
        cl="|" + str(cl) +"|"
        jump =5
        clas=str(trackPar[1][column]).lower().replace(".0", "").replace("r","").strip()
        while not cl in clas and column <len(trackPar[1]) :
            column=jump+column
            clas = str(trackPar[1][column]).replace(".0", "").replace("r", "").strip().lower()

        row=3
        currentCourse=str(trackPar[row][0]).strip()

        if cl in clas:
            while currentCourse != courseConversion and row<len(trackPar):
                row=row+1
                currentCourse = str(trackPar[row][0]).strip()

            if currentCourse == courseConversion:
                if trackPar[row][column + 4] is None: trackPar[row][column + 4] = 0
                if trackPar[row][1] is None: trackPar[row][column + 4] = 0
                currentdist=int(str(trackPar[row][1]).lower().replace(".0", "").replace("m","").strip())
                while currentdist != int(todist) and row<len(trackPar):
                    row=row+1
                    currentdist = int(str(trackPar[row][1]).lower().replace(".0", "").replace("m", "").strip())




                if currentdist ==int(todist):
                    if not trackPar[row][column+4] is None:
                        if value is None:  return trackPar[row][column+4]
                        return value + trackPar[row][column+4]
                    else:
                        return value

    except Exception as E:
        print("Track Par Error",E,column)




    pass


def getMAtch(todist, toCourse, fromClass, fromdist, fromCourse, Result, trackPar, FinalRating,st,hv,awt):
    toCourse = str(toCourse).lower().strip()
    changeable = ["5", "op m", "m", "r", "nov"]




    for index, cl in enumerate(fromClass):
        if not fromdist[index] is None:
            if not str(fromCourse[index][0]).lower().strip() == "ch":
                Result[index][1] = ""
                nclass = str(cl).lower().replace(".0", "").replace("r","").strip()

                if str(fromCourse[index][0]).lower().strip() == "st":
                    fcourse = "st"
                    fromCurrentSheet=st
                    fromCurrentSheetValues=STDISTANCE
                    if not str(fromCourse[index][1]).lower().strip() == "turf":
                        fcourse = "awt"
                        fromCurrentSheet=awt
                        fromCurrentSheetValues = AWTDISTANCE
                else:
                    fcourse="hv"
                    fromCurrentSheet=hv
                    fromCurrentSheetValues = HVDISTANCE

                if toCourse =="st":
                    toCourseValues=STDISTANCE
                    toCourseSheet=st
                elif  toCourse =="hv":
                    toCourseValues=HVDISTANCE
                    toCourseSheet=hv
                else:
                    toCourseValues=AWTDISTANCE
                    toCourseSheet=awt



                try:
                    courseConversion = fcourse + " vs " + toCourse
                    fromdist[index] = filterDistance(str(fromdist[index]))
                    todist = filterDistance(str(todist))
                    if FinalRating[index] is None:
                        FinalRating[index]=0
                    if toCourse == fcourse :
                        if todist != fromdist[index]:

                            Result[index][1]=getrate(fromCurrentSheet,fromdist[index],todist,FinalRating[index])
                            # print(toCourse, fromdist[index], todist,FinalRating[index],Result[index][1])
                        else:
                            Result[index][1] = FinalRating[index]

                    else:
                        if todist == fromdist[index]:
                            # print(fcourse, toCourse, todist, nclass, FinalRating[index])
                            Result[index][1] = getTrackPars(trackPar,courseConversion,todist,nclass,FinalRating[index])
                            # print(fcourse, toCourse, todist,nclass, FinalRating[index], Result[index][1])
                            pass
                        else:
                            fromdistance=filterDistance(str(fromdist[index]))
                            try:
                                if int(fromdistance) in toCourseValues:
                                    trackAdjusted = getTrackPars(trackPar, courseConversion, int(fromdistance),nclass, FinalRating[index])
                                    Result[index][1] = getrate(toCourseSheet, int(fromdistance), int(todist),trackAdjusted)
                                    print(
                                        f"RNo {index + 2} Orignal distance {fromdistance} converted value {FinalRating[index]} After track adjusted {trackAdjusted} Result {Result[index][1]}")
                                else:
                                    closestDistance =find_closest_value(toCourseValues,fromCurrentSheetValues,int(todist))
                                    CONVAL = getrate(fromCurrentSheet, fromdistance, int(closestDistance), FinalRating[index])
                                    trackAdjusted = getTrackPars(trackPar, courseConversion, int(closestDistance), nclass,CONVAL)
                                    Result[index][1] = getrate(toCourseSheet, closestDistance, int(todist), trackAdjusted)


                            except Exception as e:
                                print("Error in last part",e,index,fromdistance,todist,courseConversion)



                            pass



                    # if not toCourse == fromCourse[index]:
                    #  print(getrate(nclass,toCourse,todist,track ,False),getrate(cl,fromCourse[index],fromdist[index],track))


                # if not toCourse == fromdist[index]:
                #     res[index][1] =  round(getrate(cl, toCourse, todist, track,False)) -round(getrate(cl, fromCourse[index], fromdist[index], track))

                except Exception as e:
                    print("ww", e)




def clearSheeets(xw):

    for key in range(1,13):
        xw.sheets[f"r{key}"].range("A2:BJ500").clear()


def export(sheet,horses,data,courseData,trackPar,st,hv,awt):

    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row
    sh =  sheet.range("A2:BJ" + str(endRow)).value

    flag=False
    horsesrow = {}
    for hors in horses:
        horsesrow[hors] = []
    for index,row in enumerate(sh):
        if str(row[0]).strip() in horses:
            if str(row[2]).lower().replace(".0","").replace("dh","").strip().isdigit():
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
            todist = str(courseData[key][1]).lower().replace(".0","").replace("m","").strip()
            toCourse = courseData[key][2]

            endRow = csh2.cells(1048576, 1).end(Direction.xlUp).row
            fromClass = csh2.range("J2:J" + str(endRow)).value
            fromdist = csh2.range("H2:H" + str(endRow)).value
            fromCourse = csh2.range("E2:F" + str(endRow)).value
            Result = csh2.range("AO2:AP" + str(endRow)).value
            FinalRating = csh2.range("AL2:AL" + str(endRow)).value

            try:
                getMAtch(todist, toCourse, fromClass, fromdist, fromCourse, Result, trackPar, FinalRating,st,hv,awt)
                csh2.range("AO2:AP" + str(endRow)).value = Result
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
    st = xw.sheets["st"].range("A1:W83").value
    hv = xw.sheets["hv"].range("A1:N83").value
    awt = xw.sheets["st awt"].range("A1:Q83").value

    trackPar=xw.sheets["track pars"].range("A1:CT100").value
    clearSheeets(xw)



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
            url = "https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx" + str(arryAnchor[0]).split("RaceNo=")[0] + "RaceNo=" + str(counter)
            r = s.get(str(url).strip(), headers={'User-Agent': userag})
            parsedWebPage = BeautifulSoup(r.content, "html.parser")



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
            url="https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx" + str(arryAnchor[0]).split("RaceNo=")[0] + "RaceNo=" + str(counter+1)
            print(url)
        else:
            export(sheet, allHorses, data, courseData, trackPar, st, hv, awt)
            break
        counter = counter + 1
    export(sheet,allHorses,data,courseData,trackPar, st, hv, awt)

    # clearing redundant sheet
    for i in range(1,13):
        key=f"r{i}"
        if not key in data:
            csh2=xw.sheets[key]
            csh2.range("A2:BJ1000").clear()

    print("Finish")





