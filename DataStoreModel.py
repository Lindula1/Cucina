"""
===CUCINA USER DATA STORE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 17/05/2024
Last Edited: 06/07/2024
Description:

"""
import random
import json
import datetime

class DataBase():
    def __init__(self):
        try:
            self.arr = self.ReadJson()
            self.checks = True
        except FileNotFoundError:
            self.arr = []
        if self.arr == []:
            self.checks = False
    
    def AddTo(self, account):
        self.arr.append(self.AddUserID(account))
        self.arr = self.Sort(self.arr)
        self.SaveLocally()

    def AddUserID(self, account):
        usrnmIL = account["username"][0].upper()
        oId = ord(usrnmIL)
        time = datetime.datetime.now()
        nId = time.strftime('%Y%m%d%H%M%S%f')
        account["uid"] = nId
        if oId >= 99:
            print("\033[31mFATAL ERROR, oId out of range\033[0m", oId)
            oId = 0
            account = [oId, account]
            return account
        account = [oId, account]
        return account

    def RevertId(self, account):
        uId = account[1]["uid"]
        date = []
        for i in range(4,len(uId),2):
            if i == 4:
                date.append(uId[i-4:i])
            elif i == 16:
                date.append(uId[i-2:len(uId)])
                break
            else:
                date.append(uId[i-2:i])
        return date

    def Sort(self, array):
        if len(self.arr) > 0:
            n = len(array)
            for i in range(n):
                sorted = True
                for j in range(n - i - 1):
                    if array[j][0] > array[j + 1][0]:
                        array[j], array[j + 1] = array[j + 1], array[j]
                        sorted = False
                if sorted == True:
                    return array
        return []
    
    def SaveLocally(self):
        dumped = json.dumps(self.arr, indent=4)
        with open("Accounts.json", "w") as file:
            file.write(dumped)

    def ReadJson(self):
        with open("Accounts.json", "r") as file:
            raw = json.load(file)
            return raw
    
    def BulkSearch(self, query):
        self.arr = self.Sort(self.arr)
        if self.arr == []: 
            print("\033[41mFATAL ERROR DATABSE EMPTY\033[0m")
            return None, None, None
        query = ord(query[0].upper())
        low = 0
        high = len(self.arr) - 1
        accounts = []
        posRange = [0, 0]
        while low <= high:
            pos = mid = (low + high)//2
            midVal = self.arr[mid][0]
            if midVal == query:
                accounts.append(self.arr[mid])
                umid = lmid = mid
                while midVal == query:
                    umid += 1
                    try:
                        midVal = self.arr[umid][0]
                    except IndexError:
                        break
                    if not midVal == query:
                        break
                    accounts.append(self.arr[umid])
                    posRange[1] += 1
                while True:
                    lmid -= 1
                    midVal = self.arr[lmid][0]
                    if not midVal == query:
                        break
                    accounts.append(self.arr[lmid])
                    posRange[0] += 1
                return accounts, pos, posRange
            elif midVal < query:
                low = mid + 1
            else:
                high = mid - 1
        return None, None, None
    
run = DataBase()

if __name__ == "__main__":
    run.RevertId(run.AddUserID({"uid":None, "username": "lindt", "password": "2039", "name": "Admin"}))