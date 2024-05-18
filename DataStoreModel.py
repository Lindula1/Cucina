import hashlib
import random
import string

class DataBase():
    def __init__(self):
        self.arr = []
    
    def AddTo(self, account):
        self.arr.append(self.AddUserID(account))
        self.arr = self.Sort(self.arr)

    def AddUserID(self, account):
        usrnmIL = account["username"][0].upper()
        oId = ord(usrnmIL)
        if oId >= 99:
            print("oId out of range", oId)
        nId = random.randint(1000000000, 9999999999)
        account["uid"] = nId
        account = [oId, account]
        return account
    
    def Sort(self, array):
        n = len(array)
        for i in range(n):
            sorted = True
            for j in range(n - i - 1):
                if array[j][0] > array[j + 1][0]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    sorted = False
            if sorted == True:
                return array
        return -1
    
    def BulkSearch(self, query):
        query = ord(query[0].upper())
        low = 0
        high = len(self.arr) - 1
        accounts = []
        while low <= high:
            mid = (low + high)//2
            midVal = self.arr[mid][0]
            if midVal == query:
                accounts.append(self.arr[mid])
                umid = lmid = mid
                while midVal == query:
                    accounts.append(self.arr[mid])
                    umid += 1
                    midVal = self.arr[umid][0]
                while midVal == query:
                    accounts.append(self.arr[mid])
                    lmid -= 1
                    midVal = self.arr[lmid][0]
                return accounts
            elif midVal < query:
                low = mid + 1
            else:
                high = mid - 1
        return None