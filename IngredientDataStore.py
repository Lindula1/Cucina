"""
===CUCINA INGREDIENT DATA STORAGE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 18/05/2024
Last Edited: 06/07/2024
Description:
This python file holds all functions for transforming
and transferring any and all ingredient data.

Item variable data structure:
item = ["letter sort value (left empty)", "nutritional value", "item weight", "item count", "expiry date" "ingredient name"]
"""
import CSVHandler as CS
import datetime

class Pantry():
    def __init__(self):
        try:
            self.arr = CS.Reader()
            self.checks = False
        except FileNotFoundError:
            self.arr = []
            self.checks = True
    
    def Load(self):
        try:
            self.arr = CS.Reader()
        except FileNotFoundError:
            self.arr = []
            return True
    """   
    INPUTS: item - A list representing an item, where item[4] is a date in the format [year, month, day].
    PROCESS:
    The function takes the date, converts it to a datetime.date object,
    initializes a datetime.date object representing the date April 20, 1889,
    calculates the difference between the objects,
    and returns the modified item.
    OUTPUT: item[4] - The number of days between the original date and April 20, 1889.
    """
    def FormatDate(self, item):
        d0 = datetime.date(item[4][0], item[4][1], item[4][2])
        self.d1 = datetime.date(1889, 4, 20)
        delta = d0 - self.d1
        item[4] = delta.days
        return item
    
    """
    INPUTS: self - Reference to the current instance of the class, item - A list containing the item information, including the number of days until the expiry date.

    PROCESS:
    The function calculates the expiry date by adding the number of days (item[4]) to a fixed reference date.
    It then converts the expiry date to a formatted string representation ("%Y/%m/%d").
    The function splits the formatted date string into year, month, and day components.
    It calculates the number of days left until the expiry date by subtracting the current date from the expiry date.
    The result is returned as the expiry date string and the number of days left.

    OUTPUT: expDate - The expiry date in the format "YYYY/MM/DD", daysLeft - The number of days left until the expiry date.
    """
    def DateRevert(self, item):
        d0 = datetime.timedelta(item[4])
        d1 = datetime.datetime(1889,4,20,0,0)
        d2 = datetime.date.today()
        expDate = (d1 + d0).strftime("%Y/%m/%d")
        explist = expDate.split("/")
        daysLeft = datetime.date(int(explist[0]), int(explist[1]), int(explist[2])) - d2
        return expDate, daysLeft.days

    """
    INPUTS: None

    PROCESS:
        Attempts to read the pantry data using `CS.Reader()`.
        - If a `FileNotFoundError` occurs:
            - Prints an error message indicating no items are in the pantry and an empty list will be created.
            - Initializes `raw` as an empty list.
        - If no error occurs:
            - Processes the data read from `CS.Reader()`.
            - Creates a list `ilist` containing the 6th element (index 5) from each item in `raw`.
        - Returns the `raw` list of pantry items.

    OUTPUTS:
        raw (list) - A list of pantry items. Each item in the list is assumed to be a structure from which the 6th element (index 5) is extracted for `ilist` but not used further.
    """
    def PantryList(self):
        try:
            raw = CS.Reader()
        except FileNotFoundError:
            raw = []
        ilist = []
        for item in raw: ilist.append(item[5])
        return raw

    """
    INPUTS:
        item (list) - A list containing item data where each element corresponds to different attributes of the item to be added.

    PROCESS:
        Iterates through each element in the `item` list except the last one:
            - Checks if the current element is `0`.
            - If an element is `0`, returns an error message indicating which field is empty.
        Appends the formatted and sorted item to `self.arr`.
        Calls `self.SaveToDevice()` to save the updated list.
        Returns a success message indicating the item was added successfully.

    OUTPUTS:
        str - A message indicating the result of the operation:
            - "Field {i} is empty. HOW?" if any field in the item is empty.
            - "Item Added Successfully" if the item was added to the list successfully.
    """
    def AddItem(self, item):
        for i in range(len(item) - 1):
            if item[i] == 0:
                return "Field {i} is empty. HOW?"
        if self.Search(item[-1])[-1] == item[-1]:
            return "Item already exists"
        else:
            self.arr.append(self.FormatDate(self.LetterSort(item)))
            self.SaveToDevice()
            return "Item Added Successfully"

    """
    INPUTS:
        item (any) - An item to be added directly to `self.arr`. The structure or type of `item` should be compatible with `self.arr`.

    PROCESS:
        Appends the provided `item` to the `self.arr` list.
        Calls `self.SaveToDevice()` to persist the updated list.

    OUTPUTS: None
    """
    def AddRaw(self, item):
        self.arr.append(item)
        self.SaveToDevice()
        
    """
    INPUTS:
        item (list) - A list where the 5th element (index 4) is expected to be a string from which the first character is used for sorting.

    PROCESS:
        Inserts the ASCII value of the uppercase version of the first character of the 5th element (index 4) into the beginning of the `item` list.
        Returns the modified `item` list.

    OUTPUTS:
        list - The modified `item` list with the ASCII value prepended to the original elements.
    """
    def LetterSort(self, item):
        item.insert(0, ord(item[4][0].upper()))
        return item
    
    """
    INPUTS:
        query (str) - A string used for searching the `self.arr` list. It is expected that the first character of the query will be used for comparison.

    PROCESS:
        - Checks if the length of `query` is greater than 0. If not, prints an error message and returns `None` values.
        - Converts the first character of `query` to its uppercase ASCII value.
        - Sorts `self.arr` using `self.SortFunc()` with the sort key as `0`.
        - If `self.arr` is empty after sorting, prints a message and returns `None` values.
        - Performs a binary search to locate the range of items in `self.arr` that match the ASCII value of `query`:
            - Initializes `low`, `high`, `ingredients`, and `posRange`.
            - Iteratively narrows the search range until the desired items are found.
            - Collects all items with the matching ASCII value and determines their positions and range in `self.arr`.
        - Returns a tuple containing:
            - `ingredients` (list) - A list of items that match the search query.
            - `pos` (int) - The position of the first matching item.
            - `posRange` (list) - A list containing the number of matches before and after the initial match.

    OUTPUTS:
        tuple - A tuple of:
            - ingredients (list) - Items matching the query.
            - pos (int) - Position of the first match.
            - posRange (list) - List indicating the range of matches around the initial match.
            - If no items match or if the query length is too short, returns `None` values.
    """
    def BulkSearch(self, query):
        if len(query) > 0:
            self.arr = self.SortFunc(self.arr, 0)
            if self.arr == [] or self.arr == None: 
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
                            if self.arr[umid] not in ingredients: 
                                ingredients.append(self.arr[umid])
                            posRange[1] += 1
                        except IndexError:
                            break
                        if not midVal == query:
                            break
                    while True:
                        lmid -= 1
                        try:

                            midVal = self.arr[lmid][0]
                            if self.arr[lmid] not in ingredients: 
                                ingredients.append(self.arr[lmid])
                            posRange[0] += 1
                        except IndexError:
                            break
                        if not midVal == query:
                            break
                    return ingredients, pos, posRange
                elif midVal < query:
                    low = mid + 1
                else:
                    high = mid - 1
            return None, None, None
        else:
            return None, None, None
    
    """
    INPUTS:
        query (str) - The string used to search for an item in `self.arr`.

    PROCESS:
        - Calls `self.BulkSearch(query)` to perform a bulk search based on the query.
        - Checks the result of the `BulkSearch` function:
            - If `result` is `None`, returns "No item found".
            - If `result` contains items:
                - Iterates through the `result` list to find an item that matches the query.
                - Compares the `4th` element (index `4`) of each item with the `query`.
                - If more than one item matches the query, returns "Too many items match query".
                - If exactly one item matches, returns that item.

    OUTPUTS:
        - "No item found" (str) - If no items match the query or if `BulkSearch` returns `None`.
        - "Too many items match query" (str) - If more than one item matches the query.
        - item (list) - If exactly one item matches the query.
    """
    def Search(self, query):
        result, pos, ran = self.BulkSearch(query)
        if result == None:
            return ["0","0","0","0","0"]
        else:
            for i in range(len(result)):
                if result[i][-1] == query:
                    return result[i]
        return ["0","0","0","0","0"]
    
    def Remove(self, query):
        self.arr = self.SortFunc(self.arr, 0)
        if len(self.arr) <= 1:
            try:
                self.arr.pop(0)
                self.SaveToDevice()
                return "Item Deleted"
            except IndexError:
                pass
            return "Error"
        else:
            results, pos, ran = self.BulkSearch(query)
            if results == None:
                return "Item Not Found"
            else:
                count = 0
                for item in results:
                    if item[-1] == query:
                        count += 1
                if count > 1:
                    for i in range(len(results)):
                        if results[i][-1] == query:
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
                    if results[i][-1] == query:
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
    """
    INPUTS:
        query (str) - The string used to identify the item to be removed from `self.arr`.

    PROCESS:
        - Converts `query` to lowercase for case-insensitive comparison.
        - If `self.arr` contains only one item:
            - Prints a message indicating it is the last item.
            - Removes the item from `self.arr` and saves the updated list.
            - Returns "Item Deleted".
        - If `self.arr` contains more than one item:
            - Calls `self.BulkSearch(query.lower())` to find matching items.
            - If no items are found, returns "Item Not Found".
            - Counts the number of items that match the `query`.
                - If multiple items are found:
                    - Identifies the index of the item to remove based on its position in the list.
                    - Removes the first matching item and saves the updated list.
                    - Returns "First instance of item deleted."
                - If a single item is found:
                    - Identifies the index of the item to remove based on its position in the list.
                    - Removes the item and saves the updated list.
                    - Returns "Item Deleted".
        - Returns "Fatal Error" if an unexpected issue occurs.

    OUTPUTS:
        - "Item Deleted" (str) - If the item is successfully removed from `self.arr`.
        - "First instance of item deleted." (str) - If multiple items match the query and the first instance is deleted.
        - "Item Not Found" (str) - If no items match the query.
        - "Fatal Error" (str) - If an unexpected error occurs.
    """
    def SortFunc(self, array, sortIndex):
        n = len(array)
        if n < 1: return self.arr
        if abs(sortIndex) > (len(self.arr[0])-1):
            return self.arr
        for i in range(n):
            sorted = True
            for j in range(n - i - 1):
                if int(array[j][sortIndex]) > int(array[j + 1][sortIndex]):
                    array[j], array[j + 1] = array[j + 1], array[j]
                    sorted = False
            if sorted == True:
                return array
        return self.arr

    """
    INPUTS: None

    PROCESS:
        - Calls `CS.Write()` to save the sorted list of items to the device.
            - The list is sorted using `self.SortFunc(self.arr, 0)`, which sorts `self.arr` based on the specified criteria.
        - Returns a message indicating the success of the write operation.

    OUTPUTS:
        - "Write Completed Successfully" (str) - Confirmation that the list has been saved successfully.
    """
    def SaveToDevice(self):
        #Must be called when the list of items is updated
        CS.Write(self.SortFunc(self.arr, 0))
        return "Write Completed Successfully"
    
    """
    INPUTS: None

    PROCESS:
        - Clears the list `self.arr` by setting it to an empty list.
        - Calls `self.SaveToDevice()` to update the device with the now-empty list.

    OUTPUTS:
        - None
    """
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