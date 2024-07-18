"""
===CUCINA INGREDIENT DATA STORAGE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 18/05/2024
Last Edited: 06/07/2024
Description:
This python file holds all functions for transforming
and transferring any and all ingredient data.
"""
import random
import string
import pwinput
import CSVHandler as CS
import datetime
#item = ["letter sort value (left empty)", "nutritional value", "quantity", "expiry date" "ingredient name"]

class Pantry():
    def __init__(self):
        self.checks = False
        try:
            self.arr = CS.Reader()
            self.checks = True
        except FileNotFoundError:
            self.arr = []
    """   
    INPUTS: item - A list representing an item, where item[3] is a date in the format [year, month, day].
    PROCESS:
    The function takes the date, converts it to a datetime.date object,
    initializes a datetime.date object representing the date April 20, 1889,
    calculates the difference between the objects,
    and returns the modified item.
    OUTPUT: item[3] - The number of days between the original date and April 20, 1889.
    """
    def FormatDate(self, item):
        d0 = datetime.date(item[3][0], item[3][1], item[3][2])
        self.d1 = datetime.date(1889, 4, 20)
        delta = d0 - self.d1
        item[3] = delta.days
        return item
    
    """
    INPUTS: self - Reference to the current instance of the class, item - A list containing the item information, including the number of days until the expiry date.

    PROCESS:
    The function calculates the expiry date by adding the number of days (item[3]) to a fixed reference date.
    It then converts the expiry date to a formatted string representation ("%Y/%m/%d").
    The function splits the formatted date string into year, month, and day components.
    It calculates the number of days left until the expiry date by subtracting the current date from the expiry date.
    The result is returned as the expiry date string and the number of days left.

    OUTPUT: expDate - The expiry date in the format "YYYY/MM/DD", daysLeft - The number of days left until the expiry date.
    """
    def DateRevert(self, item):
        d0 = datetime.timedelta(item[3])
        d1 = datetime.datetime(1889,4,20,0,0)
        d2 = datetime.date.today()
        expDate = (d1 + d0).strftime("%Y/%m/%d")
        explist = expDate.split("/")
        daysLeft = datetime.date(int(explist[0]), int(explist[1]), int(explist[2])) - d2
        return expDate, daysLeft.days


    def PantryList(self):
        try:
            raw = CS.Reader()
        except FileNotFoundError:
            print("Fatal Error. No items in pantry. Creating empty list")
            raw = []
        ilist = []
        for item in raw: ilist.append(item[4])
        return raw

    def AddItem(self, item):
        for i in range(len(item) - 1):
            if item[i] == 0:
                return "Field {i} is empty. HOW?"
        self.arr.append(self.FormatDate(self.LetterSort(item)))
        self.SaveToDevice()
        return "Item Added Successfully"

    def AddRaw(self, item):
        self.arr.append(item)
        self.SaveToDevice()
        

    def LetterSort(self, item):
        item.insert(0, ord(item[3][0].upper()))
        return item
    
    def BulkSearch(self, query):
        if len(query) > 0:
            self.arr = self.SortFunc(self.arr, 0)
            if self.arr == []: 
                print("No items left in pantry")
                return None, None, None
            query = ord(query[0].upper())
            low = 0
            high = len(self.arr) - 1
            ingredients = []
            posRange = [0, 0]
            while low <= high:
                pos = mid = (low + high)//2
                midVal = self.arr[mid][0]
                if midVal == query:
                    ingredients.append(self.arr[mid])
                    umid = lmid = mid
                    while True:
                        umid += 1
                        try:
                            midVal = self.arr[umid][0]
                        except IndexError:
                            break
                        if not midVal == query:
                            break
                        ingredients.append(self.arr[umid])
                        posRange[1] += 1
                    while True:
                        lmid -= 1
                        midVal = self.arr[lmid][0]
                        if not midVal == query:
                            break
                        ingredients.append(self.arr[lmid])
                        posRange[0] += 1
                    return ingredients, pos, posRange
                elif midVal < query:
                    low = mid + 1
                else:
                    high = mid - 1
            return None, None, None
        else:
            print("Query length too short")
            return None, None, None
    
    def Search(self, query):
        result, pos, ran = self.BulkSearch(query)
        if result == None:
            return "No item found"
        else:
            for i in range(len(result)):
                if result[i][4].lower() == query.lower():
                    if result[i + 1][4].lower() == query.lower():
                        return "Too many items match query"
                    return result[i]
    
    def Remove(self, query):
        query = query.lower()
        if len(self.arr) == 1:
            print("This is the last item in your pantry")
            self.arr.pop(0)
            self.SaveToDevice()
            return "Item Deleted"
        else:
            results, pos, ran = self.BulkSearch(query.lower())
            if results == None:
                return "Item Not Found"
            else:
                count = 0
                for item in results:
                    if item[4].lower() == query.lower():
                        count += 1
                if count > 1:
                    for i in range(len(results)):
                        if results[i][4].lower() == query.lower():
                            if (i - ran[0]) < 0:
                                delIndex = pos - i
                            elif (i - ran[0]) > 0:
                                delIndex = pos + i
                            else:
                                delIndex = pos
                            self.arr.pop(delIndex)
                            self.SaveToDevice()
                    return "First instance of item deleted."
                for i in range(len(results)):
                    if results[i][4].lower() == query.lower():
                        if (i - ran[0]) < 0:
                            delIndex = pos - i
                        elif (i - ran[0]) > 0:
                            delIndex = pos + i
                        else:
                            delIndex = pos
                        self.arr.pop(delIndex)
                        self.SaveToDevice()
                        return "Item Deleted"
        return "Fatal Error"
        
    def SortFunc(self, array, sortIndex):
        if sortIndex < 0 or sortIndex > (len(self.arr[0])-1):
            print("Sort index out of range, Item list not sorted")
            return self.arr
        n = len(array)
        for i in range(n):
            sorted = True
            for j in range(n - i - 1):
                if int(array[j][sortIndex]) > int(array[j + 1][sortIndex]):
                    array[j], array[j + 1] = array[j + 1], array[j]
                    sorted = False
            if sorted == True:
                return array
        return []

    def SaveToDevice(self):
        #Must be called when the list of items is updated
        CS.Write(self.SortFunc(self.arr, 0))
        return "Write Completed Successfully"
    
    def Clear(self):
        self.arr = []
        self.SaveToDevice()
    
pantry = Pantry()
#for i in range(590):
#   pantry.AddItem([random.randint(23, 259), random.randint(2,23), random.randint(123,2394), ''.join(random.choices(string.ascii_letters, k=7))])
'''
print(pantry.AddItem([112,67,7524,"sugar"]))
print(pantry.AddItem([122,2,6426,"bread"]))
print(pantry.AddItem([123,2,5524,"milk"]))
print(pantry.AddItem([142,13,6342,"eggs"]))
print(pantry.AddItem([152,45,6352,"oranges"]))
print(pantry.AddItem([1562,5,1245,"lead"]))
print(pantry.AddItem([1225,6,1256,"titanium"]))
print(pantry.AddItem([1422,2,2345,"copper"]))
pantry.SaveToDevice()
'''