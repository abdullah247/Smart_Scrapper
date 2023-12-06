import os
import requests
import xlwings as xw
from bs4 import BeautifulSoup
from xlwings.constants import Direction

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
            if ssss  in str(val).replace(" ", "").strip().lower()  :
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


def getMAtch(toclass, todist, toCourse, fromClass, fromdist, fromCourse1,fromCourse2, res, track, row1, row3):
    toCourse = str(toCourse).lower().strip()
    changeable = ["5", "op m", "m", "r", "nov"]



    if not str(fromCourse1).lower().strip() == "ch":
        nclass = fromClass
        res[1] = ""
        if str(fromClass).replace(".0", "").strip().lower() in changeable and str(toclass).replace(".0",
                                                                                            "").strip() in changeable:
            nclass = toclass

        if str(fromCourse1).lower().strip() == "st":
            fcourse = "st"
            if not str(fromCourse2).lower().strip() == "turf":
                fcourse = "awt"
        else:
            fcourse="hv"

        try:
            # if not toCourse == fromCourse[index]:
            #  print(getrate(nclass,toCourse,todist,track ,False),getrate(cl,fromCourse[index],fromdist[index],track))
            res[0] = round(getrate(nclass, toCourse, todist, track, False)) - round(
                getrate(fromClass, fcourse, fromdist, track))

        # if not toCourse == fromdist[index]:
        #     res[index][1] =  round(getrate(cl, toCourse, todist, track,False)) -round(getrate(cl, fromCourse[index], fromdist[index], track))

        except Exception as e:
            print("ww", e)

        try:
            # print(row1[index], res[index][1],"  ",row3[index],int(res[index][1]))
            res[1] = round(row1 + res[0]) if round(row1 + res[0]) > 0 else "Nil"

        except:
            pass

        try:
            res[2] = round(row3 + res[0]) if round(row3 + res[0]) > 0 else "Nil"
        except:
            pass



def export(sheet,horses,data,courseData,track,noOfHorses):
    flag = True
    endRow = sheet.cells(1048576, 1).end(Direction.xlUp).row
    sh =  sheet.range("A2:BJ" + str(endRow)).value

    horsesrow = {}
    for hors in horses:
        horsesrow[hors] = []
    for index,row in enumerate(sh):
        if str(row[0]).strip() in horses:
            horsesrow[row[0]].append(index)
            if len(horsesrow[row[0]]) > noOfHorses:
                a = horsesrow[row[0]].pop(0)


    csh2 = xw.sheets["raceList"]

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
                    if i==11  or i==14 :
                            sh2[counter][i] ="'" +str(sh[row][i])

                    else:
                        sh2[counter][i] = sh[row][i]

                res=[sh2[counter][39],sh2[counter][40],sh2[counter][41]]
                try:
                    getMAtch(toclass, todist, toCourse, sh2[counter][9], sh2[counter][7],sh2[counter][4], sh2[counter][5], res, track, sh2[counter][33], sh2[counter][37])
                except Exception as e:
                    print(e)

                sh2[counter][39]=res[0]
                sh2[counter][40]=res[1]
                sh2[counter][41]=res[2]

                counter = counter + 1

            if flag:
                counter += 1


            counter=counter+3






    csh2.range("A2:BJ90000").value = sh2
    csh2.range("S2:S90000").number_format = "mm:ss.00"
    csh2.range("X2:X90000").number_format = "mm:ss.00"

def hkHandiCap(address,userag,curl,noofhorses=5):
    if len(curl)<0:
        url="https://racing.hkjc.com/racing/information/English/racing/Entries.aspx"
    else:
        url=curl


    s = requests.Session()


    filename = address
    wk = xw.Book(filename)

    sheet=xw.sheets["new data"]
    track = xw.sheets["track variance"].range("A1:CT100").value


    counter = 2



    counter=1
    allHorses=[]
    horses={}
    details={}

    # print(url,noofhorses)

    r = s.get(str(url).strip(), headers={'User-Agent': userag})




    parsedWebPage = BeautifulSoup(r.content, "html.parser")


        # print(arryAnchor)
    tbl = parsedWebPage.find("table", {"id": "trainersInfo"})
    coursename=str(parsedWebPage.find("div", {"class": "f_fs14"}).text).lower()
    head=tbl.find("thead").find_all("tr")
    names=tbl.find("tbody").find_all("tr")

    for i ,val in enumerate(names):

        for j ,hor in enumerate(val.find_all("td")):

            if j>0 and len(hor.find_all("a"))>0:
                todist=str(head[3].find_all("td")[j].text).lower().replace("m","")
                toclass=head[1].find_all("td")[j].text
                if "awt" in str(head[5].find_all("td")[j].text).lower():
                    tocourse="awt"
                elif "sha tin" in coursename:
                    tocourse = "st"
                else:
                    tocourse = "hv"


                for anch in hor.find_all("a"):


                    horseName=str(anch.text).replace("*","").replace("+","").replace("#","").replace("\xa0"," ").replace("2","").strip()
                    horseName = horseName.replace(" 2","").replace(" R1","").replace(" R2","")
                    allHorses.append(horseName)

                    details[j] =[toclass,todist,tocourse]
                    # j is the key as horses is a dictionary
                    if j in horses:
                        horses[j].append(horseName)

                        # print(horses[j],"as",j)
                    else:
                        horses[j] =[horseName]



    # print("vals",horses,details)
    export(sheet, allHorses, horses, details, track,noofhorses)

    # print("Finish")





