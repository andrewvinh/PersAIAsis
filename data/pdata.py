from imports import *

#Changes to config path must be reflected in imports.py
path = os.path.dirname(os.path.abspath(__file__))
localConfig = path + '/localConfig.txt'

#altPath = os.getcwd()
localDB = path + "/db.txt"
localContacts = path + "/contacts.txt"

def newDB():
    return {"Misc":[]}

def getLocalDB():
    db = newDB()
    #print "DB: ",db
    if os.path.isfile(localDB):
        with open(localDB,'r') as f:
            try:
                db = json.load(f)
            except:
                updateDB(db)
    else:
        updateDB(db)
    #print "Loaded DB: ", db
    return db

def updateDB(newDB):
    print "Updating local DB!"
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=2))
    #print "Newly written DB: ", newDB

def resetDB(*args):
    updateDB(newDB())

def getLocalConfig():
    bod = {}
    with open(localConfig,'r') as f:
        try:
            bod = json.load(f)
        except:
            writeConfig(bod)
    return bod

def getConfig(name):
    bod = getLocalConfig()
    return bod[name] if name in bod.keys() else bod

def writeConfig(bod):
    with open(localConfig, 'w') as f:
        f.write(json.dumps(bod, sort_keys=False, indent=2))

def getLocalContacts(*args):
    bod = {}
    with open(localContacts,'r') as f:
        try:
            bod = json.load(f)
        except:
            updateContacts(bod)
    return bod

def updateContacts(bod):
    print "Updating local contacts!"
    with open(localContacts,'w') as f:
        f.write(json.dumps(bod, sort_keys=False, indent=2))

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
    current = getLocalDB()
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


