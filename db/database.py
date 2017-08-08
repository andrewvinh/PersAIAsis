from imports import *

localDB = "db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=4))

def loadDB():
    db = {}
    if os.path.isfile(localDB):
        with open(localDB,'r') as f:
            db = json.load(f)
    else:
        writeDB({})
    #print "DB bod: ", db
    return db

def addHeader(header):
    print "Adding ", header, " to local DB!"
    db = loadDB()
    if header not in db.keys():
        db[header] = []
    else:
        print header, "already exists!" 
    writeDB(db)
    return db

def deleteHeader(header):
    print "Deleting ", header, " from local DB!"
    db = loadDB()
    print "Before deletion: ", db
    if header in db.keys():
        db.pop(header)
        print "Successfully removed from local DB:", db
    writeDB(db) if len(db) > 0 else writeDB({})
    print "Loaded after deletion: ", loadDB()
    return db

def addEntry(header, value):
    print "Attempting to add \"", value, "\" to ", header
    db = loadDB()
    if header in db.keys():
        db[header].append(value)
    writeDB(db)
    print "Load addition: ", loadDB()
    return db

def deleteEntry(header, value):
    print "Attempting to delete \"", value, "\" from ", header
    db = loadDB()
    if header in db.keys():
        if value[len(value)-1] != ":" and value in db[header]:
                db[header].remove(value)
        else:
            value = value[0:len(value)-1]
            print value
            for entry in db[header]:
                print "db[header] :", entry
                if value in entry.keys():
                    #entry.pop(value)
                    print "Value: ", value
                    db[header][:] = [d for d in db[header] if value not in d.keys()]
    writeDB(db)
    print "Load deletion: ", loadDB()
    return db


