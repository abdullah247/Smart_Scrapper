import  datetime as dt
from selenium.webdriver.common.by import By


def excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def waitthousand(selector,wait,driver,mlen=1):
    counter=0
    while len(driver.find_elements(By.CSS_SELECTOR,selector)) < mlen:
        counter+=1
        if counter>wait:
            break
        pass

def saveme(wk,name="Latest"):

    flag=True
    counter=0
    name = str(name).replace(".xlsx", "")
    print("Updating File Donot Close Or interfere")
    while flag:
        try:
            if counter==0:
                counter+=1
                wk.save(f"{name}.xlsx")
                flag=False
            else:
                counter+=1
                wk.save(f"{name}{counter}.xlsx")
                flag = False

        except:
            print("Cannot Save File if already opened saving it by adding number at the end")
    print("Updated Latest File")


    pass


def getmonth(argument):
    switcher= {
        "January":1,
        "February" :2,
        "March" :3,
        "April" :4,
        "May" :5,
        "June" :6,
        "July" :7,
        "August" :8,
        "September" :9,
        "October" :10,
        "November" :11,
        "December" :12
    }
    return switcher.get(argument)

def moveleft(driver):
    driver.find_element(By.CSS_SELECTOR,".ui-icon.ui-icon-circle-triangle-w").click()


def moveright(driver):
    driver.find_element(By.CSS_SELECTOR,".ui-icon.ui-icon-circle-triangle-e").click()
