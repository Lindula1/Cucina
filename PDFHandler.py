import sys
from pypdf import PdfReader
sys.path.insert(0, "../Cucina/PDFs")

def Read(pdf):
    try:
        reader = PdfReader(f"{pdf}.pdf")
    except FileNotFoundError:
        print("Directory Error, local file location used")
        reader = PdfReader(f"C:/Users/budwi/OneDrive/Documents/GitHub/Cucina/PDFs/{pdf}.pdf")
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
            if "ingredients" in line.lower():
                print("Ingredients being added")
                ingLine = True
                stepLine = False
            elif "method" in line.lower() or "step" in line.lower():
                print("Steps being added")
                stepLine = True
                ingLine = False
            elif "utensils" in line.lower() or  "options"  in line.lower():
                print("Random stuff")
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

#ingredients, steps, text = Read("Mushroom_Risotto")

#for i in steps: print(i)
#print("\n")
#for j in ingredients: print(j)
#print("\n")
#print(text)
