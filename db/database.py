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
    #print "Loaded DB: ", db
    return db

def addHeader(headers):
    print "Adding ", headers, " to local DB!"
    db = loadDB()
    for header in headers:
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
    #print "Attempting to add \"", values, "\" to ", header
    db = loadDB()
    count = 0
    if header in db.keys():
        '''
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
        '''
        orgArgs = getEntry(entryList)
        print "Getting entries: ", orgArgs
        print "Header: ", db[header]
        for item in orgArgs:
            print item
            db[header].append(item)
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
    '''
    Strange fucking situation with this entries list: I have to skip the first entry everytime. 
    Maybe fix later? 
    Or don't fix what ain't broke? 
    Hmm...
    '''
    #print "Entries before cutting: ", entries
    entries = entries[1::]
    #print "After cutting: ", entries
    final = []
    count = 0
    while count < len(entries):
        #print "Count: ", count
        current = entries[count]
        #print "Current: ", current
        last = current[len(current)-1]
        second = current[len(current)-2]
        if current == "/":
            final.append([])
        #Single entry
        elif last != ":":
            #print "Found single entry: ", current
            final.append(current.replace(":",''))
        #Dict with single entry
        elif last == ":" and second != ":" and count+1 != len(entries):
            #print "Found single dict!"
            final.append({current.replace(":",''):entries[count+1]})
            count = count + 1
        #Dict with multiple entries
        elif last == ":" and second == ":" and count+1 != len(entries):
            #print "Found multiple dict:", current
            head = current
            breaker = [i for i,x in enumerate(entries[count::]) if x == "/"][-1] if "/" in entries[count::] else len(entries)
            #print "Breaker: ", breaker, "\nStarting new getEntry for: ", entries[count:breaker+count]
            temp = getEntry(entries[count:breaker+count])
            #print "Equation breakup: ", temp
            final.append({current:temp})
            count = count + breaker
        elif count+1 == len(entries):
            print "End of args. I'm going to create a dict with an empty list."
            final.append({current.replace(":",''):[]})
        count = count + 1
    '''
    print "Would you like to see the long or short version?"
    lors = raw_input().strip()
    print "Okay, let's see... Here we go!"
    if lors == "Short" or lors == "short":
        print "Final: ", final
    elif lors == "Long" or lors == "long":
        print "~~~~~"
        for item in final:
            print item
        print "~~~~~"
    else:
        print "Wait hmm.. I didn't quite get that.. try again?"
    print "Length: ", len(final)
    '''
    return final

def readAhead(entries):
    print "Reading for continuous dict"

