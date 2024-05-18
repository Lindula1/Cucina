import hashlib
import random
import string
from DataStoreModel import DataBase
ds = DataBase()

h = hashlib.new('sha256')
al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CUCINA():
    def __init__(self):
        pass

    def Register(self, usrm, pwrd, name):
        ulvalid = False
        uavalid = True
        plvalid = False
        pavalid = False
        if len(usrm.strip())> 3:
            ulvalid = True
            for i in usrm.strip():
                if i.upper() not in al:
                    uavalid = False
                    break
        if len(pwrd.strip()) > 3:
            plvalid = True
            c = 0
            for j in pwrd.strip():
                if j.upper() in al:
                    c += 1
            if c < len(pwrd.strip()):
                pavalid = True
        if len(name.strip()) < 1 or name.lower() == "kesh":
            print("You're too short")
        if uavalid and ulvalid and plvalid and pavalid:
            account = {"uid": None, "username": usrm, "password":hashlib.sha256(pwrd.encode('utf-8')).hexdigest(), "name": name}
            ds.AddTo(account)
        else:
            print("Too many checks were invalid")

    def LogIn(self, usrm, pwrd):
        ulvalid = False
        uavalid = True
        plvalid = False
        if len(usrm.strip()) > 3: 
            ulvalid = True
            for i in usrm.strip():
                if i.upper() not in al:
                    uavalid = False
                    break
        if len(pwrd.strip()) > 3: plvalid = True
        if uavalid and ulvalid and plvalid:
            account = self.Search(usrm)
            if hashlib.sha256(pwrd.encode('utf-8')).hexdigest() == account[1]["password"]:
                print("Login successful")
            else:
                print("Login unsuccessful")
        else:
            print("Too many checks were invalid")
    
    def Search(self, query):
        accountList = ds.BulkSearch(query)
        for i in accountList:
            if i[1]["username"] == query:
                return i

app = CUCINA()

accounts = [{"uid":None, "username":"Lindt", "password":hashlib.sha256("2039".encode('utf-8')).hexdigest()}]
for j in range(12):
    accounts.append({"uid":None, "username":''.join(random.choices(string.ascii_letters, k=5)), "password":hashlib.sha256(str(j+2034).encode('utf-8')).hexdigest()})
for i in accounts:
    ds.AddTo(i)

app.Register("Lindt", "Cho1", "Chocolate")
print(ds.arr)
#print(app.Search("Lindt"))
#app.LogIn("Lindt", "2039")