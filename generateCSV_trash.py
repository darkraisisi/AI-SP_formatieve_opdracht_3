from pymongo import MongoClient
import csv

envvals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER", "RECOMADDRESS"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

client = MongoClient()
database = client.huwebshop

products = database.products.find()
sessions = database.sessions.find()
profiles = database.profiles.find()

def multi_getattr(obj, attr, default = None):
    """
    http://code.activestate.com/recipes/577346-getattr-with-arbitrary-depth/
    Source
    Changed it a tiny bit
    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = obj.get(i)
        except AttributeError:
            try:
                obj = obj[int(i)]
            except:
                return default
    return obj

def generateCSV(fileNameString, category, fieldnames, values):
    print("Creating the database contents...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        c = 0

        for record in category:
            writeDict = {}
            for x in range(len(fieldnames)):
                    writeDict.update({fieldnames[x]: multi_getattr(record, values[x])})
                    x +=1
            writer.writerow(writeDict)
            c += 1
            if c % 10000 == 0:
                break
                print(f"{c} records written to {fileNameString}...")
    print(f"Finished creating {fileNameString}")

def generateAllCSV():
    generateCSV('csv/trash/products.csv', products,
                ['id', 'name', 'gender', 'category', 'subcategory', 'subsubcategory', 'brand'],
                ["_id", "name", "gender", "category", "sub_category", "sub_sub_category", "brand"])
    generateCSV('csv/trash/sessions.csv', sessions,
                ['id', 'segment','orders'],
                ['buid.0', 'segment','order.products'])
    generateCSV('csv/trash/profiles.csv', profiles,
                ['id','order_amount', 'browser_id'],
                ['xoxo', 'order.count',"buids"])
generateAllCSV()
#           BRONVERMELDING
#   Dit is de code die gebruikt is tijdens de les van 5 maart met Nick.