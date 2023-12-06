
import sys

import xlwings as xw
import re
import os
import datetime as dt


class RelativeColumn:

    def __init__(self):
        self.horsename = 0
        self.raceindex = 1
        self.pla = 2
        self.date = 3
        self.rc = 4
        self.track = 5
        self.course = 6
        self.dist = 7
        self.g = 8
        self.RaceClass = 9
        self.dr = 10
        self.rtg = 11
        self.trainer = 12
        self.jockey = 13
        self.lbw = 14
        self.winodds = 15
        self.actWt = 16
        self.Runningposition = 17
        self.finishtime = 18
        self.DeclareHorse = 19
        self.gear = 20
        self.videoreplay = 21
        self.videoreplay2 = 22
        self.winnertime = 23

        self.speedrating = 0
        self.winnerrating = 1
        self.track = 2
        self.variancerating = 3
        self.difference = 4


MissingHorses=[]
SpeedRatingTop=[]

trackClass={
    "g1":4,
    "g2":4,
    "g3":4,
    "1":7,
    "2":10,
    "3":13,
    "4":16,
    "5":19,
    "griffin":22
    }

trackStart={
    "st":4,
    "hv":16,
    "awt":28
}

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def getIndex(srat, lbw, dist,marginSheet):
    lbw=str(lbw).replace("'","")
    if str(lbw).strip()=="-" or len(str(lbw).strip())<1:
        return 0
    else:
        for col in range(1,26):
            try:
                if not marginSheet[1][col] is None:
                    if int(dist)==int(marginSheet[1][col]):
                        for row in range(2,90):
                            if not marginSheet[row][0] is None:
                                if str(marginSheet[row][0]).strip()==str(lbw).strip():
                                        # print(srat,margin[row][col])
                                        return srat-marginSheet[row][col]
                                else:
                                    if has_numbers(lbw) and has_numbers(str(marginSheet[row][0])):
                                        if "-" in lbw or "/" in lbw:

                                            nlbw=str(lbw).replace("-","+").strip()
                                            # print(eval(nlbw) ,float(marginSheet[row][0]))
                                            if eval(nlbw) <=float(marginSheet[row][0]):
                                                return  srat-marginSheet[row][col]
                                        else:
                                            # print(float(lbw),float(str(marginSheet[row][0])),float(lbw) <=float(marginSheet[row][0]))
                                            if float(lbw) <=float(str(marginSheet[row][0])):
                                                return  srat-marginSheet[row][col]



            except Exception as e:
                print("EE",e)
                pass


    return 0




def CalCulations(sh, k, turn,val,SpeedRating,winingTime,trackVariance,tv,clas,raceIndex,lbw,marginSheet):

    raceNoCounter=0
    PlaceCounter=1
    if len(str(sh[k]).replace("-", "").strip())>2:

            atime=(format_result(sh[k]).strftime("%M.%S.%f")) if (not "-" in str(sh[k]) or not sh[k] is None) else ""



            # print("First")
            srat=getTurnValue(turn,atime,val)
            SpeedRating[k][0]=srat

            if not "http" in str(winingTime[k]):
                wtime = (format_result(winingTime[k]).strftime("%M.%S.%f")) if (
                        not "-" in str(sh[k]) or not sh[k] is None) else ""
                # print("second")
                SpeedRating[k][1] = getTurnValue(turn, wtime, val)

            try:
                if int(raceIndex[raceNoCounter]) == 1 and int(str(raceIndex[PlaceCounter]).lower().replace("dh","").strip())==1:
                        SpeedRatingTop[raceIndex[raceNoCounter]] =srat
                else:
                    if raceIndex in SpeedRatingTop:
                        SpeedRating[k][0] = getIndex(srat,lbw,val,marginSheet)
                    else:
                        print(str(raceIndex[PlaceCounter]).lower().replace("dh","").strip())
                        if not  int(float(str(raceIndex[PlaceCounter]).lower().replace("dh","").strip()))==1:
                            MissingHorses.append([k,SpeedRating[k][1],lbw,val])
                        else:
                            SpeedRating[k][0]= SpeedRating[k][1]


            except Exception as e:
                print("eRR 1",e)
                pass

    #
    #
    #
    SpeedRating[k][2] = getTrackVarianxe(tv, val, clas,trackVariance)

    try:
        SpeedRating[k][3] = int( SpeedRating[k][1]) - int(SpeedRating[k][2])
    except  Exception as e:
        print("eRR 2",e)
        pass

    try:
        if "-" in str(SpeedRating[k][3]):
            SpeedRating[k][4] = int(SpeedRating[k][0]) + int(str(SpeedRating[k][3]).replace("-",""))
        else:
            SpeedRating[k][4] = int(SpeedRating[k][0]) - int(str(SpeedRating[k][3]).replace("-", ""))

    except Exception as e:
        print("eRR 3",e)
        pass

    return  SpeedRating



def getTurnValue(turn, param, dist):

    flag=1
    try:
        myval=float("".join(param.replace(":","").rsplit(".", 1)))

        for i in range(29):
            # print(turn.range(1,flag).value ,f"{val}m",turn.range(1,flag).value == f"{val}m")
            if turn[0][flag] == f"{dist}m":

                break
            flag=flag+3

        current=turn[1][flag]

        for i in range(1,150):
            val = turn[i][flag-1]

            comp=float("".join(val.replace(":",".").rsplit(".", 1)))

            # print(myval ,comp,myval ==comp,comp>myval)
            if myval ==comp :
                current = turn[i][flag]
                # return current
            elif  comp>myval:
                current = turn[i-1][flag]

                return current
    except Exception as e:
        print("eRR 4",e)
        return ""




    pass


def getTrackVarianxe(track, distance, mclass,trackVariance):
    try:
        track=str(track).lower().strip()
        mclass= "|"+str(mclass).replace(".0","").lower().strip()+"|"
        st=trackStart[track]-1
        # print(track,trackStart[track])
        for i in range (0,15):
            # print("asdfa ",trackVariance.range(st+i,2).value,st,trackClass[mclass])
            if int(trackVariance[st+i][1])==int(distance):
                for j in range(1,60):

                    if mclass in str(trackVariance[1][j]).lower().strip():

                        return trackVariance[st+i][j+1]
                        break
    except:
        return ""
    return ""

    pass


def format_result(result):
    x = result  # a float
    x = int(x * 24 * 3600)  # convert to number of seconds
    y=result * 24 * 3600 - int(result * 24 * 3600)
    y=round(y*100)*10000
    while y>=1000000:
        x=x+1
        y=y-1000000
    # print(y)
    my_time = dt.time(0,(x % 3600) // 60, x % 60, y)
    return my_time

# Press the green button in the gutter to run the script.
from xlwings.constants import Direction




def HkHtmlSolver(address):



    filename = address


    wb = xw.Book(filename)
    sh = xw.sheets["new data"]
    sh2= xw.sheets["margin"]
    hv= xw.sheets["hv"].range("A1:S100").value
    stAwt= xw.sheets["st awt"].range("A1:Z100").value
    st= xw.sheets["st"].range("A1:Z100").value
    margin = xw.sheets["margin"].range("A1:Z100").value
    trackVariance = xw.sheets["track variance"].range("A1:AI65").value

    namelist = []
    fullnames = []

    my_date_handler = lambda mm, ss, ff, **kwargs: "%02i-%02i-%02i" % (mm, ss, ff)
    endRow=sh.cells(1048576, 1).end(Direction.xlUp).row
    finishTime=sh.range("s2:s" +str(endRow)).value
    winingTime = sh.range("X2:X" + str(endRow)).value
    SpeedRating = sh.range("AB2:AF" + str(endRow)).value
    Distance = sh.range("H2:H" + str(endRow)).value
    lbw = sh.range("O2:O" + str(endRow)).value
    horseName=sh.range("A2:A" + str(endRow)).value

    cdate = sh.range("D2:D" + str(endRow)).value
    Course = sh.range("E2:E" + str(endRow)).value
    Track = sh.range("F2:F" + str(endRow)).value
    classm=sh.range("J2:J" + str(endRow)).value




    raceIndex=sh.range("B2:C" + str(endRow)).value

    for i ,val in enumerate(Distance):
        if not val is None:
            try:
                tv=Course[i] if not str(Track[i]).strip().lower() == "awt" else "awt"
                if str(Course[i]).replace(" ", "").upper() == "HV":
                    SpeedRating= CalCulations(finishTime, i, hv, int(val),SpeedRating,winingTime,trackVariance,tv,classm[i],raceIndex[i],lbw[i],margin)
                elif str(Course[i]).replace(" ", "").upper() + str(Course[i]).replace(" ","").upper() == "STAWT" or "AWT" in str(Course[i]).replace(" ", "").upper() or "AWT" in str(Track[i]).replace(" ","").upper():
                    SpeedRating=CalCulations(finishTime, i, stAwt, int(val),SpeedRating,winingTime,trackVariance,tv,classm[i],raceIndex[i],lbw[i],margin)
                else:
                    SpeedRating=CalCulations(finishTime, i, st, int(val),SpeedRating,winingTime,trackVariance,tv,classm[i],raceIndex[i],lbw[i],margin)
            except Exception as e:
                print("NEw Re",e)
                pass

    for array in MissingHorses:
        k=array[0]
        SpeedRating[k][0] = getIndex(array[1], array[2], array[3], margin)

        try:
            SpeedRating[k][3] = int(float(SpeedRating[k][1])) - int(float(SpeedRating[k][2]))
        except  Exception as e:
            print("eRR 2", e)
            pass

        try:
            if "-" in str(SpeedRating[k][3]):
                SpeedRating[k][4] = int(float(SpeedRating[k][0])) + int(float(str(SpeedRating[k][3]).replace("-", "")))
            else:
                SpeedRating[k][4] = int(float(SpeedRating[k][0])) - int(float(str(SpeedRating[k][3]).replace("-", "")))
        except  Exception as e:
            print("eRR 3", e)
            pass


    sh.range("AB2:AF" + str(endRow)).value=SpeedRating
