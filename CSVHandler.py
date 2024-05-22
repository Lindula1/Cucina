import csv

'''
with open("UserPantryData.txt", 'a') as pantry:
    reader = csv.reader(pantry, delimiter=',')
    lCount = 0
    for row in reader:
        if lCount == 0:
            print(f"Column names {", ".join(row)}")
            lCount += 1
        else:
            print(row)
            lCount += 1
    print(f"Lines Processed {lCount}")
    '''

def Reader():
    with open('UserPantryData.csv', mode='r') as pantry:
        reader = csv.DictReader(pantry)
        lCount = 0
        for row in reader:
            if lCount == 0:
                print(f'Column names are {", ".join(row)}')
                lCount += 1
            print(f'\t{row["Letter sort value"]}, {row["Nutritional value"]}, {row["Quantity"]}, {row["Expiry date"]}, {row["Ingredient name"]}')
            lCount += 1
        print(f'Processed {lCount} lines.')
    return reader

def Write(array):
    with open('UserPantryData.csv', mode='a') as pantry:
        writer = csv.writer(pantry, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(["Letter sort value", "Nutritional value", "Quantity", "Expiry date", "Ingredient name"])
        for i in range(len(array)):
            writer.writerow([array[i][0], array[i][1], array[i][2], array[i][3], array[i][4]])