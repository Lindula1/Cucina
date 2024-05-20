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
        self.arr = self.Sort(self.arr)
        if self.arr == -1: 
            print("Fatal Error")
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