import hashlib
import random
import string
from DataStoreModel import DataBase
import PDFHandler as PDF
import IngredientDataStore as Pantry
import datetime
from Hashing import HashingFunc
ds = DataBase()

h = hashlib.new('sha256')
al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CUCINA():
    def __init__(self):
        self.admin = False
        self.errors = []
        if ds.checks == False:
            self.errors.append("\033[31mFATAL ERROR DATABSE EMPTY\033[0m")
        if Pantry.pantry.checks == False:
            self.errors.append("\033[31mPANTRY IS EMPTY\033[0m")
        if len(self.errors) > 0:
            for i in self.errors: print(i)
            print(f"\033[33mAn error was detected in dependancies.\nThe progam may not be able to run properley.\033[0m\n")

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
        if usrm[0].strip().upper() not in al: return "username has an invalid leader"
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
            for j in ingredients:
                if i.lower() in j.lower(): matches.append(j)
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

#for i in Pantry.pantry.arr:
#    print(Pantry.pantry.DateRevert(i))

#Debugging Code
"""
accounts = [{"uid":None, "username":"Lindt", "password":HashingFunc("2039")}]
for j in range(74):
    accounts.append({"uid":None, "username":''.join(random.choices(string.ascii_letters, k=5)), "password":HashingFunc(str(j+2034)), "name":''.join(random.choices(string.ascii_letters, k=13))})
for i in accounts:
    ds.AddTo(i)
"""

if __name__ == "__main__":
    print("\033[33m***PLEASE READ ALL THE TEXT BELOW BEFORE USING THIS SOFTWARE***\033[0m")
    print("This is a backend representation of the software solution and any errors made while entering values is loosely checked for.\nEntering incorrect values will have the program slander you for your blunder.")
    print("Register your account if this is your first time using the application")
    yn = input("Enter [y] to register a new account: ")
    while True:
        if yn == "y":
            print("Account Registration")
            prompt = ["Enter a Username (do not lead with a non alphabetical character, min length of 3): ", "Enter a secure Password (must include a number or special character, min length of 3): ", "Enter your own name: "]
            account = []
            for i in range(3):
                entry = input(prompt[i])
                if not entry.isdigit():
                    account.append(entry)
                else:
                    print("Input leads with a number, please confirm with your parent that you attended primary school")
                    account = []
                    break
            if account == []:
                pass
            else:
                result = app.RegisterAccount(account[0], account[1], account[2])
                if result == "Success":
                    yn = "n"
                    print("Account registered successfully")
                else:
                    print(result)
                    print("Please read the instructions")
        else:
            print("Please Log In")
            run = True
            while run:
                prompt = ["Enter your username: ", "Enter your password: "]
                account = []
                for i in range(2):
                    entry = input(prompt[i])
                    if len(entry) < 1:
                        print("Input is invalid, Try again genius")
                        account = []
                        break
                    account.append(entry)
                if account == []:
                    pass
                else:
                    result = app.LogIn(account[0], account[1])
                    if result == "Login successful" or result == "Logged in as Admin":
                        print(f"\033[34m{result}\033[0m")
                        while True:
                            if app.admin == True:
                                choice = input("Enter [a] to Add an item\nEnter [s] to Sort the list\nEnter [v] for recipe finder beta\nEnter [i] to view an item\n\033[31mEnter [f] to view an account\033[0m\nEnter Selection Here: ")
                            else:
                                choice = input("Enter [a] to Add an item\nEnter [s] to Sort the list\nEnter [v] for recipe finder beta\nEnter [i] to view an item\nEnter Selection Here: ")
                            if choice.lower() == "s":
                                t = input("Enter a sort Index [0 = Alphabetical, 1 = Nutritional Value, 2 = Quantity, 3 = Expiry Date]: ")
                                if t.isdigit():
                                    t = int(t)
                                    if 0 <= t <= 3:
                                        Pantry.pantry.SortFunc(Pantry.pantry.arr, t)
                                        keys = ["Numerical Name: ", "Nutrional Value: ", "Quantity: ", "Expiry Date: "]
                                        c = 0
                                        for item in Pantry.pantry.arr:
                                            if t == 3:
                                                date, days = Pantry.pantry.DateRevert(item)
                                                print(f"index: {c}, Item name: {item[4]}, {keys[t]}{date}")
                                            else:
                                                print(f"index: {c}, Item name: {item[4]}, {keys[t]}{item[t]}")
                                            c += 1
                                    else:
                                        print("Please follow the instructions to save yourself some time.")
                                else:
                                    print("Numbers are the following unique characters that represent quantaties [0,1,2,3,4,5,6,7,8,9] this program requires that you used them in the correct way.")
                            elif choice.lower() == "a":
                                endLoop = True
                                while endLoop:
                                    prompts = ["Enter the nutrional value of the item in kJ [numbers only]: ", "Enter the quantity of the item you have [numbers only]: "
                                            , "Enter the expiry date in the following format [yyyy/mm/dd]: ", "Enter the name of the item [Do not enter a number first]: "]
                                    iToAdd = []
                                    for l in range(4):
                                        entry = input(prompts[l])
                                        if l == 2:
                                            if "/" in entry:
                                                dtime = entry.split("/")
                                                for i in range(len(dtime)): dtime[i] = int(dtime[i])
                                                try:
                                                        d = datetime.date(dtime[0], dtime[1], dtime[2])
                                                        iToAdd.append(dtime)
                                                except ValueError:
                                                    print("That date doesn't exist, please reconsider your education")
                                                    break
                                            else:
                                                print("Wrong format, genius")
                                                break
                                        elif l == 3:
                                            if entry[0].isdigit():
                                                print("Name leads with a number, Further your understanding of numarical values and return to the program another time :)")
                                                break
                                            else:
                                                iToAdd.append(entry)
                                                print(Pantry.pantry.AddItem(iToAdd))
                                                endLoop = False
                                        elif entry.isdigit():
                                            if int(entry) < 99999999:
                                                iToAdd.append(int(entry))
                                            else:
                                                print(f"Please tell your cat to remove its paw from the '{entry[-1]}' key")
                                                break
                                        else:
                                            print("Humans have developed a base 10 counting system that is proficient at representing any quantity of items, please use it.")
                                            break
                            elif choice.lower() == "v":
                                entry = input("Recipe name: ")
                                names, matches = app.RecipeCompare(entry)
                                if type(matches) is list:
                                    for index in range(len(matches)):
                                        print(f"Ingredients you might have for the recipe {names[index]} are, {matches[index]}")
                                else:
                                    print(matches)
                            elif choice.lower() == "i":
                                entry = input("Enter the exact name of the item you want to search or enter [a] to view all items: ")
                                if entry == "a":
                                    result = Pantry.pantry.arr
                                    for item in result:
                                        print(item[4])
                                else:
                                    result = Pantry.pantry.Search(entry)
                                    print(f"RESULT\n{result}")
                                    if result == None:
                                        print("The search wasn't exact.")
                                    else:
                                        print("What do you wish to do with this item?")
                                        option = input("Enter [r] to remove, Enter [v] to view the expiry date: ")
                                        if option == "r":
                                            print(Pantry.pantry.Remove(entry))
                                        elif option == "v":
                                            date, days = Pantry.pantry.DateRevert(Pantry.pantry.Search(entry))
                                            print(f"This item will expire on the {date}. You have {days} days to use it")
                                        elif option == "clear":
                                            if input("Confirm clear all pantry. Clear all is permenant, [yes/no]:") == "yes":
                                                Pantry.pantry.Clear()
                                        else:
                                            print(f"I'm sorry but '{option}' isn't a valid option, please read with your eyes.")
                                            break
                            elif choice.lower() == "f" and app.admin == True:
                                query = input("Enter a username to view an account or enter [c] to wipe database: ")  
                                if query == "c":
                                    if input("Are your sure you want to do this? [y/n]: ") == "y":
                                        if input("This action is permanent and cannot be reverted, confirm one more time that you want to delete all accounts. [y/n]: ") == "y":
                                            ds.arr = []
                                            if input("This is your last chance to go back. Are you sure? [y/n]: "):
                                                ds.SaveLocally()
                                elif len(query) > 0 and not query.isdigit():
                                    account = app.Search(query)
                                    originalUser = account[1]["username"]
                                    if len(account[1]) > 4:
                                        print("Cannot view admin accounts")
                                    else:
                                        print(f"Sort ID: {account[0]}")
                                        for o in account[1].keys():
                                            d = account[1][o]
                                            print(f"{o}: {d}")
                                        entry = input("Enter [r] to remove the account, Enter [uid, username, name] to edit values: ")
                                        if entry == "r":
                                            print(app.RemoveAccount(query))
                                        elif entry == "uid":
                                            c = input("Generate new UID? [y/n]: ")
                                            if c == "y":      
                                                nId = random.randint(1000000000, 9999999999)
                                                account[1]["uid"] = nId
                                                app.RemoveAccount(originalUser)
                                                ds.arr.append(account)
                                                ds.SaveLocally()
                                        elif entry == "username":
                                            account[1]["username"] = input("Enter a new username for this user (Sort ID requires first value to be a non-integer): ")
                                            account[0] = ord(account[1]["username"][0])
                                            app.RemoveAccount(originalUser)
                                            ds.arr.append(account)
                                            ds.SaveLocally()
                                        elif entry == "password":
                                            account[1]["password"] = HashingFunc(input("Enter a new password for this user: "))
                                            app.RemoveAccount(originalUser)
                                            ds.arr.append(account)
                                            ds.SaveLocally()
                                        elif entry == "name":
                                            account[1]["name"] = input("Enter a new name for this user: ")
                                            app.RemoveAccount(originalUser)
                                            ds.arr.append(account)
                                            ds.SaveLocally()
                                    print("Account updated successfully")
                            elif choice.lower() == "end": 
                                run = False
                                print("Successfully logged out.")
                                break
                            else:
                                print(f"'{choice}' is not an option. Learn to read before using this program please.")             
                    else:
                        print(result)
                        print("Please read the instructions")
    print("Thank you for testing this software :)")