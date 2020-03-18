from pymongo import MongoClient
import csv

envvals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER", "RECOMADDRESS"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

client = MongoClient()
database = client.huwebshop

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

def generateCSV(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0

        for record in mongoCollections:
            writeDict = {}
            for x in range(len(csvFieldNames)):
                    writeDict.update({csvFieldNames[x]: multi_getattr(record,mongoFieldNames[x])})
                    x +=1
            writer.writerow(writeDict)
            c += 1
            if c % 10000 == 0:
                break
                print(f"{c} records written to {fileNameString}...")

    print(f"Finished creating {fileNameString}")

def generateBrandsCSV(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        
        brandDict = {} #id,brandName
        for record in mongoCollections:
            c += 1
            try:
                brandDict.setdefault(record[mongoFieldNames[1]], len(brandDict)+1)
            except:
                brandDict.setdefault('None', len(brandDict)+1)
            if c % 10000 == 0:
                    print(f"{c} records sorted...")

        for item in brandDict:
            writer.writerow({csvFieldNames[0]:brandDict[item],csvFieldNames[1]:item})

    print(f"Finished creating {fileNameString}")
    return brandDict

def generateCSVProducts(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames,brandDict):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        for record in mongoCollections:
            c+=1
            writeDict = {}
            for x in range(len(csvFieldNames)):
                if csvFieldNames[x] != 'brand':
                    writeDict.update({ csvFieldNames[x]: multi_getattr(record,mongoFieldNames[x]) })
                else:
                    brandId = brandDict.get(multi_getattr(record,mongoFieldNames[x]))
                    writeDict.update({ csvFieldNames[x]: brandId })
            writer.writerow(writeDict)
            if c % 10000 == 0:
                    print(f"{c} records written...")

    print(f"Finished creating {fileNameString}")
    return brandDict

def generateAllCSV():
    sessions = database.sessions.find()
    profiles = database.profiles.find()

    products = database.products.find()
    brandDict = generateBrandsCSV('csv/new/brand.csv', products,
    ['id','name'],
    ['','brand'])

    products = database.products.find()
    generateCSVProducts('csv/new/products.csv', products,
    ['id','brand','name','targetaudience','category', 'sub_category','sub_sub_category','msrp','discount','sellingprice','deal'],
    ['_id','brand','name','gender','category', 'sub_category', 'sub_sub_category','price.mrsp','price.discount','price.selling_price','properties.discount'],brandDict)

    # generateCSV('csv/new/profiles.csv', profiles)

    # generateCSV('csv/new/sessions.csv', sessions)

    # generateCSV('csv/new/cart.csv', sessions)

#           BRONVERMELDING
#   Dit is de code die gebruikt is tijdens de les van 5 maart met Nick.