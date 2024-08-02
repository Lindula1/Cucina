"""
===CUCINA USER DATA STORE MODULE===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 17/05/2024
Last Edited: 23/07/2024
Description:

"""
import GitCommunication
import json
import datetime
from cryptography.fernet import Fernet
from Hashing import HashingFunc

class DataBase():
    def __init__(self):
        if GitCommunication.ErrorCheck():
            self.checks = True
        else:
            self.arr = self.ReadJson()
            if self.arr != None:
                self.checks = False
            else: self.checks = True

    """
    INPUTS:
        None

    PROCESS:
        - Attempts to load the list of items from a JSON source using `self.ReadJson()`.
        - If loading is successful, assigns the result to `self.arr` and sets `self.checks` to `True`.
        - If a `GitCommunication.github.GithubException` is raised, sets `self.arr` to an empty list.
        - If `self.arr` is empty after loading or if an exception was caught, returns `True`.

    OUTPUTS:
        - (bool) - Returns `True` if the list is empty or if an exception was raised during loading. Otherwise, returns `None`.
    """
    def Load(self):
        try:
            self.arr = self.ReadJson()
            self.checks = True
        except GitCommunication.github.GithubException:
            self.arr = []
        if self.arr == []:
            return True
    
    """
    INPUTS:
        data (bytes): The data to be encrypted. This should be in bytes format, typically the content of a JSON file.

    PROCESS:
        - Reads the encryption key from the file keyFile.key.
        - Uses the Fernet encryption scheme to encrypt the provided data.
        - Writes the encrypted data to a file named Accounts.json.

    OUTPUTS:
        - (bytes) - Returns the encrypted data.
    """
    def EncryptJson(self, data):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open("Accounts.json", "wb") as jsonFile:
            jsonFile.write(encrypted)
        return encrypted

    """
    INPUTS: None

    PROCESS:
        - Generates a new encryption key using the `Fernet` encryption scheme.
        - Saves the generated key to a file named `keyFile.key`.
        - Reads the content of the `Accounts.json` file.
        - Encrypts the content of `Accounts.json` using the new key.
        - Updates the class attribute `arr` with the encrypted data.

    OUTPUTS: None
    """
    def GenEncryptionKey(self):
        key = Fernet.generate_key()
        with open('keyFile.key', 'wb') as filekey:
            filekey.write(key)
        fernet = Fernet(key)
        with open("Accounts.json", 'rb') as file:
            original = file.read()
        self.arr = fernet.encrypt(original)
    
    """
    INPUTS:
        None

    PROCESS:
        - Reads the encryption key from the file `keyFile.key`.
        - Uses the `Fernet` encryption scheme with the read key to decrypt the encrypted data.
        - Retrieves the encrypted data from an external source using `GitCommunication.LoadGist()`.
        - Decrypts the retrieved data using the `Fernet` scheme.
        - Loads the decrypted data into a JSON object.

    OUTPUTS:
        - (dict) - Returns the decrypted JSON data as a Python dictionary. If no encrypted data is found, behavior may vary based on external implementation.
    """
    def DecryptJson(self):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        encrypted = GitCommunication.LoadGist()
        '''
        with open("Accounts.json", 'rb') as encFile:
            encrypted = encFile.read()
        '''
        if encrypted:
            raw = json.loads(fernet.decrypt(encrypted))
            return raw
    
    """
    INPUTS:
        account (dict): A dictionary representing a user account with required fields.

    PROCESS:
        - Appends the provided `account` to the internal list `arr` after processing it with the `AddUserID` method.
        - Sorts the updated list `arr` using the `Sort` method.
        - Saves the sorted list online using the `SaveOnline` method.

    OUTPUTS:
        None
    """
    def AddTo(self, account):
        self.arr.append(self.AddUserID(account))
        self.arr = self.Sort(self.arr)
        self.SaveOnline()

    """
    INPUTS:
        account (dict): A dictionary representing a user account with a "username" field.

    PROCESS:
        - Extracts the first character of the username from `account` and converts it to uppercase.
        - Computes a numeric ID (`oId`) from the ASCII value of this uppercase character.
        - Generates a unique timestamp-based ID (`nId`) and assigns it to the `uid` field in the `account` dictionary.
        - If the computed `oId` is 99 or higher, prints an error message, sets `oId` to 0, and creates a list with `oId` and `account`.
        - Otherwise, creates a list with `oId` and `account` and returns it.

    OUTPUTS:
        list: A list where the first element is `oId` and the second element is the `account` dictionary with the added `uid` field.
    """
    def AddUserID(self, account):
        usrnmIL = account["username"][0].upper()
        oId = ord(usrnmIL)
        time = datetime.datetime.now()
        nId = time.strftime('%Y%m%d%H%M%S%f')
        account["uid"] = nId
        if oId >= 99:
            print("\033[31mFATAL ERROR, oId out of range\033[0m", oId)
            oId = 0
            account = [oId, account]
            return account
        account = [oId, account]
        return account

    """
    INPUTS:
        account (list): A list where the second element is a dictionary containing a "uid" field.

    PROCESS:
        - Extracts the `uid` field from the dictionary within the `account` list.
        - Parses the `uid` string to extract specific segments of the timestamp.
        - The `uid` string is expected to be in the format `YYYYMMDDHHMMSSFFFF`, where:
        - The first segment (index 4) represents the year.
        - The second segment (index 6) represents the month and day.
        - The third segment (index 8) represents the time (hours, minutes, seconds).
        - The last segment (index 16) represents the microseconds.
        - Appends these segments to the `date` list.

    OUTPUTS:
        list: A list containing segments of the `uid` string, representing year, month, day, time, and microseconds.
    """
    def RevertId(self, account):
        uId = account[1]["uid"]
        date = []
        for i in range(4,len(uId),2):
            if i == 4:
                date.append(uId[i-4:i])
            elif i == 16:
                date.append(uId[i-2:len(uId)])
                break
            else:
                date.append(uId[i-2:i])
        return date

    """
    INPUTS:
        array (list): A list of lists, where each sub-list contains at least one sortable element (the first element is used for sorting).

    PROCESS:
        - Implements a bubble sort algorithm to sort the `array` based on the first element of each sub-list.
        - Iterates over the `array`, comparing adjacent elements and swapping them if they are out of order.
        - Continues iterating until no more swaps are needed, indicating that the array is sorted.

    OUTPUTS:
        list: The sorted list, or an empty list if the input list is empty.
    """
    def Sort(self, array):
        if len(self.arr) > 0:
            n = len(array)
            for i in range(n):
                sorted = True
                for j in range(n - i - 1):
                    if array[j][0] > array[j + 1][0]:
                        array[j], array[j + 1] = array[j + 1], array[j]
                        sorted = False
                if sorted == True:
                    return array
        return []
    
    """
    INPUTS:
        None

    PROCESS:
        - Serializes the `self.arr` list to a JSON formatted string using `json.dumps`.
        - Converts the JSON string into bytes with UTF-8 encoding.
        - Encrypts the byte data using the `EncryptJson` method.
        - Writes the encrypted data to a file named `Accounts.json` in binary write mode.

    OUTPUTS:
        None
    """
    def SaveLocally(self):
        dumped = json.dumps(self.arr, indent=4)
        with open("Accounts.json", "wb") as file:
            file.write(self.EncryptJson(bytes(dumped.encode("utf-8"))))

    """
    INPUTS:
        None

    PROCESS:
        - Checks the `self.checks` attribute to determine if the data should be saved online.
        - If `self.checks` is True, serializes the `self.arr` list to a JSON formatted string using `json.dumps`.
        - Converts the JSON string into bytes with UTF-8 encoding.
        - Encrypts the byte data using the `EncryptJson` method.
        - Updates an online gist with the encrypted data using `GitCommunication.UpdateGist`.
        - If `self.checks` is False, calls `SaveLocally` to save the data locally.

    OUTPUTS:
        None
    """
    def SaveOnline(self):
        if self.checks:
            dumped = json.dumps(self.arr, indent=4)
            GitCommunication.UpdateGist(self.EncryptJson(bytes(dumped.encode("utf-8"))))
        else:
            self.SaveLocally()
            
    """
    INPUTS:
        None

    PROCESS:
        - Calls the `DecryptJson` method to retrieve and decrypt the JSON data.
        - The `DecryptJson` method reads the encryption key, decrypts the JSON data, and loads it.

    OUTPUTS:
        - (dict) - Returns the decrypted and parsed JSON data as a Python dictionary.
    """
    def ReadJson(self):
        return self.DecryptJson()
        
    """
    INPUTS:
        query (str): The search query, which is expected to be a string. Only the first character is used for searching.

    PROCESS:
        - Checks if the `arr` is empty and prints an error message if it is, then returns `None, None, None`.
        - Converts the first character of the query to its ASCII value.
        - Performs a binary search on the `arr` based on the ASCII value.
        - Collects all items with the matching ASCII value into the `accounts` list.
        - Determines the range of positions (`posRange`) where the matching items are found.

    OUTPUTS:
        - (list, int, list) - Returns a tuple containing:
            - `accounts`: A list of accounts that match the query.
            - `pos`: The position of the first match in the sorted list.
            - `posRange`: A list containing the start and end offsets of the matched range within the sorted list.
    """
    def BulkSearch(self, query):
        if self.arr == []: 
            self.arr = self.Sort(self.arr)
            print("\033[41mFATAL ERROR DATABSE EMPTY\033[0m")
            return None, None, None
        query = ord(query[0].upper())
        low = 0
        high = len(self.arr) - 1
        accounts = []
        posRange = [0, 0]
        while low <= high:
            pos = mid = (low + high)//2
            midVal = self.arr[mid][0]
            if midVal == query:
                accounts.append(self.arr[mid])
                umid = lmid = mid
                while midVal == query:
                    umid += 1
                    try:
                        midVal = self.arr[umid][0]
                    except IndexError:
                        break
                    if not midVal == query:
                        break
                    accounts.append(self.arr[umid])
                    posRange[1] += 1
                while True:
                    lmid -= 1
                    midVal = self.arr[lmid][0]
                    if not midVal == query:
                        break
                    accounts.append(self.arr[lmid])
                    posRange[0] += 1
                return accounts, pos, posRange
            elif midVal < query:
                low = mid + 1
            else:
                high = mid - 1
        return None, None, None
    
    def SaveLoginInfo(self, usrm):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open("SaveData.json","wb") as file:
            encrypted = fernet.encrypt(bytes(usrm.encode("utf-8")))
            file.write(encrypted)
    
    def ClearLoginInfo(self):
        with open("SaveData.json","wb") as file:
            file.write(b'')
    
    def LoadLoginInfo(self):
        with open('keyFile.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)
        with open("SaveData.json","rb") as file:
            raw = file.read()
            if not raw == b'':
                decrypted = str((fernet.decrypt(raw)).decode("utf-8"))
                return decrypted
        return None

run = DataBase()

if __name__ == "__main__":
    #run.GenEncryptionKey()
    #print(run.arr)
    #run.SaveLocally()
    #run.SaveOnline()
    #print(run.DecryptJson())
    #run.SaveLoginInfo("Men")
    print(run.LoadLoginInfo())