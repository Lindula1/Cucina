import random
import string
import pwinput
import CSVHandler as CS
import datetime
#item = ["letter sort value (left empty)", "nutritional value", "quantity", "expiry date" "ingredient name"]

class Pantry():
    def __init__(self):
        try:
            self.arr = CS.Reader()
        except FileNotFoundError:
            print("New ingredient list made")
            self.arr = []
        
    def FormatDate(self, item):
        d0 = datetime.date(item[3][0], item[3][1], item[3][2])
        self.d1 = datetime.date(1889, 4, 20)
        delta = d0 - self.d1
        item[3] = delta.days
        return item
    
    def DateRevert(self, item):
        d0 = datetime.timedelta(item[3] - 1)
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
            print("No items left to delete")
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
        arr, pos, ran = self.BulkSearch(query)
        query = ord(query[0].upper())
        if query == None:
            return query
        else:
            for i in arr:
                if i[0] == query:
                    return i
    
    def Remove(self, query):
        query = query.lower()
        if len(self.arr) == 1:
            print("This is the last item in your pantry")
            self.arr.pop(0)
            pantry.SaveToDevice()
            return "Item Deleted"
        else:
            results, pos, ran = self.BulkSearch(query)
            if results == None:
                return "Item Not Found"
            else:
                for i in range(len(results)):
                    if results[i][4].lower() == query.lower():
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