from imports import *

localDB = "/Users/andrewvinh/Development/db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=2))
    #print "New DB: ", newDB

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
    print "addEntry entryList: ", entryList
    header = entryList[0]
    values = entryList[1::]
    #print "Attempting to add \"", values, "\" to ", header
    db = loadDB()
    count = 0
    if header in db.keys():
        orgArgs = getEntry(entryList)
        print "orgArgs: ", orgArgs
        #print "Header: ", db[header]
        redResult = redAdd(db[header], orgArgs)
        print "redResult: ", redResult
        db[header] = redResult
        writeDB(db)
        '''
        for key in orgArgs.keys():
            item = orgArgs[key]    
            
            print "getEntry Item: ", item 
            print "Item.keys: ", item.keys()
            print "Header: ", header
            print "db[header]: ", db[header]
            
            if item != "" and len(item) != 0:
                #print "Found matching dict: ", header if any(header in d for d in entryList) else "Not a dict!"
                db[header] = {key:item}
            writeDB(db)
        '''
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
    final = {}
    count = 0
    #print "After cutting: ", entries
    while count < len(entries):
        #print "Count: ", count
        current = entries[count]
        #print "Current: ", current
        last = current[len(current)-1]
        second = current[len(current)-2]
        if current == "/":
            break
        #Single entry
        if last != ":":
            #print "Found single entry: ", current
            final["misc"] = final["misc"] + current.replace(":",'')
        #Dict with single entry
        elif last == ":" and second != ":" and count+1 != len(entries):
            #print "Found single dict!"
            final[current.replace(":",'')] = entries[count+1]
            count = count + 1
        #Dict with multiple entries
        elif last == ":" and second == ":" and count+1 != len(entries):
            '''
            Have to perform getEntry on each subsection of the breakpoints
            '''
            
            head = current
            openers = [i for i,x in enumerate(entries[count::]) if x.endswith("::")] 
            breakers = [i for i,x in enumerate(entries[count::]) if x == "/"] if "/" in entries[count::] else [len(entries)]
            if len(breakers) < len(openers):
                breakers.append(len(entries))
            '''
            print "---\nFound multiple dict:", current
            print "Openers: ", openers
            print "Breakers: ", breakers, ", count: ", count
            print "Starting new getEntry for: ", entries[count:breakers[-1]+count]
            '''
            '''
            Compare openers/breakers to get correct combination sets
            '''
            breaks = dictNesting(openers, breakers)
            head = 0
            segments = []
            for breakPoint in breaks:
                current = entries[head]
                temp = getEntry(entries[head:breakPoint])
                head = breakPoint
                '''
                print "getEntry: ", temp
                print "Current: ", current
                print "Final: ", final,"\n---"
                '''
                '''
                if len(final) > 0:
                    for item in final:
                        if current in item.keys():
                            print "final[0]: ", item
                            print "final[0][current]: ", item[current]
                            if temp[0] != item[current]:
                                item[current].append(temp[0])
                            success = 1
                '''
                if len(final) > 0:
                    for key in temp.keys():
                        #print "Key: ", key
                        final[current] = temp
                else:
                    print current, " is empty."
                    final[current] = temp
            count = count + breakers[-1]
        elif count+1 == len(entries):
            print "End of args. I'm going to create a dict with an empty list."
            final[current.replace(":",'')] = {}
        count = count + 1
    #print "Returning final: ", final
    return final

def dictNesting(openers, breakers):
    
    oc = 0
    bc = 0
    nested = 0
    breaks = []
    '''
    print "Openers: ", openers, "\nBreakers: ", breakers
    print openers[oc]
    print breakers[bc]
    '''
    while oc < len(openers) and bc < len(breakers):
        if openers[oc] > breakers[bc]:
            '''
            print "Found break! Breaker: ", breakers[bc], " Opener: ", openers[oc]
            print "Initial nested: ", nested
            '''
            nested = nested - 1
            if nested == 0:
                breaks.append(openers[oc])
            else: 
                bc = bc + 1
        else:
            #print "Nested opener."
            nested = nested + 1
            oc = oc + 1
    if bc < len(breakers):
        #print "Reached end of openers. "
        breaks.append(breakers[-1])
    #print "Breaks: ", breaks
    return breaks

def redAdd(branches, entries):
    print "redAdd Branch: ", branches
    print "redAdd Entries: ", entries
    bkeys = branches.keys()
    ekeys = entries.keys()
    if len(bkeys) == 0:
        print "Branch is empty and we can add straight into db"
        for key in ekeys:
            branches[key] = entries[key]
    else:
        for key in ekeys:
            if key in bkeys:
                redAdd(branches[key], entries[key])
            else:
                branches[key] = entries[key]
    print "Returning branch: ", branches
    return branches
