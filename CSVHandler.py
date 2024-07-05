import csv

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

def Write(array):
    with open('UserPantryData.csv', mode='w') as pantry:
        writer = csv.writer(pantry, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["Letter sort value", "Nutritional value", "Quantity", "Expiry date", "Ingredient name"])
        for i in range(len(array)):
            writer.writerow([array[i][0], array[i][1], array[i][2], array[i][3], array[i][4]])
        return "Write completed successfully"