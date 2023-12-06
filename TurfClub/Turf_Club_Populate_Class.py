import os

import xlwings as xw
import requests
from xlwings.constants import Direction



data={

    "r1": [],
    "r2": [],
    "r3": [],
    "r4": [],
    "r5": [],
    "r6":[],
    "r7": [],
    "r8": [],
    "r9": [],
    "r10": [],
    "r11": [],
    "r12": [],
    "r13": []

}

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


def getMAtch(toclass,todist,toCourse,fromClass,fromdist,fromCourse,res,track,row1,row3):
    toCourse=str(toCourse).lower()

    changeable = ["5", "op m","m", "r", "nov"]

    if not(toCourse =="sc" or toCourse =="lc"):
        toCourse="py"

    for index ,cl in enumerate(fromClass):

        nclass = cl
        res[index][1] = ""
        if  str(cl).replace(".0","").strip().lower() in changeable and str(toclass).replace(".0","").strip() in changeable:
            nclass=toclass


        try:
           # if not toCourse == fromCourse[index]:
           #  print(getrate(nclass,toCourse,todist,track ,False),getrate(cl,fromCourse[index],fromdist[index],track))
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

def clearSheeets(xw):
    for key in data:
        xw.sheets[key].range("A2:BJ500").clear()




def TurfCLUBPopulateClass(Address,userag):
    datelist = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardDatelist/8"
    murl = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardTabledetail/en/"
    races = "https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardRaceno/"

    s = requests.Session()
    r = s.get(datelist, headers={'User-Agent': userag})
    datelistjson = r.json()
    mdate = datelistjson["Data"][0]["racedate"]

    r = s.get(f"{races}{mdate}", headers={'User-Agent': userag})
    racesjson = r.json()

    races = racesjson["Data"]
    horses = []

    for index, race in enumerate(races):
        r = s.get(f"{murl}{mdate}/{race['raceno']}", headers={'User-Agent': userag})
        print(f"{murl}{mdate}/{race['raceno']}")
        namesjson=r.json()
        for names in namesjson["Data"]:
            # print(names["horsename"])
            horses.append(names["horsename"])
            data[f"r{index+1}"].append(names["horsename"])


    wk = xw.Book(Address)
    sheet=xw.sheets["Database"]
    track = xw.sheets["track variance"].range("A1:CT100").value
    clearSheeets(xw)
    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row
    sh =  sheet.range("A2:BJ" + str(endRow)).value


    horsesrow = {}

    for hors in horses:
        horsesrow[hors] = []
    for index,row in enumerate(sh):
        if str(row[13]).strip() in horses:
            horsesrow[row[13]].append(index)
            if len(horsesrow[row[13]]) > 5:
                a = horsesrow[row[13]].pop(0)

    for key in data:
        csh2=xw.sheets[key]
        sh2=csh2.range("A2:BJ500").value
        counter = 0
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

                counter = counter + 1

            if flag:
                counter += 1

        csh2.range("A2:BJ500").value = sh2
        csh2.range("F2:F500").number_format="mm:ss.00"
        csh2.range("AD2:AD500").number_format = "mm:ss.00"
        raceNo=key.lower().replace("r","").strip()
        raceUrl = f"https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardHeader/en/{mdate}/" + raceNo
        response = s.get(raceUrl, headers={'User-Agent': userag})
        try:
            if response.status_code == 200:
                ndata = response.json()  # Parse the JSON response into a Python dictionary
                toclass = str(ndata['Data'][0]['raceclasscode']).lower().replace("class", "").strip()
                todist = str(ndata['Data'][0]['racedistcode']).lower().replace("m", "").strip()
                newurl = f"https://api.turfclub.com.sg/api/v1/racing/stc/getRacecardTabledetail/en/{mdate}/" + raceNo
                newreq = s.get(str(newurl).strip(), headers={'User-Agent': userag})
                newdat = newreq.json()
                toCourse = newdat['Data'][0]['course']


                endRow = csh2.cells(1048576, 1).end(Direction.xlUp).row
                fromClass = csh2.range("D2:D" + str(endRow)).value
                fromdist = csh2.range("J2:J" + str(endRow)).value
                fromCourse = csh2.range("I2:I" + str(endRow)).value
                res = csh2.range("AT2:AW" + str(endRow)).value
                row1 = csh2.range("AP2:AP" + str(endRow)).value
                row3 = csh2.range("AS2:AS" + str(endRow)).value

                try:
                    getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse, res, track, row1, row3)
                    csh2.range("AT2:AW" + str(endRow)).value = res


                except Exception as e:
                    print("Error 2", e)
                toCourse = str(toCourse).replace("None", "py")
                csh2.range("AS" + str(endRow + 3)).value = f"Class :{toclass} Distance : {todist} Course : {toCourse}"
                print(f"Race {raceNo} Finished")
            else:
                print(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Inside Error {e}")

