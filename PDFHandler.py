import sys
import os
from pypdf import PdfReader
import json
sys.path.insert(0, "../Cucina/PDFs")

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

def ListPDFs():
    items = []
    with os.scandir("../Cucina/Pdfs/") as files:
        for item in files: items.append(item.name)
    SavePDFData(items)

def SavePDFData(arr):
    path = os.path.join("../Cucina/PDFs","PdfInformation.json")
    dumped = json.dumps(arr, indent=4)
    with open(path, "w") as jsn:
        jsn.write(dumped)
        
def ReadPDFData():
    path = os.path.join("../Cucina/PDFs","PdfInformation.json")
    with open(path, "r") as jsn:
        raw = json.load(jsn)
        for i in range(len(raw)):
            raw[i] = raw[i].rstrip(".pdf")
        return raw

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

