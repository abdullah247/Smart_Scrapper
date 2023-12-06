import sys

import xlwings as xw
import re
import os
import datetime as dt

from xlwings.constants import Direction

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


trackStart = {
    "sc": 4,
    "lc": 14,
    "py": 28
}
def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def getIndex(srat, lbw, dist, orignal,marginSheet):
    lbw = str(lbw).replace("'","")
    if lbw is None:
        return orignal
    lbw = lbw.strip()
    if str(lbw).strip() == "-" or len(str(lbw).strip()) < 1:
        return 0
    else:
        for col in range(1, 26):
            try:
                if not marginSheet[1][col] is None:
                    if int(dist) == int(marginSheet[1][col]):
                        for row in range(2, 90):
                            if not marginSheet[row][0] is None:
                                if str(marginSheet[row][0]).strip() == str(lbw).strip():
                                    # print(srat,margin[row][col])
                                    return srat - marginSheet[row][col]
                                else:
                                    if has_numbers(lbw) and has_numbers(str(marginSheet[row][0]).replace("'","")):
                                        if float(lbw) < float(str(marginSheet[row][0])):
                                            if marginSheet[row - 1][col] is None:
                                                return srat - marginSheet[row][col]
                                            else:

                                                return srat - marginSheet[row - 1][col]





            except Exception as e:
                # print("EE",e)
                pass

    return 0

def getTurnValue(turn, param, dist):

    flag = 1
    try:
        myval = float("".join(param.replace(":", "").rsplit(".", 1)))

        for i in range(29):
            # print(turn.range(1,flag).value ,f"{val}m",turn.range(1,flag).value == f"{val}m")
            if turn[0][flag] == f"{dist}m":
                break
            flag = flag + 3

        current = turn[1][flag]

        for i in range(1, 150):
            if not turn[i][flag - 1] is None:
                val = turn[i][flag - 1]
                # print(val)
                comp = float("".join(val.replace(":", ".").rsplit(".", 1)))

                # print(myval ,comp,myval ==comp,comp>myval)
                if myval == comp:
                    current = turn[i][flag]
                elif comp > myval:
                    current = turn[i - 1][flag]

                    return current
    except Exception as e:
        # print("eRR 4",e,param,dist)
        return ""

    pass

def getTrackVarianxe(track, distance, mclass,trackVariance):
    try:
        track = str(track).lower().strip()
        mclass = str(mclass).lower().strip().replace(" ", "").replace("none", "py").replace(".0","")
        st = trackStart[track] - 1

        trak = -1
        for i in range(2, len(trackVariance[0]), 4):
            # print(st,i,track, str(trackVariance.cell((st - 2), i).value).replace(" ","").strip().lower(), mclass, trackVariance.cell(st, i).value)
            val = trackVariance[st - 2][i]
            if type(val) == float:
                val = str(int(val))
            if str(val).replace(" ", "").strip().lower() == mclass:
                # print(track,trackVariance.cell(st-2,i).value,mclass,trackVariance.cell(st,i).value)
                trak = i + 2
                break

        # print(track,trackStart[track])
        for i in range(0, 75):
            # print("asdfa ",trackVariance.cell(st+i,2).value,st,trackClass[mclass])
            # print(trackVariance.cell(st + i, 3).value,distance,mclass)
            if float(trackVariance[st + i][2]) == float(distance):
                # print("tt",trackVariance.cell(st+i,trak).value)
                return trackVariance[st + i][trak]
    except Exception as e:
        # print("Track Error" ,e)
        return ""
    return ""

    pass

def format_result(result):
    x = result  # a float
    x = int(x * 24 * 3600)  # convert to number of seconds
    y = result * 24 * 3600 - int(result * 24 * 3600)
    y = round(y * 100) * 10000
    # print(y)
    if y >= 1000000:
        y = 999999
    my_time = dt.time(0, (x % 3600) // 60, x % 60, y)
    return my_time

def CalCulations(sh, k, turn, val, SpeedRating,marginSheet,trackVariance):
    # print("as",sh.cell(k, 30).value)
    if len(str(sh[29]).replace("-", "").strip()) > 2:
        # print( str(sh.cell(k, 30).value))

        wtime = (format_result(sh[5]).strftime("%M.%S.%f")) if (
                not "-" in str(sh[5]) or not sh[5] is None) else ""
        # print(wtime)
        wrat = getTurnValue(turn, wtime, val)
        SpeedRating[1] = wrat

        atime = (format_result(sh[29]).strftime("%M.%S.%f")) if (
                    not "-" in str(sh[29]) or not sh[29] is None) else ""

        srat = getTurnValue(turn, atime, val)
        SpeedRating[0] = srat
        margin = sh[28]
        if int(float(str(sh[12]).lower().replace("dh", "").strip())) == 1:
            SpeedRating[0] = srat
        else:
            SpeedRating[0] = getIndex(wrat, margin, val, srat,marginSheet)

    tv = sh[8]
    if tv is None or len(str(tv).strip()) < 1:
        tv = "py"
    tv = str(tv).lower()
    SpeedRating[2] = getTrackVarianxe(tv, val, sh[3],trackVariance)
    try:
        SpeedRating[3] = int(SpeedRating[1]) - int(SpeedRating[2])
    except  Exception as e:
        # print(e)
        pass

    try:
        if "-" in str(SpeedRating[3]):
            SpeedRating[4] = int(SpeedRating[0]) + int(str(SpeedRating[3]).replace("-", ""))
        else:
            SpeedRating[4] = int(SpeedRating[0]) - int(str(SpeedRating[3]).replace("-", ""))

    except:
        pass


def TurfClubHTMLSOLVER(address):



    filename = os.path.join(address)

    wk =  xw.Book(filename)
    sh = xw.sheets["Database"]
    marginSheet = xw.sheets["margin"].range("A1:Z200").value
    trackVariance = xw.sheets["track variance"].range("A1:CT100").value
    SC= xw.sheets["sc"].range("A1:Z250").value
    LC = xw.sheets["lc"].range("A1:Z250").value
    PY = xw.sheets["py"].range("A1:Z250").value



    endRow = sh.cells(1048576, 1).end(Direction.xlUp).row
    AllData = sh.range("A2:AE" + str(endRow)).value
    SpeedRating = sh.range("AJ2:AN" + str(endRow)).value
    for index,row in enumerate(AllData):
        if not row[9] is None:
            try:
                if str(row[8]).replace(" ","").upper() =="SC":

                        CalCulations(AllData[index], index, SC, int(str(row[9]).replace("M","")),SpeedRating[index],marginSheet,trackVariance)

                elif str(row[8]).replace(" ","").upper() =="LC":
                        CalCulations(AllData[index], index, LC, int(str(row[9]).replace("M","")),SpeedRating[index],marginSheet,trackVariance)
                else:
                    CalCulations(AllData[index], index, PY,int(str(row[9]).replace("M","")),SpeedRating[index],marginSheet,trackVariance)
            except:
                pass


    sh.range("AJ2:AN" + str(endRow)).value = SpeedRating








