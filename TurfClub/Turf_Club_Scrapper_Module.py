# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import  datetime as dt
import xlwings as xw
import requests


# sending get request and saving the response as response object
# r=s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77'})
# reply=r.json()


def addvalue(dic,value):
    vv=""
    try:
        vv=str(dic[value]).replace("None","")
    except Exception as e:
        print(e,"While adding")
    return vv

class myvalues:
    def __init__(self):
        self.a1=""
        self.a2=""
        self.a3 = ""
        self.a4 = ""
        self.a5 = ""
        self.a6 = ""
        self.a7 = ""
        self.a8 = ""
        self.a9=""
        self.a10 = ""
        self.a11 = ""
        self.a12 = ""
        self.a13 = ""
        self.a14 = ""
        self.a16 = ""
        self.a17 = ""
        self.a18 = ""
        self.v1=""
        self.v2 = ""

    def reset(self):
        self.a1 = ""
        self.a2 = ""
        self.a3 = ""
        self.a4 = ""
        self.a5 = ""
        self.a6 = ""
        self.a7 = ""
        self.a8 = ""
        self.a9 = ""
        self.a10 = ""
        self.a11 = ""
        self.a12 = ""
        self.a13 = ""
        self.a14 = ""
        self.a16 = ""
        self.a17 = ""
        self.a18 = ""
        self.v1 = ""
        self.v2 = ""


def requesting(req,s,userag,url):
    json = ""
    flag= True
    counter=1
    while flag:
        try:
            r = s.get(req, headers={'User-Agent': userag})
            json = r.json()
            flag=False
        except Exception as e:
            print(req,e)
            s.close()
            time.sleep(2)
            s = requests.Session()
            try:
                r = s.get(url, headers={'User-Agent': userag})
                json    =r.json()
            except:
                print("two level failure ")

            counter+=1

            if counter>4:
                break

    return json ,s


def excel_date(date1):
    temp = dt.datetime(1899, 12, 30)
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def getAllDates(month, year, presentDates, cumonth, cuyear):
    finalizedates = []
    s = requests.Session()
    while True:
        if month == 13:
            month = 1
            year += 1

        ur = f"https://api.turfclub.com.sg/api/v1/racing/stc/getRaceResultDatelistCalendar/{year}/{int(month)}"
        print(ur)
        r = s.get(ur, headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 Edg/103.0.1264.77'})
        reply = r.json()
        # print(r,reply)

        for data in reply['Data']:
            dat=str(data["racedate"]).split("-")
            exdate=str(excel_date(dt.datetime(int(dat[0]), int(dat[1]), int(dat[2]))))
            # print(exdate)
            if not exdate in presentDates:
                print("missing",data['racedate'])
                finalizedates.append(data['racedate'])

        if str(month).zfill(2) == str(cumonth).zfill(2) and str(year) == str(cuyear):
            break
        month += 1
    return finalizedates


def gettimevalue(val):
    s=str(val).replace("None","")

    if not str(val) =="None"  or str(val) == "0" :
        s = str(val).zfill(6)
        s = s[:2]+":" + s[2:4] + "." + s[4:6]
    return s


def SCRAP_Turf_Club_Data(Address,userag):
    print("Processing")
    presentDates = []
    datet = dt.date.today()
    # Current dates
    cumonth = datet.strftime("%m").lower().strip()
    cuyear = datet.strftime("%Y").strip()

    wk = xw.Book(Address)

    sh = xw.sheets["Database"]
    sh2 = xw.sheets["Settings"]

    s = requests.Session()

    counter =sh.range(f"A1048576").end('up').row + 1

    cuy = 2015
    cum = 1
    ur = f"https://api.turfclub.com.sg/api/v1/racing/stc/getRaceResultDatelistCalendar/{cuy}/{cum}"



    url = "https://api.turfclub.com.sg/api/v1/racing/stc/getRaceResultDatelistCalendar/2016/04"

    raceid = "https://api.turfclub.com.sg/api/v1/racing/result/racenos/single/"
    url2 = "https://api.turfclub.com.sg/api/v1/racing/result/header/en"
    url3 = "https://api.turfclub.com.sg/api/v1/racing/result/raceresult/en"
    video = "https://api.turfclub.com.sg/api/v1/racing/result/video/en"


    # start date
    month = int(sh2.cells(1, 2).value)
    year = int(sh2.cells(1, 3).value)

    # all dates in sheet

    values=sh.range(f"A1:A{counter}").value
    for val  in values:
        if not val is None and not val in presentDates:

            if "-" in str(val):
                arr= str(val).split(" ")
                arr=arr[0].split("-")
                presentDates.append(str(excel_date(dt.datetime(int(arr[0]), int(arr[1]), int(arr[2])))))
            else:
                presentDates.append(val)


    # remainin dates

    alldates=getAllDates(month,year,presentDates,cumonth,cuyear)

    for index, data in enumerate(alldates):
        try:
            cudate=str(data)
            dat=cudate.split("-")
            exdate = excel_date(dt.datetime(int(dat[0]), int(dat[1]), int(dat[2])))
            ids ,s = requesting(raceid + cudate,s,userag,url)
            print(cudate)
            val = myvalues()
            for id in ids["Data"]:
                cuid=id["RACEID"]
                cuno=id['RACENO']
                headerdata,s=requesting(f"{url2}/{cudate}/{cuno}",s,userag,url)
                maindata,s=requesting(f"{url3}/{cudate}/{cuid}", s,userag,url)
                val.reset()
                if len(headerdata["Data"])>0:
                    headerdataJ=headerdata["Data"][0]
                    maindataJ=maindata["Data"]
                    val.a1=cudate
                    val.a2=addvalue(headerdataJ,"lb_raceno")
                    val.a3 = addvalue(headerdataJ, "lb_starttime")
                    val.a4 = addvalue(headerdataJ, "RACECLASS")
                    val.a5 = addvalue(headerdataJ, "lb_racedivision")
                    val.a6 = addvalue(headerdataJ, "finishedtime")
                    val.a7 = addvalue(headerdataJ, "TRACKTYPE").replace("TRACK","")
                    val.a8 = addvalue(headerdataJ, "TRACKTYPECODE")
                    val.a9 = addvalue(headerdataJ, "COURSE")
                    val.a10 = addvalue(headerdataJ, "RACEDIST")

                    val.a12 = addvalue(headerdataJ, "lb_raceno")


                    if "poly" in str(val.a7).lower():
                        val.a11 = addvalue(headerdataJ, "tc_turf_rating")
                    else:
                        val.a11 = addvalue(headerdataJ, "tc_turf_rating")

                    val.a12 = addvalue(headerdataJ, "twr_polytrack_surface_temperature")

                    for data in maindataJ:
                        # print(data)
                        sh.cells(counter, 1).value  = exdate
                        sh.cells(counter, 2).value = val.a2
                        sh.cells(counter, 3).value = val.a3
                        sh.cells(counter, 4).value = val.a4
                        sh.cells(counter, 5).value = val.a5
                        sh.cells(counter, 6).value = gettimevalue(maindataJ[0]["finishedtime"])
                        sh.cells(counter, 7).value = val.a7
                        sh.cells(counter, 8).value = val.a8
                        sh.cells(counter, 9).value = val.a9
                        sh.cells(counter, 10).value = val.a10
                        sh.cells(counter, 11).value = val.a11
                        sh.cells(counter, 12).value = val.a12
                        try:
                            data["prev_wt"] = 0 if str(data["prev_wt"]) == "None" else data["prev_wt"]
                            data["currwt"] = 0 if str(data["currwt"]) == "None" else data["currwt"]
                            lbw= data["sectional"].split("<br/>")[1] if "<br/>" in data["sectional"] else ""
                            lbw=lbw.replace(")","").replace("(","")
                            data["sectional"]= data["sectional"].split("<br/>")[0] if "<br/>" in data["sectional"] else data["sectional"]
                            sh.cells(counter, 13).value = data["placing"] if not data["placing"] is None else ""
                            sh.cells(counter, 14).value = data["horsename"] if not data["horsename"] is None else ""
                            sh.cells(counter, 15).value = data["currwt"] if not data["currwt"] is None else ""
                            sh.cells(counter, 16).value = (data["currwt"] -data["prev_wt"])
                            sh.cells(counter, 17).value = data["barrier"] if not data["barrier"] is None else ""
                            sh.cells(counter, 18).value = data["gear"] if not data["gear"] is None else ""
                            sh.cells(counter, 19).value = gettimevalue(data["besttime"]) if not data["besttime"] is None else ""
                            sh.cells(counter, 20).value = data["last400mPl"] if not data["last400mPl"] is None else ""
                            sh.cells(counter, 21).value = data["rating"] if not data["rating"] is None else ""
                            sh.cells(counter, 22).value = data["proven_wt"] if not data["proven_wt"] is None else ""
                            sh.cells(counter, 23).value = data["jockeyname"] if not data["jockeyname"] is None else ""
                            sh.cells(counter, 24).value = data["cwt"] if not data["cwt"] is None else ""
                            sh.cells(counter, 25).value = data["handicapwt"] if not data["handicapwt"] is None else ""
                            sh.cells(counter, 26).value = data["trainername"] if not data["trainername"] is None else ""
                            sh.cells(counter, 27).value = data["owner"] if not data["owner"] is None else ""
                            sh.cells(counter, 28).numberFormat = "@"
                            sh.cells(counter, 28).value = "'" + str(data["sectional"]) if not data["sectional"] is None else ""

                            sh.cells(counter, 29).value =  lbw
                            sh.cells(counter, 30).value = gettimevalue(data["finishedtime"])
                            sh.cells(counter, 31).value = "'" + str(data["margin"]) if not data["margin"] is None else ""
                            sh.cells(counter, 32).value = data["comment"] if not data["comment"] is None else ""
                        except Exception as e:
                            print("Inner level error")
                        counter += 1

        except Exception as e:
            print(f" Error {e}")
            wk.save()




    wk.save()
    print("Done")