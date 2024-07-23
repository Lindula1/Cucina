"""
===CUCINA USER DATA STORE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 17/05/2024
Last Edited: 23/07/2024
Description:

"""
import GitCommunication
import random
import json
import datetime
from cryptography.fernet import Fernet

class DataBase():
    def __init__(self):
        try:
            if GitCommunication.ErrorCheck():
                self.checks = True
            else:
                self.arr = self.ReadJson()
                self.checks = True
        except GitCommunication.github.GithubException:
            self.arr = []
            self.checks = True

    def Load(self):
        try:
            self.arr = self.ReadJson()
            self.checks = True
        except GitCommunication.github.GithubException:
            self.arr = []
        if self.arr == []:
            return True
    
    def EncryptJson(self, data):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open("Accounts.json", "wb") as jsonFile:
            jsonFile.write(encrypted)
        return encrypted

    def GenEncryptionKey(self):
        key = Fernet.generate_key()
        with open('keyFile.key', 'wb') as filekey:
            filekey.write(key)
        fernet = Fernet(key)
        with open("Accounts.json", 'rb') as file:
            original = file.read()
        self.arr = fernet.encrypt(original)
    
    def DecryptJson(self):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        encrypted = GitCommunication.LoadGist()
        '''
        with open("Accounts.json", 'rb') as encFile:
            encrypted = encFile.read()
        '''
        if encrypted:
            raw = json.loads(fernet.decrypt(encrypted))
            return raw
    
    def AddTo(self, account):
        self.arr.append(self.AddUserID(account))
        self.arr = self.Sort(self.arr)
        self.SaveOnline()

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
        self.EncryptJson(bytes(dumped.encode("utf-8")))
        '''
        dumped = json.dumps(self.arr, indent=4)
        with open("Accounts.json", "w") as file:
            file.write(dumped)
        '''
    def SaveOnline(self):
        dumped = json.dumps(self.arr, indent=4)
        GitCommunication.UpdateGist(self.EncryptJson(bytes(dumped.encode("utf-8"))))

    def ReadJson(self):
        return self.DecryptJson()
        
    
    def BulkSearch(self, query):
        if self.arr == []: 
            self.arr = self.Sort(self.arr)
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
    #run.GenEncryptionKey()
    #print(run.arr)
    #run.SaveLocally()
    #run.SaveOnline()
    print(run.DecryptJson())