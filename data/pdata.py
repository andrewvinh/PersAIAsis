from imports import *
import psms
import panalyze

#Changes to config path must be reflected in imports.py
#altPath = os.getcwd()
path = os.path.dirname(os.path.abspath(__file__))
localConfig = path + '/localConfig.txt'
localContacts = path + "/contacts.txt"
localDB = path + "/db.txt"

def newDB():
    return {"Misc":[]}

localFiles = {
        "localConfig":[str(path + '/localConfig.txt'),{}],
        "localContacts":[str(path + "/contacts.txt"),{}],
        "localDB":[str(path + "/db.txt"),newDB()]
        }

def getLocal(words):
    branch = str("local" + words)
    if branch in localFiles.keys():
        cur = localFiles[branch][0]
        if os.path.isfile(cur):
            with open(cur,'r') as f:
                    db = json.load(f)
                    return db
        else:
            print "Unable to find local file. Making new one"
            match = localFiles[branch][1]
            #print "Branch: ", words, " Match: ", match
            updateLocal(words,match)
    else:
        print "Local branch not found"

def updateLocal(branch, new):
    #print "Updating local", branch
    branch = str("local" + branch)
    if branch in localFiles.keys():
        with open(localFiles[branch][0],'w') as f:
            f.write(json.dumps(new, sort_keys=False, indent=2))

def resetDB(*args):
    updateDB(newDB())

def getConfig(name):
    bod = getLocal("Config")
    return bod[name] if name in bod.keys() else bod

def listContacts(*args):
    conts = getLocal("Contacts")
    if len(conts) == 0:
        print "No contacts... loser."
    else:
        search = args[0][0].lower() if args[0] else ""
        if search:
            ids = psms.getID(search)
            for item in sorted(ids):
                print "User ID: ", item
                print "Name: ", conts[item]["Name"]
                print "Mobile: ", conts[item]["Mobile"]
                print "Email: ", conts[item]["Email"]
                print "Relation: ", conts[item]["Relation"]
        else:
            count = 1
            while count < len(conts.keys())-1: #-1 because of Contact -1: Twilio Bot
                print "ID: ", count
                print "Name: ", conts[str(count)]["Name"]
                print "Mobile: ", conts[str(count)]["Mobile"]
                print "Email: ", conts[str(count)]["Email"]
                print "Relation: ", conts[str(count)]["Relation"]
                count = count + 1

"""
Args:
1) ptext.find
2) ["string"]
"""
def callPFunc(handler, thruArgs):
    method = None
    try:
        pclass = __import__(handler.split(".")[0])
        pfunc = handler.split(".")[1]
        method = getattr(pclass, pfunc)
        return method(thruArgs)
        #break;time this
    except AttributeError:
        print "Unable to call ", handler

def lookup(full):
    #print "Full: ", full
    #paths = string.replace(full[0], ".", " ").replace(full[0],"/"," ").split(" ") if len(full) == 1 else full
    if len(full) == 1:
        paths = full[0]
        for ch in ["/","."]:
            if ch in paths:
                paths = paths.replace(ch," ") 
        paths = paths.split(" ")
    else:
        paths = full
    #print "Paths: ", paths
    current = getLocal("DB")
    if len(paths) > 0:    
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
            if len(current.keys()) > 0:
                select = ""
                print "Would you like to lookup further?"
                select = raw_input()
                if "no" not in select.lower():
                    lookup(paths + [select])
        except KeyError:
            print "Key not found! (Note: Keys are case-sensitive)"
    else:
        print "Current DB keys: ",current.keys()

def addCat(words):
    if len(words) > 0:
        db = getLocal(words[0])
        cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
        #print "Adding", cat,"to", db
        print "Did you wanna make this a list?"
        choice = raw_input()
        choice = [] if choice.lower() == "yes" else ""
        for item in db:
            db[item][cat] = choice
        updateLocal("Contacts", db)

def removeCat(words):
    if len(words) > 0:
        db = getLocal(words[0])
        cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
        #print "Adding", cat,"to", db
        if cat in db["0"].keys():
            for item in db:
                db[item].pop(cat)
        else:
            print cat, "is not in", words[0]
        updateLocal("Contacts", db)

