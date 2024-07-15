"""
===CUCINA PDF HANDLER===
Author: Lindula Pallawela Appuhamilage
Contributors: -
Date Created: 27/05/2024
Last Edited: 04/06/2024
Description: 
A python file holding all functions for handling any and all PDF data.
"""
import sys
import os
from pypdf import PdfReader
import json
sys.path.insert(0, "../Cucina/PDFs")

"""
INPUTS: pdf - The name of the PDF file to be read.

PROCESS:
The function attempts to read the PDF file from a specific directory relative to the current working directory.
The function then extracts text from each page of the PDF, identifies lines containing ingredient information and step information,
and adds them to separate lists (ingredients and steps) while ignoring lines related to utensils or options.
The function also collects all text from the PDF pages into a separate list (text).

OUTPUT: 
ingredients - A list of ingredient lines extracted from the PDF, 
steps - A list of step lines extracted from the PDF,
text - A list containing all text lines from the PDF.
"""
def Read(pdf):
    try:
        reader = PdfReader(f"../Cucina/PDFs/{pdf}.pdf")
    except FileNotFoundError:
        reader = PdfReader(f"C:/Users/budwi/OneDrive/Documents/GitHub/Cucina/PDFs/{pdf}.pdf")
        print("Directory Error, local file location used")
    text = []
    ingredients = []
    steps = []
    for i in reader.pages:
        ingLine = False
        stepLine = False    
        page = ""
        page = i.extract_text()
        #print(page)
        for line in page.split("\n"):
            if "ingredient" in line.lower():
                #print("Ingredients being added")
                ingLine = True
                stepLine = False
            elif "method" in line.lower() or "step" in line.lower():
                #print("Steps being added")
                stepLine = True
                ingLine = False
            elif "utensils" in line.lower() or  "options"  in line.lower():
                #print("Random stuff")
                ingLine = False
                stepLine = False
            else:
                pass

            if ingLine:
                #print(line)
                if "\t" in line:
                    t = line.split("\t")
                    line = ' '.join(t)
                    items = line.split("• ")
                    for j in items:
                        if "\uf0b7" in j:
                            line.replace(j, "")
                        if "(" in t or ")" in j:
                            line.replace(j, "")
                        ingredients.append(j.strip())
                else:
                    ingredients.append(line.strip())
                    itm, qty = Quantity(line)
                    #print(f"Item: {itm}, The quantity: {qty}")
                # ingredients.append(' '.join([print(word.strip()) or 'a' for word in line.split(' ')]))
                # for word in line.split(' '):
                #    print(':', word.strip(), ':', sep='')
                # ingredients.append(line.replace(' ', ''))
                #new_line = ''
                #for c in line:
                #    new_line += c

                #ingredients.append(new_line)
            if stepLine:
                #print(line)
                steps.append(line.strip())
            else:
                #print(line)
                text.append(line.strip())

    return ingredients, steps, text
"""
INPUTS: None

PROCESS:
The function scans the directory "../Cucina/Pdfs/" using the os.scandir() method to retrieve a list of files in that directory.
For each item (file) in the directory, the name of the item is extracted and added to a list (items).

OUTPUT: The function indirectly calls the SavePDFData() function with the 'items' list as an argument to save the PDF data.
"""
def ListPDFs():
    items = []
    with os.scandir("../Cucina/Pdfs/") as files:
        for item in files: items.append(item.name)
    SavePDFData(items)

"""
INPUTS: arr - A list of PDF file names.

PROCESS:
The function first constructs the file path by joining the directory "../Cucina/PDFs" and the filename "PdfInformation.json" using os.path.join().
It then converts the 'arr' list to a JSON-formatted string with indentation using the json.dumps() method.
Finally, it opens the file at the constructed path in write mode and writes the JSON string to the file.

OUTPUT: The function saves the JSON-formatted data to a file.
"""
def SavePDFData(arr):
    path = os.path.join("../Cucina/PDFs","PdfInformation.json")
    dumped = json.dumps(arr, indent=4)
    with open(path, "w") as jsn:
        jsn.write(dumped)
        
"""
INPUTS: None

PROCESS:
The function constructs the file path by joining the directory "../Cucina/PDFs" and the filename "PdfInformation.json" using os.path.join().
It then opens the file at the constructed path in read mode using the open() function.
The JSON data from the file is loaded using json.load() and stored in the 'raw' variable.
Each element of the 'raw' list is stripped of the ".pdf" extension using the rstrip() method.
The modified 'raw' list is returned as the output.

OUTPUT: raw (list) - The modified list obtained from the JSON file.
"""
def ReadPDFData():
    path = os.path.join("../Cucina/PDFs","PdfInformation.json")
    with open(path, "r") as jsn:
        raw = json.load(jsn)
        for i in range(len(raw)):
            raw[i] = raw[i].rstrip(".pdf")
        return raw

"""
INPUTS: entry - A string representing an ingredient line.

PROCESS:
The function splits the 'entry' string into a list of words using the split() method.
It initializes 'item' as an empty string and 'quantity' as None.
It iterates over each word in the list. If the word contains any digit character, it is considered the 'quantity'.
Otherwise, the word is part of the 'item' name.
Finally, the function returns the 'item' and 'quantity' as a tuple.

OUTPUT: A tuple containing the 'item' (list) and 'quantity' (list) containing repective values.
"""
def Quantity(entry):
    sep = entry.split(" ")
    item = ""
    quantity = None
    for word in sep:
        if any(char.isdigit() for char in word):
            quantity = word
        else:
            item = item.strip() + " " + word.strip()
    #item = " ".join(sep)
    return item, quantity

if __name__ == "__main__":
    ingredients, steps, text = Read("beef_stroganoff")
    print(ReadPDFData())

'''
    print("***********STEPS***********")
    for i in steps: print(i)
    print("***********INGREDIENTS***********")
    for j in ingredients: print(j)
    print("***********TEXT***********")
    print(text)
'''

