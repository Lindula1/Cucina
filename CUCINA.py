import hashlib
import random
import string
from DataStoreModel import DataBase
import PDFHandler as PDF
#import IngredientDataStore as Pantry
import pwinput
ds = DataBase()

h = hashlib.new('sha256')
al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CUCINA():
    def __init__(self):
        pass

    def RegisterAccount(self, usrm, pwrd, name):
        ulvalid = False
        uavalid = True
        plvalid = False
        pavalid = False
        if len(usrm.strip()) >= 3:
            ulvalid = True
            if usrm[0].upper() not in al:
                uavalid = False
                return "Username Type error"
        else: return "Username Too short"
        if len(pwrd.strip()) >= 3:
            plvalid = True
            c = 0
            for j in pwrd.strip():
                if j.upper() in al:
                    c += 1
            if c < len(pwrd.strip()):
                pavalid = True
            else:
                return "Password Type error"
        else: return "Password Too short"
        if uavalid and ulvalid and plvalid and pavalid and self.Search(usrm) == None:
            account = {"uid": None, "username": usrm, "password":hashlib.sha256(pwrd.encode('utf-8')).hexdigest(), "name": name}
            ds.AddTo(account)
            return 1
        else:
            return "Username already exists"

    def LogIn(self, usrm, pwrd):
        ulvalid = False
        uavalid = True
        plvalid = False
        if usrm[0].strip().upper() not in al: 
            uavalid = False
            print("username has an invalid leader")
        if len(usrm.strip()) >= 3: ulvalid = True
        else: print("username is too short")
        if len(pwrd.strip()) >= 3: plvalid = True
        else: print("password is too short")
        if uavalid and ulvalid and plvalid:
            account = self.Search(usrm)
            if hashlib.sha256(pwrd.encode('utf-8')).hexdigest() == account[1]["password"]:
                return "Login successful"
            else:
                return "Login unsuccessful"
        else:
            return "Too many checks were invalid"

    def RemoveAccount(self, query):
        if len(query) < 1: return "Query length too short"
        if len(ds.arr) == 1:
            print("This is the last account in the database.")
            ds.arr.pop(0)
        else:
            results, pos, ran = ds.BulkSearch(query)
            if results == None: return "Item Not found"
            for i in range(len(results)):
                if results[i][1]["username"] == query:
                    if (i - ran[0]) < 0:
                        delIndex = pos - i
                    elif (i - ran[0]) > 0:
                        delIndex = pos + i
                    else:
                        delIndex = pos
                    ds.arr.pop(delIndex)
                    return "Item Deleted"
        return "Item Not Found"
    
    def Search(self, query):
        accountList, pos, ran = ds.BulkSearch(query)
        if accountList == None: return None
        else:
            for i in accountList:
                if i[1]["username"] == query:
                    return i
                
    def AddToPantry(self, item):
        Pantry.pantry.AddItem(item)
        
    
    def DishSearch(self, dishName):
        ingredients, text, steps = PDF.Read(dishName)
        ingredients = ingredients
        pantryItems = Pantry.pantry.PantryList()
        #print(ingredients, pantryItems)
        matches = []
        for i in pantryItems:
            for j in ingredients:
                if i in j: matches.append(j)
        return matches

app = CUCINA()

#Debugging Code
print("This is a backend representation of the software solution and any errors made while entering values is not checked for.\nIf you make any errors the code will simply restart from the beginning or crash :)")

accounts = [{"uid":None, "username":"Lindt", "password":hashlib.sha256("2039".encode('utf-8')).hexdigest()}]
for j in range(12):
    accounts.append({"uid":None, "username":''.join(random.choices(string.ascii_letters, k=5)), "password":hashlib.sha256(str(j+2034).encode('utf-8')).hexdigest()})
for i in accounts:
    ds.AddTo(i)

while True:
    prompt = ["Enter a Username (do not lead with a non alphabetical character, min length of 3): ", "Enter a secure Password (must include a number or special character, min length of 3): ", "Enter your own name: "]
    account = []
    for i in range(3):
        entry = input(prompt[i])
        if not entry.isdigit():
            account.append(entry)
        elif entry == "end":
            account = []
            break
        else:
            print("Input is invalid, Try again")
            break
    if account == []:
        pass
    else:
        result = app.RegisterAccount(account[0], account[1], account[2])
        if result == 1:
            print("Account registered successfully")
            break
        else:
            print(result)
            print("Please read the instructions")

while True:
    if app.LogIn(input("Enter your username: "), pwinput.pwinput("Enter your password: ")) == "Login successful": break
    if input("Break? [yes or no] ").strip().lower() == 'yes': break
'''
'''
print(ds.arr)

while len(ds.arr) > 0:
    print(app.RemoveAccount(input("Enter a username to remove it: ")))
    print(ds.arr)
