"""
===CUCINA APPLICATION===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 17/05/2024
Last Edited: 28/05/2024
Description:

"""
try:
    import random
    import string
    from DataStoreModel import DataBase
    import PDFHandler as PDF
    import IngredientDataStore as Pantry
    import datetime
    from Hashing import HashingFunc
    ds = DataBase()
    al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

except ModuleNotFoundError:
    print("\033[31mFATAL ERROR. Dependenant modules missing.\nThe software must terminate\033[0m")
    exit()

class CUCINA():
    def __init__(self):
        self.disableLogin = False
        self.admin = False
        self.errors = []
        if ds.checks == False:
            self.errors.append("\033[31mFATAL ERROR DATABSE EMPTY\033[0m")
        if Pantry.pantry.checks == False:
            self.errors.append("\033[31mPANTRY IS EMPTY\033[0m")
            self.disableLogin = True
        if len(self.errors) > 0:
            for i in self.errors: print(i)
            print(f"\033[33mAn error was detected in dependancies.\nThe progam may not be able to run properley.\033[0m\n")
        self.dtList = ds.arr
        self.pantryList = Pantry.pantry.arr

    def RegisterAccount(self, usrm, pwrd, name):
        usLength = 0
        for u in usrm:
            if u == " ":
                pass
            else:
                usLength += 1
        psLength = 0
        for p in pwrd:
            if p == " ":
                pass
            else:
                psLength += 1
        if usLength < 3: return "Username is too short"
        if usrm[0].upper() not in al: return "Username type error"
        if psLength < 3: return "Password is too short"
        c = 0
        for j in pwrd.strip():
            if j.upper() in al:
                c += 1
        if c == len(pwrd.strip()): return "Password Type error"
        if self.Search(usrm) == None:
            account = {"uid": None, "username": usrm, "password":HashingFunc(pwrd), "name": name}
            ds.AddTo(account)
            return "Success"
        else:
            return "Username already exists"

    def LogIn(self, usrm, pwrd):
        if self.disableLogin:
            return "Login feature is disabled"
        if usrm[0].upper() not in al: return "username has an invalid leader"
        account = self.Search(usrm.lower())
        if account == None: return "Username doesn't exist"
        if HashingFunc(pwrd) == account[1]["password"]: 
            if len(account[1]) < 4:
                self.admin = True
                return "Logged in as Admin"
            self.admin = False
            return "Login successful"
        else:
            return "Login unsuccessful"

    def RemoveAccount(self, query):
        if len(ds.arr) == 1:
            ds.arr.pop(0)
            return "The last item in the database has been removed."
        else:
            results, pos, ran = ds.BulkSearch(query.lower())
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
                    ds.SaveLocally()
                    return "Item Deleted"
        return "Item Not Found"
    
    def Search(self, query):
        accountList, pos, ran = ds.BulkSearch(query.lower())
        if accountList == None: return None
        else:
            for i in accountList:
                if i[1]["username"].lower() == query.lower():
                    return i
                
    def AddToPantry(self, item):
        Pantry.pantry.AddItem(item)
    
    def DishSearch(self, recipe):
        ingredients, text, steps = PDF.Read(recipe)
        pantryItems = Pantry.pantry.PantryList()
        matches = []
        for i in pantryItems:
            d = i[4]
            for x in range(len(d)):
                if d[x].isdigit(): 
            for j in ingredients:
                if d.lower() in j.lower(): matches.append(j)
        return recipe, matches
    
    def RecipeCompare(self, dishName):
        recipes = []
        recipeList = PDF.ReadPDFData()
        for recipe in recipeList:
            if dishName.lower() in recipe.lower():
                recipes.append(recipe)
        if recipes == []:
            return dishName, "No recipes found for your dish."
        else:
            names = []
            matches = []
            for recipe in recipes:
                name, match = self.DishSearch(recipe)
                names.append(name)
                matches.append(match)
            return names, matches


app = CUCINA()

#Debugging Code
'''
ds.arr = []
ds.SaveLocally
accounts = [{"uid":None, "username":"Lindt", "password":HashingFunc("2039")}]
for j in range(74):
    accounts.append({"uid":None, "username":''.join(random.choices(string.ascii_letters, k=6)), "password":HashingFunc(str(random.choices(string.ascii_letters, k=5))), "name":''.join(random.choices(string.ascii_letters, k=13))})
for i in accounts:
    ds.AddTo(i)
'''

if __name__ == "__main__":
    pass