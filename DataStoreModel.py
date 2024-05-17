import math
import keyboard
import hashlib
import random

class DataBase():
    def __init__(self):
        self.arr = []
    
    def AddTo(self):
        self.arr.append()

    def UserID(self, account):
        usrnmIL = account["username"][0]#.upper()
        oId = ord(usrnmIL)
        if oId >= 99:
            print("oId out of range", oId)
        else:
            print(oId)
        nId = random.randint(1000000000000, 9999999999999)
        #usrID
    
    def Sort(self, array):
        n = len(array)
        for i in range(n):
            sorted = True
            for j in range(n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    sorted = False
            if sorted == True:
                return array

        return -1
    
dS = DataBase()
account = {"username":"zL"}
dS.UserID(account)