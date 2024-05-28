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
        if len(usrm.strip()) < 3: return "Username is too short"
        if usrm[0].upper() not in al: return "Username type error"
        if len(pwrd.strip()) < 3: return "Password is too short"
        c = 0
        for j in pwrd.strip():
            if j.upper() in al:
                c += 1
        if c > len(pwrd.strip()):
            return "Password Type error"
        if self.Search(usrm) == None:
            account = {"uid": None, "username": usrm, "password":hashlib.sha256(pwrd.encode('utf-8')).hexdigest(), "name": name}
            ds.AddTo(account)
            return "Success"
        else:
            return "Username already exists"

    def LogIn(self, usrm, pwrd):
        if usrm[0].strip().upper() not in al: return "username has an invalid leader"
        account = self.Search(usrm)
        if account == None: return "Username doesn't exist"
        if hashlib.sha256(pwrd.encode('utf-8')).hexdigest() == account[1]["password"]: 
            #Login unlocked functions
            return "Login successful"
        else:
            return "Login unsuccessful"

    def RemoveAccount(self, query):
        if len(ds.arr) == 1:
            ds.arr.pop(0)
            return "The last item in the database has been removed."
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
    if input("Skip Login [y/n]: ") == "y": break
    prompt = ["Enter a Username (do not lead with a non alphabetical character, min length of 3): ", "Enter a secure Password (must include a number or special character, min length of 3): ", "Enter your own name: "]
    account = []
    for i in range(3):
        entry = input(prompt[i])
        if not entry.isdigit():
            account.append(entry)
        else:
            print("Input is invalid, Try again")
            account = []
            break
    if account == []:
        pass
    else:
        result = app.RegisterAccount(account[0], account[1], account[2])
        if result == "Success":
            print("Account registered successfully")
            break
        else:
            print(result)
            print("Please read the instructions")

print("Please LogIn")

while True:
    prompt = ["Enter your username: ", "Enter your password: "]
    account = []
    for i in range(2):
        entry = input(prompt[i])
        if len(entry) < 1:
            print("Input is invalid, Try again")
            account = []
            break
        account.append(entry)
    if account == []:
        pass
    else:
        result = app.LogIn(account[0], account[1])
        if result == "Login successful":
            print("result")
            print(ds.arr)
            while True:
                query = input("Enter a username to remove an account: ")
                if query == "end": break   
                elif len(query) > 0 and not query.isdigit():
                    print(app.RemoveAccount(query))
                    print(ds.arr)
                else: pass                    
        else:
            print(result)
            print("Please read the instructions")