import random
import string
import CSVHandler as CS
#item = ["letter sort value (left empty)", "nutritional value", "quantity", "expiry date" "ingredient name"]

class Pantry():
    def __init__(self):
        self.arr = []

    def AddItem(self, item):
        for i in range(len(item) - 1):
            if item[i] == 0:
                print(f"Field {i} is empty")
        self.arr.append(self.LetterSort(item))

    def LetterSort(self, item):
        item.insert(0, ord(item[3][0].upper()))
        return item
    
    def BulkSearch(self, query):
        self.arr = self.SortFunc(self.arr, 0)
        if self.arr == -1: 
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
        else:
            results, pos, ran = self.BulkSearch(query)
            for i in range(len(results)):
                print(i)
                if results[i][4] == query:
                    if (i - ran[0]) < 0:
                        delIndex = pos - i
                    elif (i - ran[0]) > 0:
                        delIndex = pos + i
                    else:
                        delIndex = pos
                    self.arr.pop(delIndex)
                    return "Item Deleted"
        return "Item Not Found"
        
    def SortFunc(self, array, sortIndex):
        n = len(array)
        for i in range(n):
            sorted = True
            for j in range(n - i - 1):
                if array[j][sortIndex] > array[j + 1][sortIndex]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    sorted = False
            if sorted == True:
                return array
        return -1

    def SaveToDevice(self):
        CS.Write(self.arr)
    
pantry = Pantry()
#for i in range(590):
#    pantry.AddItem([random.randint(23, 259), random.randint(2,23), random.randint(123,2394), ''.join(random.choices(string.ascii_letters, k=7))])

pantry.AddItem([112,67,7524,"sugar"])
pantry.AddItem([122,2,6426,"bread"])
pantry.AddItem([123,2,5524,"milk"])
pantry.AddItem([142,13,6342,"eggs"])
pantry.AddItem([152,45,6352,"oranges"])
pantry.AddItem([1562,5,1245,"lead"])
pantry.AddItem([1225,6,1256,"titanium"])
pantry.AddItem([1422,2,2345,"copper"])

pantry.SaveToDevice()
print(CS.Reader())

'''
print(pantry.arr)
pantry.SortFunc(pantry.arr, 0)
print(pantry.BulkSearch(int(input("number:"))))
while len(pantry.arr) > 0:
    pantry.Remove(input("query: "))
    print(pantry.arr)
'''