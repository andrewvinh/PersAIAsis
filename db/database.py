from imports import *

localDB = "/Users/andrewvinh/Development/db/db.txt"

def writeDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=2))
    #print "Newly written DB: ", newDB

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
            db[header] = {"Misc": []}
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
    #print "addEntry entryList: ", entryList
    header = entryList[0]
    values = entryList[1::]
    #print "Attempting to add \"", values, "\" to ", header
    db = loadDB()
    count = 0
    if header in db.keys():
        orgArgs = getEntry(entryList)
        #print "orgArgs: ", orgArgs
        #print "Header: ", db[header]
        redResult = redAdd(db[header], orgArgs)
        #print "redResult: ", redResult
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
    #print "Entries before cutting: ", entries
    entries = entries[1::]
    final = {"Misc": []}
    count = 0
    #print "After cutting: ", entries
    while count < len(entries):
        #print "Count: ", count
        current = entries[count]
        #print "Current: ", current
        last = current[len(current)-1]
        second = current[len(current)-2]
        current = string.replace(current, ":", '')
        if current == "/":
            break
        #Single entry
        if current == "String":
            print "What is the sentence you'd like to add?"
            statement = raw_input()
            final["Misc"].append(statement)
        elif last != ":":
            #print "Found single entry: ", current
            final["Misc"].append(current)
        #Dict with single entry
        elif last == ":" and second != ":" and count+1 != len(entries):
            #print "Found single dict!"
            if entries[count+1] != "String":
                final[current] = entries[count+1]
            else:
                print "What is the sentence you'd like to add?"
                statement = raw_input()
                final[current] = statement
            count = count + 1
        #Dict with multiple entries
        elif last == ":" and second == ":" and count+1 != len(entries):
            head = current
            openers = [i for i,x in enumerate(entries[count::]) if x.endswith("::")] 
            breakers = [i for i,x in enumerate(entries[count::]) if x == "/"] if "/" in entries[count::] else [len(entries)]
            if len(breakers) < len(openers):
                breakers.append(len(entries))
            breaks = dictNesting(openers, breakers)
            '''
            print "---\nFound multiple dict:", current
            print "Openers: ", openers
            print "Breakers: ", breakers, ", count: ", count
            print "Break points: ", breaks
            print "Starting new getEntry for: ", entries[count:breakers[-1]+count]
            '''
            head = 0
            segments = []
            for breakPoint in breaks:
                current = string.replace(entries[head], ':', '')
                temp = getEntry(entries[head:breakPoint])
                head = breakPoint
                '''
                print "getEntry: ", temp
                print "Current: ", current
                print "Final: ", final,"\n---"
                '''
                if len(final) > 0:
                    for key in temp.keys():
                        #print "Key: ", key
                        final[current] = temp
                else:
                    #print current, " is empty."
                    final[current] = temp
            count = count + breakers[-1]
        elif count+1 == len(entries):
            print "I'm going to create a dict with an empty list!"
            final[current] = {"Misc": []}
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
        #print "Nested: ", nested
        if openers[oc] > breakers[bc]:
            #print "Found break! Breaker: ", breakers[bc], " Opener: ", openers[oc]
            nested = nested - 1 if nested >= 1 else 0
            if nested == 0:
                #print "Nested = 0. Adding: ", openers[oc]
                breaks.append(openers[oc])
                oc = oc + 1
            else: 
                bc = bc + 1
        else:
            #print "Nested opener."
            nested = nested + 1
            oc = oc + 1
    if bc < len(breakers):
        #print "Reached end of openers. "
        breaks.append(breakers[-1])
    return breaks

def redAdd(branches, entries):
    ''' 
    print "redAdd Branch: ", branches
    print "redAdd Entries: ", entries
    '''
    bkeys = branches.keys()
    ekeys = entries.keys()
    if len(bkeys) == 0:
        #print "Branch is empty and we can add straight into db"
        for key in ekeys:
            key = string.replace(key, ':', '')
            branches[key] = entries[key]
    else:
        for key in ekeys:
            key = string.replace(key, ':', '')
            if key == "Misc":
                '''
                print "BMisc: ", branches["Misc"]
                print "EMisc: ", entries["Misc"]
                '''
                for item in entries[key]:
                    if item not in branches[key]:
                        branches[key] = branches[key] + entries[key]
                #branches[key] = entries[key] if key not in bkeys else branches[key] + entries[key]
            elif key in bkeys:
                redAdd(branches[key], entries[key])
            else:
                branches[key] = entries[key]
                if key in branches["Misc"]:
                    branches["Misc"].remove(key)
    #print "Returning branch: ", branches
    #print json.dumps(branches)
    return branches

def lookup(full):
    print "Full: ", full
    #paths = string.replace(full[0], ".", " ").replace(full[0],"/"," ").split(" ") if len(full) == 1 else full
    if len(full) == 1:
        paths = full[0]
        for ch in ["/","."]:
            if ch in paths:
                paths = paths.replace(ch," ") 
        paths = paths.split(" ")
    else:
        paths = full
    print "Paths: ", paths
    current = loadDB()
    try:
        for path in paths:
            current = current[path]
        print paths[-1], "data:"
        if len(current.keys()) > 1:
            print "-----\nObjects: " 
        for key in current.keys():
            if key != "Misc":
                print key
        if len(current["Misc"]) > 0:
            print "-----\nSingles: " 
        for item in current["Misc"]:
            print item
        print "-----"
        select = ""
        print "Would you like to lookup further?"
        select = raw_input()
        if select.lower() != "no":
            lookup(paths + [select])
    except KeyError:
        print "Key not found! (Note: Keys are case-sensitive)"
    
