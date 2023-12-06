
import os
import sys

import xlwings as xw
import requests
from xlwings.constants import Direction


userag='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77'



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


def getMAtch(toclass,todist,toCourse,fromClass,fromdist,fromCourse,res,track,row1,row3,names,nn):
    toCourse=str(toCourse).lower()

    changeable = ["5", "op m","m", "r", "nov"]

    if not(toCourse =="sc" or toCourse =="lc"):
        toCourse="py"

    for index ,cl in enumerate(fromClass):
        if str(names[index]).lower().strip() == str(nn).lower().strip() :

            nclass = cl
            res[index][1] = ""
            if  str(cl).replace(".0","").strip().lower() in changeable and str(toclass).replace(".0","").strip() in changeable:
                nclass=toclass


            try:
               # if not toCourse == fromCourse[index]:
                print(getrate(nclass,toCourse,todist,track ,False),getrate(cl,fromCourse[index],fromdist[index],track))
                res[index][0] =  round(getrate(nclass,toCourse,todist,track ,False)) - round(getrate(cl,fromCourse[index],fromdist[index],track))

               # if not toCourse == fromdist[index]:
               #     res[index][1] =  round(getrate(cl, toCourse, todist, track,False)) -round(getrate(cl, fromCourse[index], fromdist[index], track))


            except Exception as e:
                print("ww",e)

            try:
                # print(row1[index], res[index][1],"  ",row3[index],int(res[index][1]))
                res[index][2]=round(row1[index]+res[index][0]) if round(row1[index]+res[index][0])>0 else "Nil"

            except:
                pass


            try:

                res[index][3]=round(row3[index]+res[index][0]) if round(row3[index]+res[index][0])>0 else "Nil"
            except:
                pass
    pass







if __name__=="__main__":
    datelist = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardDatelist/8"
    murl = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardTabledetail/en/"
    races = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardRaceno/"

    toclass=sys.argv[1]
    todist=sys.argv[2]
    toCourse=sys.argv[3]
    nn=sys.argv[4]
    PATH = sys.argv[5]

    # toclass='m'
    # todist="1000"
    # toCourse="py"
    # nn="MAGIC MASTER"
    # PATH =r"C:\Users\ABDULLAH\Desktop\FreeLancing\Fiver\Fiver Python\Fiver_Eric_Populate_Class_Helper\TurfClub.xlsx"

    print(toclass,todist,toCourse,nn,PATH)
    wk = xw.Book(PATH)


    sheet=xw.sheets["Database"]
    track = xw.sheets["track variance"].range("A1:CT100").value

    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row


    fromClass = sheet.range("D2:D" + str(endRow)).value
    fromdist = sheet.range("J2:J" + str(endRow)).value
    fromCourse = sheet.range("I2:I" + str(endRow)).value
    names=sheet.range("N2:N" + str(endRow)).value
    res = sheet.range("AT2:AW" + str(endRow)).value
    row1 = sheet.range("AP2:AP" + str(endRow)).value
    row3 = sheet.range("AS2:AS" + str(endRow)).value

    try:
        getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse, res, track, row1, row3,names,nn)
        sheet.range("AT2:AW" + str(endRow)).value = res


    except Exception as e:
        print("Error 2", e)



