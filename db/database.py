from imports import *

localDB = "db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=4))
        print "Successful write!"

def loadDB():
    db = {}
    if os.path.isfile(localDB):
        with open(localDB,'r') as f:
            db = json.load(f)
    else:
        writeDB({})
    print "DB bod: ", db
    return db

def addHeader(header):
    print "Adding ", header, " to local DB!"
    db = loadDB()
    if header not in db.keys():
        db[header] = []
    writeDB(db)
    return db

def deleteHeader(header):
    print "Deleting ", header, " from local DB!"
    db = loadDB()
    print "Before deletion: ", db
    if header in db.keys():
        db.pop(header, 0)
        print "Successfully removed from local DB!"
    print "After deletion: ", db
    return db
