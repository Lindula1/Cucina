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
import fitz
import json
sys.path.insert(0, "../Cucina/PDFs")

"""
[A-Z] Look for one uppercase letter.
[A-Z]{3} Look for three consecutive uppercase letters.
[0-9]{5} Look for five consecutive digits.
[0-9]+ Look for one or more digits.
[^a-z] Look for everything except lowercase a to z.
\s (Lowercase s) Look for one whitespace character (space, tab, etc).
\S (Uppercase S) Look for any character not whitespace.
"""

import pdfplumber
import re

def extract_ingredients_from_pdf(pdf_path):
    """
    Extracts ingredients from a recipe PDF using text extraction and regex.

    INPUTS:
        pdf_path (str): The file path to the PDF.

    OUTPUTS:
        ingredients (list of str): List of extracted ingredients.
    """

    def extract_text_from_pdf(pdf_path):
        """Extract text from each page of the PDF."""
        text = ""
        with fitz.open(f"../Cucina/PDFs/{pdf_path}.pdf") as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
        return text

    def clean_text(text):
        """Clean up text by removing special characters and unwanted formatting."""
        # Replace non-breaking spaces with regular spaces
        text = text.replace('\xa0', ' ')
        # Replace newlines and multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def find_ingredients(text):
        """Identify ingredients using regex patterns."""
        # Regex pattern for common ingredient formats
        ingredient_pattern = r'\b(\d+(?:[\.,]\d+)?\s*(?:cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|gram|grams|kg|kilogram|ml|milliliter|liter|ounces|ounce|pound|pounds|lb|lbs|oz|g|kg|l|tbsp|tsp)?\s*[a-zA-Z\s]+)\b'

        # Find all matches
        matches = re.findall(ingredient_pattern, text, re.IGNORECASE)

        # Filter out known date, time, and timing patterns
        date_time_pattern = r'\b(\d{1,4}[/-]\d{1,2}[/-]\d{1,4}|\d{1,2}:\d{2}(?:\s?[AP]M)?|20[0-9]{2})\b'
        timing_pattern = r'\b\d+\s*(?:minute|minutes|hour|hours|second|seconds)\b'

        filtered_matches = [
            match for match in matches
            if not re.search(date_time_pattern, match) and not re.search(timing_pattern, match)
        ]

        # Clean and deduplicate ingredients
        ingredients = list(set(filtered_matches))
        ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]

        return ingredients

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Clean text
    clean_text_content = clean_text(text)
    
    # Find and return ingredients
    ingredients = find_ingredients(clean_text_content)
    return ingredients

def Read2(pdf_path):
    ingredients = []
    ingredient_section_found = False
    
    with pdfplumber.open(f"../Cucina/PDFs/{pdf_path}.pdf") as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
        
        # Look for common ingredient section headers
        ingredient_headers = ["ingredients:", "you will need:", "you'll need:", "shopping list:"]
        start_index = -1
        for header in ingredient_headers:
            start_index = full_text.lower().find(header)
            if start_index != -1:
                ingredient_section_found = True
                full_text = full_text[start_index:]
                break
        
        if not ingredient_section_found:
            # If no header found, try to identify ingredient patterns
            regex = r'\n[\d½¼¾⅓⅔⅛⅜⅝⅞]+\s*(?:cup|g|kg|ml|l|tsp|tbsp|oz|pound|lb)s?\s+\w+'
            out = re.findall(r'\•.*|\uf0b7.*', full_text)
            potential_ingredients = re.findall(r'(\d+g.*)|(\d+\s{1}\S+)', full_text)
            out.extend(potential_ingredients)
            ingredientList = []
            for ingredient in out:
                ingredient = re.sub(r'\([^)]*\)*\s', '', ingredient).strip()
                ingredient = re.sub(r'^(of|and)\s', '', ingredient, flags=re.IGNORECASE)
                ingredient = re.sub(r'•\s|\uf0b7\s', '', ingredient, flags=re.IGNORECASE)
                ingredient = re.sub(r'\,.*\s', '', ingredient, flags=re.IGNORECASE)
                ingredientList.append(ingredient)
            return [], ingredientList
            if potential_ingredients:
                ingredient_section_found = True
                full_text = "\n".join(potential_ingredients)
        
        if ingredient_section_found:
            # Split text into lines
            lines = full_text.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and common non-ingredient lines
                if not line or any(header in line.lower() for header in ingredient_headers) or \
                   line.lower().startswith(("method:", "instructions:", "directions:", "to make")):
                    continue
                
                # Remove quantities and units
                #ingredient = re.sub(r'^[\d½¼¾⅓⅔⅛⅜⅝⅞/\-\s]+(?:[a-zA-Z]+\s)?', '', line)
                
                # Remove additional descriptions in parentheses
                ingredient = re.sub(r'\([^)]*\)', '', ingredient).strip()
                
                # Remove common prefixes
                ingredient = re.sub(r'^(of|and)\s', '', ingredient, flags=re.IGNORECASE)
                
                # Add ingredient if it's not empty, not too short, and not already in the list
                if ingredient and len(ingredient) > 1 and ingredient.lower() not in [i.lower() for i in ingredients]:
                    ingredients.append(ingredient)
    
    return ingredients, potential_ingredients

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
            if "ingredient" in line.lower() or "what you need" in line.lower():
                #print("Ingredients being added")
                ingLine = True
                stepLine = False
            elif "method" in line.lower() or "step" in line.lower():
                #print("Steps being added")
                stepLine = True
                ingLine = False
            elif "utensils" in line.lower() or  "options"  in line.lower():
                #print("Random stuff")/
                ingLine = False**-**+-+                stepLine = False
            elif "equipment" in line.lower():
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
                    if len(line) > 1:
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
                if len(line) > 1:
                    steps.append(line.strip())
            else:
                if len(line) > 1:
                    text.append(line.strip())

        ingredients = ingredients[1:-1]
        steps = steps[1:-1]
        text = text[1:-1]

    return ingredients, steps, text
"""
INPUTS: None

PROCESS:
The function scans the directory "../Cucina/Pdfs/" using the os.scandir() method to retrieve a list of files in that directory.
For each item (file) in the directory, the name of the item is extracted and added to a list (items). The function indirectly 
calls the SavePDFData() function with the 'items' list as an argument to save the PDF data.

OUTPUT: items - A list of all recipe names
"""
def ListPDFs():
    items = []
    with os.scandir("../Cucina/PDFs/") as files:
        for item in files: items.append(item.name)
    SavePDFData(items)
    return items

"""
INPUTS: arr - A list of PDF file names.

PROCESS:
The function first constructs the file path by joining the directory "../Cucina/PDFs" and the filename "PdfInformation.json" using os.path.join().
It then converts the 'arr' list to a JSON-formatted string with indentation using the json.dumps() method.
Finally, it opens the file at the constructed path in write mode and writes the JSON string to the file.

OUTPUT: The function saves the JSON-formatted data to a file.
"""
def SavePDFData(arr):
    path = os.path.join("../Cucina","PdfInformation.json")
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
    path = os.path.join("../Cucina","PdfInformation.json")
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
    recipes = ReadPDFData()
    print(extract_ingredients_from_pdf(recipes[1]))
    #ingredients, steps, text = Read("Lasagne")
    #ingredients, text = Read2(recipes[2])
    #print(ingredients)
    #print(text)

'''
    print("***********STEPS***********")
    for i in steps: print(i)
    print("***********INGREDIENTS***********")
    for j in ingredients: print(j)
    print("***********TEXT***********")
    print(text)
'''

