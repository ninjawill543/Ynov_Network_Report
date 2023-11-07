import sys
import time
from requests import get

site = "https://api.macvendors.com/"

def openFiles(x: str) -> []:
    file = open("/devices"+x+".txt", "r")
    result = file.read().split("\n")
    file.close()
    return result

def openAllFiles() -> []:
    allFiles = []
    for i in range(1, 16):
        number = str(i)
        if i < 10:
            number = "0" + number
        allFiles += openFiles(number)
    return allFiles

def deleteDoubleEntries() -> []:
    allDevices = openAllFiles()
    i = 0
    while (i < len(allDevices)):
        k = 0
        while (k < len(allDevices)):
            if (i != k) and ((allDevices[i] == allDevices[k]) or (allDevices[k] == "")):
                allDevices = allDevices[:k] + allDevices[k+1:]
            else:
               k += 1
        i += 1
    return allDevices

def writeAllDevices():
    allDevices = deleteDoubleEntries()
    f = open("allDevices.txt", "a")
    for i in allDevices:
        f.write(i + "\n")
        f.close()

def getMac(file: [], index: int) -> str:
    return file[index].split(" ")[1]

def getId(file: str, index: int) -> str:
    return " ".join(file[index].split(" ")[2:])

def macLookup(file: [], index: int) -> str:
    request = site + getMac(file, index)
    result = get(request).text
    if ("Not Found" in result) or (len(result) == 0):
        return "Not found"
    else:
        return result

def formatVendor(vendor: str) -> str:
    return "_".join(vendor.split(" "))

def reverseAllMac(allDevices: []):
    allVendors = ""
    for i in range(0, len(allDevices)-1):
        time.sleep(10)
        vendor = formatVendor(macLookup(allDevices, i))
        
        while vendor == '{"errors":{"detail":"Too_Many_Requests","message":"Please_slow_down_your_requests_or_upgrade_your_plan_at_https://macvendors.com"}}':
            time.sleep(10)
            vendor = formatVendor(macLookup(allDevices, i))
        allVendors += vendor + "\n"

    f = open("allVendors.txt", "a")
    f.write(allCendors)
    f.close()

def writeVendors():
    file = open("allVendors.txt", "r")
    vendors = file.read().split("\n")
    file.close()

    file = open("allDevices.txt", "r")
    devices = file.read().split("\n")
    file.close()

    for i in range(0, len(devices)-1):
        file = open("Vendors/"+vendors[i]+".txt", "a")
        file.write(devices[i] + "\n")
        file.close()
