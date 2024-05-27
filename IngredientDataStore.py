import random
import string
import pwinput
import CSVHandler as CS
from datetime import date
#item = ["letter sort value (left empty)", "nutritional value", "quantity", "expiry date" "ingredient name"]

class Pantry():
    def __init__(self):
        try:
            self.arr = CS.Reader()
        except FileNotFoundError:
            print("New ingredient list made")
            self.arr = []
        
    def FormatDate(self, item):
        d0 = date(item[3][0], item[3][1], item[3][2])
        d1 = date(1889, 4, 20)
        delta = d1 - d0
        item[3] = delta.days
        return item

    def PantryList(self):
        try:
            raw = CS.Reader()
        except FileNotFoundError:
            print("Fatal Error. No items in pantry")
            raw = []
        ilist = []
        for item in raw: ilist.append(item[4])
        return ilist

    def AddItem(self, item):
        for i in range(len(item) - 1):
            if item[i] == 0:
                return "Field {i} is empty"
        self.arr.append(self.FormatDate(self.LetterSort(item), ))
        pantry.SaveToDevice()
        return "Item Added Successfully"

    def LetterSort(self, item):
        item.insert(0, ord(item[3][0].upper()))
        return item
    
    def BulkSearch(self, query):
        self.arr = self.SortFunc(self.arr, 0)
        if self.arr == []: 
            print("Fatal Error")
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
    
    def Search(self, query, arr):
        arr, pos, ran = self.BulkSearch(self.arr)
        query = ord(query[0].upper())
        if query == None:
            return query
        else:
            for i in arr:
                if i[0] == query:
                    return i
    
    def Remove(self, query):
        if len(self.arr) == 1:
            print("This is the last item in your pantry")
            self.arr.pop(0)
            pantry.SaveToDevice()
            return "Item Deleted"
        else:
            results, pos, ran = self.BulkSearch(query)
            if results == None:
                return "Item Not Found"
            for i in range(len(results)):
                if results[i][4] == query:
                    if (i - ran[0]) < 0:
                        delIndex = pos - i
                    elif (i - ran[0]) > 0:
                        delIndex = pos + i
                    else:
                        delIndex = pos
                    self.arr.pop(delIndex)
                    pantry.SaveToDevice()
                    return "Item Deleted"
        return "Fatal Error"
        
    def SortFunc(self, array, sortIndex):
        if len(array) > 0:
            if sortIndex < 0 or sortIndex > (len(self.arr[0])-1):
                print("Sort index out of range")
                return self.arr
            n = len(array)
            for i in range(n):
                sorted = True
                for j in range(n - i - 1):
                    if array[j][sortIndex] > array[j + 1][sortIndex]:
                        array[j], array[j + 1] = array[j + 1], array[j]
                        sorted = False
                if sorted == True:
                    return array
        return []

    def SaveToDevice(self):
        #Must be called when the list of items is updated
        CS.Write(self.arr)
        return "Write Completed Successfully"
    
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

#Debugging Code
print("This is a backend representation of the software solution and any errors made while entering values is not checked for.\nIf you make any errors the code will simply restart from the beginning or crash :)")
while True:
    choice = input("Enter [a] to Add an item, Enter [s] to Sort the list, Enter [r] to Remove an Item: ")
    if choice.lower() == "s":
        t = input("Enter a sort Index [0 = Alphabetical, 1 = Nutritional Value, 2 = Quantity, 3 = Expeiry Date]: ")
        if t.isdigit():
            t = int(t)
            pantry.SortFunc(pantry.arr, t)
            print(pantry.arr)
        else:
            print("Not a valid input")
    elif choice.lower() == "r":
        pantry.Remove(input("query: "))
        print(pantry.arr)
    elif choice.lower() == "a":
        while True:
            iToAdd = []
            n = input("Enter the nutrional value of the item [numbers only]: ")
            if n.isdigit():
                n = int(n)
                iToAdd.append(n)
            q = input("Enter the quantity of the item you have [numbers only]: ")
            if q.isdigit():
                q = int(q)
                iToAdd.append(q)
            print("Enter Expeiry date in the following format")
            y = input("Enter the year of expeiry [1890 or greater]: ")
            if y.isdigit():
                m = input("Enter the month of expeiry [1-12]: ")
                if m.isdigit():
                    if 1 <= int(m) <= 12:
                        d = input("Enter the date of expeiry, if it exists. Else enter 0: ")
                        if d.isdigit():
                            y = int(n)
                            m = int(m)
                            d = int(d)
                            iToAdd.append([y, m, d])
                            name = input("Enter the name of the item [Do not enter a number first]: ")
                            if not name[0].isdigit():
                                try:
                                    iToAdd.append(name)  
                                    print(pantry.AddItem(iToAdd))
                                    break
                                except ValueError:
                                    print("That date doesn't exist, Try again")
                            else:
                                print("Not a valid name, Please reconsider your education")
                    else:
                        print("Not a number, Try again")
                else:
                    print("Not a valid month, Try again")
            else:
                print("You did not enter a valid number. Try again genius")
    elif choice.lower() == "end": break
    else:
        print(f"'{choice}' is not an option. Learn to read before using this program please.")