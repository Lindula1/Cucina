"""
===CUCINA APPLICATION===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 17/05/2024
Last Edited: 28/05/2024
Description:
*RUNNING THIS FILE WILL DO NOTHING*
This python file contains all functions of the Cucina App.
"""

from DataStoreModel import DataBase
import IngredientDataStore as Pantry
import random
import string
ds = DataBase()
al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CUCINA():
    def __init__(self):
        try:
            global HashingFunc
            from Hashing import HashingFunc
            global PDF
            import PDFHandler as PDF
            self.disableLogin = False
        except ModuleNotFoundError:
            self.disableLogin = True
        self.admin = False

    """
    INPUTS:
        usrm (str): The username for the new account. Must be a non-empty string with specific format constraints.
        pwrd (str): The password for the new account. Must meet length and character type constraints.
        name (str): The name associated with the new account. 

    PROCESS:
        - Validates the username for length and character constraints.
        - Checks if the password meets length and character constraints.
        - Verifies that the username does not already exist.
        - If valid, creates a new account with a hashed password and adds it to the account storage.

    OUTPUTS:
        - (str) - Returns a message indicating the result of the registration attempt.
            - "Username is too short": If the username is shorter than 3 non-space characters.
            - "Username type error": If the username does not start with a valid character.
            - "Password is too short": If the password is shorter than 3 non-space characters.
            - "Password Type error": If the password only contains letters (and thus lacks required complexity).
            - "Username already exists": If the username is already taken.
            - "Success": If the registration is successful.
    """
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

    """
    INPUTS:
        usrm (str): The username provided for logging in. Must be a valid string.
        pwrd (str): The password provided for logging in. Must be a valid string.

    PROCESS:
        - Checks if the login feature is disabled (`self.disableLogin`).
        - Searches for an account with the provided username using `self.Search`.
        - Verifies the provided password against the stored hashed password using `HashingFunc`.
        - Determines the login type based on the account details.

    OUTPUTS:
        - (str) - Returns a message indicating the result of the login attempt:
            - "Login feature is disabled": If login functionality is currently disabled.
            - "Username doesn't exist": If the username is not found in the system.
            - "Password is Incorrect": If the password provided does not match the stored password.
            - "Logged in as Admin": If the account is identified as an admin based on specific conditions.
            - "Login successful": If the login is successful and the user is not an admin.
    """
    def LogIn(self, usrm, pwrd):
        if self.disableLogin:
            return "Login feature is disabled"
        account = self.Search(usrm.lower())
        if account == None: return "Credentials are incorrect"
        if HashingFunc(pwrd) == account[1]["password"]: 
            if len(account[1]) < 4:
                self.admin = True
                return "Logged in as Admin"
            self.admin = False
            return "Login successful"
        else:
            return "Credentials are incorrect"

    """
    INPUTS:
        query (str): The username of the account to be removed. Must be a valid string.

    PROCESS:
        - Checks if the database contains only one item and removes it if true.
        - Performs a bulk search for the account using `ds.BulkSearch`.
        - Iterates through the search results to find the matching username.
        - Determines the index to delete based on the search results and removes the account from the database.
        - Saves the updated database to an online repository.

    OUTPUTS:
        - (str) - Returns a message indicating the result of the removal attempt:
            - "The last item in the database has been removed.": If the only item in the database is removed.
            - "Item Deleted": If the specified account is successfully found and removed from the database.
            - "Item Not Found": If the specified account is not found in the database.
    """
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
                    ds.SaveOnline()
                    return "Item Deleted"
        return "Item Not Found"
    
    """
    INPUTS:
        query (str): The username to search for. Must be a valid string.

    PROCESS:
        - Calls `ds.BulkSearch` with the query to retrieve a list of accounts matching the query.
        - If no accounts are found, returns `None`.
        - Iterates through the list of found accounts to match the username with the query.
        - Returns the account information if a match is found.

    OUTPUTS:
        - (dict or None) - Returns the account information if a match is found, otherwise `None`.
    """
    def Search(self, query):
        accountList, pos, ran = ds.BulkSearch(query.lower())
        if accountList == None: return None
        else:
            for i in accountList:
                if i[1]["username"].lower() == query.lower():
                    return i

    """
    INPUTS:
        item (dict): The item to be added to the pantry. Should include necessary details like name, quantity, etc.

    PROCESS:
        - Calls `AddItem` method from `Pantry.pantry` to add the provided item to the pantry.

    OUTPUTS:
        - None
    """          
    def AddToPantry(self, item):
        Pantry.pantry.AddItem(item)
    
    """
    INPUTS:
        recipe (str): The name of the recipe (e.g., a PDF filename) to be searched for ingredients.

    PROCESS:
        - Reads the recipe file to extract ingredients and other details using `PDF.Read`.
        - Retrieves the list of items from the pantry using `Pantry.pantry.PantryList`.
        - Compares the ingredients from the recipe with the pantry items to find matches and opposites:
            - Matches are ingredients found in both the recipe and the pantry.
            - Opposites are ingredients in the recipe that are not found in the pantry.

    OUTPUTS:
        - (list, list): A tuple containing:
            - `opposite` (list): Ingredients from the recipe not found in the pantry.
            - `matches` (list): Ingredients from the recipe that match with items in the pantry.
    """
    def DishSearch(self, recipe):
        ingredients, text, steps = PDF.Read(recipe)
        pantryItems = Pantry.pantry.PantryList()
        opposite = []
        matches = []
        for item in pantryItems:
            d = item[5]
            userIngredient = "".join(c for c in d if c.isalpha())
            for ingredient in ingredients:
                if (userIngredient.lower() in ingredient.lower()) and (userIngredient not in matches):
                    matches.append(ingredient)
        for ing in ingredients:
            if ing not in matches:
                opposite.append(ing)
        return opposite, matches
    
    """
    INPUTS:
        dishName (str): The name of the dish to search for in the recipe list.

    PROCESS:
        - Retrieves a list of all recipes using `PDF.ReadPDFData()`.
        - Searches for recipes whose names contain the `dishName` (case-insensitive).
        - For each matching recipe, performs a `DishSearch` to find ingredients and their availability in the pantry.
        - Collects and organizes the results:
            - `names` contains lists of ingredients not found in the pantry for each recipe.
            - `matches` contains lists of ingredients found in the pantry for each recipe.

    OUTPUTS:
        - (tuple): A tuple containing:
            - `names` (list of lists): Lists of ingredients not found in the pantry for each matching recipe.
            - `matches` (list of lists): Lists of ingredients found in the pantry for each matching recipe.
        - If no recipes are found, returns a tuple with the `dishName` and a message indicating no recipes were found.
    """
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



if __name__ == "__main__":
    #Debugging Code
    '''
    ds.arr = []
    ds.SaveLocally
    accounts = [{"uid":None, "username":"Lindt", "password":HashingFunc("2039")}]
    for j in range(19):
        accounts.append({"uid":None, "username":''.join(random.choices(string.ascii_letters, k=6)), "password":HashingFunc(str(random.choices(string.ascii_letters, k=5))), "name":''.join(random.choices(string.ascii_letters, k=13))})
    for i in accounts:
        ds.AddTo(i)
    '''
    pass