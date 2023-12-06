
from tkinter import Tk, filedialog, messagebox
import json
import os

# Data to be written
dictionary = {
    "SCADDRESS": "",
    "TCADDRESS": "",
    "HKADDRESS": "",
    "BRADDRESS": "",

}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

def importData():
    FileAddress=os.path.join(os.getcwd(),"FilesAddress.json")
    if os.path.exists(FileAddress):
        print("YEs")
        with open(FileAddress, 'r') as openfile:
            json_object = json.load(openfile)

            return json_object
    else:
        with open(FileAddress, "w") as outfile:
            json.dump(dictionary, outfile)
            return dictionary



def SAVEDATA(a,b,c,d):
    dictionary["HKADDRESS"]=a
    dictionary["TCADDRESS"] = b
    dictionary["SCADDRESS"] = c
    dictionary["BRADDRESS"] = d
    FileAddress = os.path.join(os.getcwd(), "FilesAddress.json")

    with open(FileAddress, "w") as outfile:
        json.dump(dictionary, outfile)



def oneVal(val):
    FileAddress = os.path.join(os.getcwd(), "FilesAddress.json")
    if os.path.exists(FileAddress):
        with open(FileAddress, 'r') as openfile:
            json_object = json.load(openfile)

            return json_object[val]
    return ""
def GetTC():
     return oneVal("TCADDRESS")



def GetHK():
    return oneVal("HKADDRESS")
    return


def GetSC():
    return oneVal("SCADDRESS")
    return


def GetBR():
    return oneVal("BRADDRESS")
    return

def Browse(tc_Address):
    root = Tk()
    root.withdraw()
    filetypes = (('Files', ".xlsx"), ('All files', '*.*'))
    tc_Address.setText(str(filedialog.askopenfilename(title='Select a file', filetypes=filetypes)).replace("/", "\\"))
    pass