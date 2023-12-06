from selenium.webdriver.common.by import By

from SCMP.ScmpFunctions import moveleft, moveright, getmonth


def getDates(driver,startDate):
    GAMEDATES=[]
    rowcount = "Max"
    driver.find_element(By.CSS_SELECTOR,".ui-datepicker-trigger").click()
    driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-menu li")[0].click()
    while not str(driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-month")[0].text).strip() == "January":
        moveleft(driver)

    # change this to every year
    while not (str(driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-month")[1].text).strip() == "December" and str(
            driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-year")[0].text).strip() == "2023"):
        moveright(driver)
        moveright(driver)
        # time.sleep(1)
        tables = driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-calendar")


        for index, table in enumerate(tables):
            trs = table.find_elements(By.CSS_SELECTOR,"td.ui-state-enabled")

            for tr in trs:
                cdat = str(driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-year")[index].text).strip() +","+ str(getmonth(
                    driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-month")[
                        index].text)).zfill(2)+","+str(tr.find_element(By.CSS_SELECTOR,"a").text).strip().zfill(2)
                if not cdat in GAMEDATES:

                    if startDate is None  or startDate =="None" or len(startDate)<1 :


                        GAMEDATES.append(cdat)
                        rowcount="1"
                        print(1,cdat,startDate)
                    else:
                        arr = startDate.split("-")
                        print(arr)
                        arr[2]=arr[2].split(" ")[0]
                        arr2 = cdat.split(",")


                        if int(arr2[0])>=int(arr[0]) and int(arr2[1])>=int(arr[1]) and int(arr2[2])>=int(arr[2]):

                            # print(2, cdat, startDate,int(arr[0])>=int(arr2[0]),int(arr[1])>=int(arr2[1]),int(arr[2])>=int(arr2[2]),int(arr[2]),int(arr2[2]))
                            GAMEDATES.append(cdat)
                            print(2,cdat,startDate)



                    # print(cdat)
            # print(len(table.find_elements_by_css_selector("td.ui-state-current")),str(driver.find_elements_by_css_selector(".ui-datepicker-year")[index].text).strip() + "," + str(
            #         getmonth(driver.find_elements_by_css_selector(".ui-datepicker-month")[index].text)).zfill(
            #         2) )
            if len(table.find_elements(By.CSS_SELECTOR,"td.ui-state-current")) > 0:

                tl = table.find_elements(By.CSS_SELECTOR,"td.ui-state-current")[0]
                cd = str(driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-year")[index].text).strip() + "," + str(
                    getmonth(driver.find_elements(By.CSS_SELECTOR,".ui-datepicker-month")[index].text)).zfill(
                    2) + "," + str(tl.find_element(By.CSS_SELECTOR,"a").text).strip().zfill(2)
                arr2 = cd.split(",")
                print(cd)
                if int(arr2[0]) >= int(arr[0]) and int(arr2[1]) >= int(arr[1]) and int(arr2[2]) >= int(arr[2]):
                    GAMEDATES.append(cd)
    return GAMEDATES,rowcount