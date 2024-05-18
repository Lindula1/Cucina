#item = ["nutritional value", "quantity", ""]

class Pantry():
    def __init__(self):
        self.arr = []

    def AddItem(self, item):
        for i in item:
            if i == "":
                print("A field is empty")
            else:
                self.arr.append(item)
    
    def Filter(self, query):
        if query == ""
    
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
    
pantry = Pantry()
item = []