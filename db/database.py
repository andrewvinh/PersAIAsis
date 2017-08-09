from imports import *

localDB = "db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=4))
    print "New DB: ", newDB

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
    count = 0
    if header in db.keys():
        while count < len(values)-1:
            print "Count: ", count
            value = values[count]
            vLen = len(value)
            print "Addition value: ", value
            #Single dict addition
            last = value[vLen-1]
            print "Last Value: ", last
            if last == ":":
                if value[vLen-2] == ":":
                    print "Found dict with multiple entries"
                    
                else:
                    print "Found single dict"
                    if count+1 != vLen:
                        temp = {value:values[count+1]}
                        print "Single dict value: ", temp
                        db[header].append(temp)
                        count = count + 1
            #Single entry addition
            elif value[vLen-1] != ":":
                print "Found single entry"
                db[header].append(value)
            count = count + 1
        writeDB(db)
    else:
        print "Header was not found in DB! No changes made =["
    return db

def deleteEntry(entryList):
    header = entryList[0]
    value = entryList[1]
    print "Attempting to delete \"", value, "\" from ", header
    db = loadDB()
    if header in db.keys():
        print "Found key!"
        if value[len(value)-1] != ":":
            print "Single variable"    
            if value in db[header]:
                db[header].remove(value)
            else:
                print "Entry not found. Deletion finished! :D"
        #Value is a dict, record differently
        else:
            value = value[0:len(value)-1]
            print "Value is a dict. Delete Value: ", value
            for entry in db[header]:
                print "db[header] :", entry
                if value in entry.keys():
                    #entry.pop(value)
                    db[header][:] = [d for d in db[header] if value not in d.keys()]
                else:
                    print "Entry not found. Deletion finished! :D"
    else:
        print "Key not found for deletion. Looks good to me :P"
    writeDB(db)
    loadDB()
    return db

def getEntry(entries):
    print "Getting entry from: ", entries
    final = []
    count = 0
    while count < len(entries):
        current = entries[count]
        last = current[len(current)-1]
        second = current[len(current)-2]
        if last != ":":
            final.append(current)
        elif last == ":" and second != ":":
            print "Found single dict!"
            if count+1 != len(values):
                final.append({current:values[count+1]})
                count = count + 1
            else:
                print "Reached end of list with incomplete dict.. What do I do =["
        count = count + 1
    return final
