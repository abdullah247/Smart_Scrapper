
import sys
import re
import requests
from bs4 import BeautifulSoup
import xlwings as xw

mycourse={
    "happy valley" :"HV",
    "sha  tin":"ST"
}


def getGoing(track,going):

    out=""
    arr = str(going).upper().strip().split(" ")
    if len(arr)>1:
        out = arr[0][0] + arr[-1][0]
    elif track=="AWT":
            out=arr[0][0] +arr[0][-1]

    else:
        out = arr[0][0]

    return out


def getPage(s,date,userag):
    if date == "":
        url = f"https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx"
    else:
        url = f"https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={date}"

    # print("ss",url )
    r = s.get(url, headers={'User-Agent': userag})
    parsedWebPage = BeautifulSoup(r.content, "html.parser")
    return  parsedWebPage

def getTotalRacesDefault(s,url,userag):
    r = s.get(url, headers={'User-Agent': userag})
    parsedWebPage = BeautifulSoup(r.content, "html.parser")
    Races = len(parsedWebPage.find("table", {"class": "js_racecard"}).find("tr").find_all("img"))
    return str(Races)

def getTotalRaces(s,date,userag):
    parsedWebPage = getPage(s,date,userag=userag)
    Races = len(parsedWebPage.find("table", {"class": "js_racecard"}).find("tr").find_all("img"))
    return str(Races)

def getCourse(parsedWebpage):
    row = parsedWebpage.find("table", {"class": "js_racecard"}).find("tr")
    course = str(row.find("td").text).strip().replace(":", "").replace("\n","").strip().upper()
    arr=course.split(" ")
    cor=""
    for cr in arr:
        cor=cor+cr[0]
    return cor



def getDate(s,userag):
    url = f"https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx"
    r = s.get(url, headers={'User-Agent': userag})
    pp = BeautifulSoup(r.content, "html.parser")
    ar = pp.find("select", {"id": "selectId"}).find('option', selected=True).text
    arr = ar.split("/")
    date = arr[2] + "/" + arr[1] + "/" + arr[0]
    return date




def getAllHorseDetails(s,date,raceNo,sheet,userag,flag=True):



    sheet.range("O2:O1048574").NumberFormat ="@"
    last_row = sheet.range("A1048575").end('up').row
    # print(course)
    if flag:
        date = date.replace("\n", "").strip()
        course = getCourse(getPage(s, date, userag))
        url = f"https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={date}&Racecourse={course}&RaceNo={raceNo +1}"
    else:
        url=date.replace("RaceNo=1",f"RaceNo={raceNo+1}")
        # getRaceCourse
        smallurl=url.lower()
        course=smallurl.split("racecourse=")[1].split("&raceno=")[0].strip()
        date=smallurl.split("racedate=")[1].split("&racecourse=")[0].strip()

    print(url)
    resultsArray=[]

    try:

        r = s.get(url, headers={'User-Agent': userag})
        parsedWebPage = BeautifulSoup(r.content, "html.parser")



        table = parsedWebPage.find("div", {"class": "performance"})

        tb2=parsedWebPage.find("div", {"class": "race_tab"})

        race=str(tb2.find("td").text).replace(" ","").lower().split("(")[1].replace(")","").replace("-","")
        tbrows=tb2.find_all("tr")

        row2=tbrows[2]

        distancearray=re.findall("\d*M", str(row2.find("td").text).upper())
        rtgArray=re.findall("\(\d*", str(row2.find("td").text).upper())
        raceClassArray=re.findall("CLASS*\s+\d", str(row2.find("td").text).upper())
        parahs=tb2.find_all("p")

        goingtd=row2.find_all("td")
        gpong=str(goingtd[len(goingtd)-1].text).strip().replace("\n","")
        tracktd=tbrows[3].find_all("td")

        maintrack=str(tracktd[len(tracktd)-1].text).strip().replace("\n","")
        if "ALL WEATHER TRACK" in maintrack:
            track="AWT"
            courseALL=""
        else:
            arr = re.findall("\S+", maintrack)
            if len(arr)>0:
                track=arr[0]
            else:
                track="TURF"
            arr = re.findall("\".*\"", maintrack)

            if len(arr) > 0:
                courseALL = arr[0]
            else:
                courseALL = ""



        video1="--"
        video2="--"
        # print(parahs[len(parahs) - 1].prettify())
        if len(parahs)>0:
            for anc in parahs[len(parahs) - 1].find_all("a"):
                if video1=="--":
                    # print(anc["href"])
                    video1="https://racing.hkjc.com/"+anc["href"]
                else:
                    # print(anc["href"])
                    video2="https://racing.hkjc.com/"+anc["href"]

                    break


        if len(distancearray)>0:
            distance=distancearray[0].replace("M","")
        else:
            distance="--"
        # print(distance)
        if len(rtgArray)>0:
            rtg=rtgArray[0].replace("(","")
        else:
            rtg="--"
        # print(rtg)
        if "GROUP ONE" in str(row2.find("td").text).upper():
            raceClass ="G1"
        elif "GROUP TWO" in str(row2.find("td").text).upper():
            raceClass = "G2"
        elif "GROUP THREE" in str(row2.find("td").text).upper():
            raceClass = "G3"
        elif "GRIFFIN" in str(row2.find("td").text).upper():
            raceClass="Griffin"
        elif len(raceClassArray)>0:
            raceClass=re.sub("\S+\s+","",raceClassArray[0])
        else:
            raceClass = "--"
            arr= str(row2.find("td").text).strip().replace("Race","").strip().split(" ")
            if len(arr)>=1:
                raceClass=arr[0]



        # print(course)


        tablebody = table.find("tbody")
        trs = tablebody.find_all("tr")

        winnertime=str(trs[0].find_all("td")[10].text).replace(":",".").replace(".",":",1)
        # print(winnertime)
        for tr in trs:

            result = []

            result.append(str(tr.find_all("td")[2].find("a").text))
            link=""
            try:
                link="https://racing.hkjc.com/" + tr.find_all("td")[2].find("a")["href"]
            except Exception as e :
                print(f"Gear Address Error {e}")
                pass
            result.append(race)

            result.append(str(tr.find_all("td")[0].text) )
            # print(result)
            # time
            result.append(str(date))


            #rc st
            result.append(course)

            #track turf
            result.append(track)
            # course
            result.append(courseALL)
            #dist
            result.append(distance)
            # g
            result.append(getGoing(track,gpong))
            # RaceClass
            result.append(raceClass)

            # dr
            result.append(str(tr.find_all("td")[7].text) )


            # rtg
            # result.append(rtg)
            result.append("")


            #trainer
            result.append(str(tr.find_all("td")[4].text).strip().replace("\n",""))

            # Jockey
            result.append(" " +str(tr.find_all("td")[3].text).strip().replace("\n",""))

            # Lbw
            result.append("'"+str(tr.find_all("td")[8].text).strip().replace("\n",""))


            # Win odds
            result.append(str(tr.find_all("td")[11].text).strip().replace("\n","") )

            # actual weight
            result.append(str(tr.find_all("td")[5].text).strip().replace("\n","") )


            # runing position
            try:
                mainpos=tr.find_all("td")[9].find("div")
                val=""
                for pos in mainpos.find_all("div"):

                    val=val + str(pos.text).strip() +" "

                result.append(val.strip())
            except Exception as e:
                result.append(str(tr.find_all("td")[9].text).strip().replace("\n",""))


            # finish time
            result.append(str(tr.find_all("td")[10].text).replace(":",".").replace(".",":",1).strip().replace("\n",""))

            #declare Weight
            result.append(str(tr.find_all("td")[6].text).strip().replace("\n",""))


            # gear
            result.append(link)

            # video1
            result.append(video1)

            # video2
            result.append(video2)
            # winner time
            result.append(winnertime.strip().replace("\n",""))
            # print(result)
            resultsArray.append(result)

    except Exception as E:
        print(E)
        # return "&&" +str(E)
        return  "&&"

    last_cell = sheet.range("A1048576").end('up')

    # Determine the row where the new data should be added
    next_row = last_cell.row + 1

    # Specify the target range for the new data
    target_range = f"A{next_row}"

    # Write the new data to the specified range
    sheet.range(target_range).value = resultsArray


def ScrapLatest(Address,userarg,dt=""):


    s = requests.Session()

    xw.Book(Address)

    sheet=xw.sheets["new data"]
    if len(dt)<1:
        dt=getDate(s,userarg)
        ttlraces = getTotalRaces(s, dt, userarg)
        for i in range(0, int(ttlraces)):
            a = getAllHorseDetails(s, date=dt, raceNo=i, sheet=sheet, userag=userarg)
    else:
        ttlraces = getTotalRacesDefault(s, dt, userarg)
        for i in range(0, int(ttlraces)):
            a = getAllHorseDetails(s, date=dt, raceNo=i, sheet=sheet, userag=userarg,flag=False)


    print(dt,ttlraces)




