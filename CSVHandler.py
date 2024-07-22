"""
===CUCINA CSV HANDLER===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 22/05/2024
Last Edited: 27/05/2024
Description:
The python file used to transform and transfer all data for the users pantry.
"""
import csv

"""
INPUTS: None

PROCESS:
The function opens the file 'UserPantryData.csv' in read mode using the open() function.
The CSV data is read. It iterates over each row in the 'reader' object.
- If 'lCount' is 0, it extracts the column headings from the first row and splits them into a list.
- For each key (column heading) in 'headings':
    - If the value in the row can be converted to an integer, it appends the integer value to 'vList'.
    - Otherwise, it appends the value as a string to 'vList'.
The 'vList' is appended to 'array' to store the row data.
Finally, the function returns the 'array' containing the processed CSV data.

OUTPUT: array (list) - A list containing the processed CSV data, with each row represented as a list of values.
"""
def Reader():
    with open('UserPantryData.csv', mode='r') as pantry:
        array = []
        reader = csv.DictReader(pantry)
        lCount = 0 #Debugging
        for row in reader:
            if lCount == 0:
                headings = (", ".join(row)).split(', ')
                lCount += 1 #Debugging
            vList = []
            for keys in headings:
                try:
                    vList.append(int(row[keys]))
                except ValueError:
                    vList.append(row[keys])
            array.append(vList)
            lCount += 1 #Debugging
        #print(f'Processed {lCount} lines.') #Debugging
    return array

"""
INPUTS: array - A list containing the data to be written to the CSV file.

PROCESS:
The function opens the file 'UserPantryData.csv' in write mode using the open() function.
The function writes the column headings as the first row using writer.writerow().
It then iterates over each element in the 'array' list.
- For each element, it writes a row to the CSV file using writer.writerow().

OUTPUT: A string that stating the success of the function.
"""
def Write(array):
    with open('UserPantryData.csv', mode='w') as pantry:
        writer = csv.writer(pantry, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["Letter sort value", "Nutritional value","Item Weight", "Item Quantity", "Expiry date", "Ingredient name"])
        for i in range(len(array)):
            writer.writerow([array[i][0], array[i][1], array[i][2], array[i][3], array[i][4], array[i][5]])
        return "Write completed successfully"