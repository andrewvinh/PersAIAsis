from imports import *

localDB = "db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=4))

def loadDB(*args):
    db = {}
    if os.path.isfile(localDB):
        with open(localDB,'r') as f:
            db = json.load(f)
    else:
        writeDB({})
    print "Loaded DB: ", db
    return db

def addHeader(header):
    print "Adding ", header, " to local DB!"
    db = loadDB()
    if header not in db.keys():
        db[header] = []
    else:
        print header, "already exists!" 
    writeDB(db)
    loadDB()
    return db

def deleteHeader(header):
    print "Deleting ", header, " from local DB!"
    db = loadDB()
    print "Before deletion: ", db
    if header in db.keys():
        db.pop(header)
        print "Successfully removed from local DB:", db
    writeDB(db) if len(db) > 0 else writeDB({})
    loadDB()
    return db

def addEntry(entryList):
    header = entryList[0]
    values = entryList[1::]
    print "Attempting to add \"", values, "\" to ", header
    db = loadDB()
    if header in db.keys():
        for value in values:
            db[header].append(value)
            writeDB(db)
            print "Load addition: ", db
    else:
        print "Header was not found in DB! No changes made"
    return db

def deleteEntry(entryList):
    header = entryList[0]
    value = entryList[1]
    print "Attempting to delete \"", value, "\" from ", header
    db = loadDB()
    if header in db.keys():
        print "Found key!"
        if value[len(value)-1] != ":" and value in db[header]:
            print "Single variable"    
            db[header].remove(value)
        #Value is a dict, record differently
        else:
            value = value[0:len(value)-1]
            print "Delete Value: ", value
            for entry in db[header]:
                print "db[header] :", entry
                if value in entry.keys():
                    #entry.pop(value)
                    print "Value: ", value
                    db[header][:] = [d for d in db[header] if value not in d.keys()]
    else:
        print "Key not found for deletion. Looks good to me :P"
    writeDB(db)
    loadDB()
    return db


