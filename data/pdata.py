from imports import *
import psms
import panalyze
import schema

#Changes to config path must be reflected in imports.py
#altPath = os.getcwd()
localFiles = {
        "config":["/localConfig.txt",schema.blankDict()],
        "contacts":["/contacts.txt",schema.blankDict()],
        "calendar":["/calendar.txt",schema.blankDict()],
        "db":["/db.txt",schema.newDB()],
        "log":["/dlog.txt",schema.blankDict()]
        }

def getLocal(word):
    branch = str(word).lower()
    if branch in localFiles.keys():
        cur = str(os.path.dirname(os.path.abspath(__file__))+localFiles[branch][0])
        #print cur
        if os.path.isfile(cur):
            with open(cur,'r') as f:
                    db = json.load(f)
                    return db
        else:
            print "Unable to find local file. Making new one"
            match = localFiles[branch][1]
            #print "Branch: ", words, " Match: ", match
            updateLocal(word,match)
            return match
    else:
        fail = "Branch not found. Note: Keys are case-sensitive"
        print fail
        return fail


def getMatch(word):
    branch = str(word).lower()
    if branch in localFiles.keys():
        return localFiles[branch][1]
    else:
        print "Branch not found. Note: Keys are case-sensitive"

def updateLocal(branch, new):
    if branch != "Config" and branch != "Log": 
        print "Updating local", branch
    branch = str(branch).lower()
    if branch in localFiles.keys():
        with open(str(os.path.dirname(os.path.abspath(__file__))+localFiles[branch][0]),'w') as f:
            f.write(json.dumps(new, sort_keys=False, indent=2))

def resetDB(*args):
    print "Resetting local DB!"
    updateLocal("DB",schema.newDB())

def checkDict(branch):
    print "Looking up", branch
    branch = branch[0] if isinstance(branch,list) else branch
    cur = getLocal(branch)
    if isinstance(cur,(dict)):
        if len(cur) > 0:
            print branch,":"
            for key in sorted(cur):
                print key
                if isinstance(cur[key],list):
                    for item in cur[key]:
                        print item
                else:
                    print cur[key]
        else:
            print "Empty dict"
    else:
        print "Local",branch,"not found. Note: Keys are case-sensitive"
    return cur

#branch = local branch name, entry = {newKey:newVal}
def dictAdd(branch, entry):
    local = getLocal(branch)
    newKey = entry.keys()[0]
    newVal = entry[newKey]
    if len(local.keys()) > 0:
        if newKey not in local.keys():
            local[newKey] = newVal
        else:
            if isinstance(local[newKey],list):
                local[newKey] = local[newKey] + entry[newKey]
            print newKey, "already found in", branch
    else:
        print "Creating new", branch
        local[newKey] = newVal
    updateLocal(branch,local)
    return local

def dictRem(branch, key):
    local = getLocal(branch)
    if key in local.keys():
        print "Deleting", key, "from",branch
        local.pop(key)
        updateLocal(branch,local)
    else:
        print "Key not found"

def getKey(local, search):
    local = getLocal(local)
    search = panalyze.cleanString(search) 
    final = []
    print "Searching for: ", search
    for key in local.keys():
        cur = local[key]
        if isinstance(cur, dict):
            for k1 in cur.keys():
                c1 = cur[k1]
                if search in c1 or search in k1 or search in key:
                    final.append(key)
                    break
        else:
            if search in cur or search in key:
                final.append(key)
                break
    return sorted(final)

#paia addCat Contacts Address
def addCat(words):
    if len(words) > 1:
        db = getLocal(words[0])
        cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
        print "Adding", cat,"to", words[0]
        if cat not in db["0"].keys():
            print "Did you wanna make this a list?"
            choice = raw_input()
            choice = [] if choice.lower() == "yes" else ""
            for key in db.keys():
                db[key][cat] = choice
            updateLocal(words[0], db)
            #print "New", words[0],":", db
        else: 
            print cat,"is already present in", words[0]
    else:
        print "Args: [branch,newCat]"

#paia removeCat Contacts Address
def removeCat(words):
    if len(words) > 0:
        db = getLocal(words[0])
        cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
        if cat in db["0"].keys():
            #print "Removing", cat,"from", db
            for item in db:
                db[item].pop(cat)
        else:
            print cat, "is not in", words[0]
        updateLocal("Contacts", db)

def redAdd(bod, add):
    bkeys = bod.keys()
    for akey in add.keys():
        #if akey == "Misc":
        if isinstance(add[akey], list):
            bod[akey] = bod[akey] + list(set(add[akey]) - set(bod[akey]))
        else:
            if akey in bkeys:
                bod[akey] = redAdd(bod[akey],add[akey])
            else:
                bod[akey] = add[akey]
    #print "Finished bod: ", bod
    return bod

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
                print "-----\nLists: " 
            for key in current.keys():
                if key != "Misc":
                    print key
            if len(current["Misc"]) > 0:
                print "-----\nMisc: " 
            for item in current["Misc"]:
                print item
            print "-----" 
        except KeyError:
            print "Key not found! (Note: Keys are case-sensitive)"
    else:
        print "Current DB keys: ",current.keys()
    if len(current.keys()) > 1:
        select = ""
        print "Would you like to lookup further?"
        select = raw_input()
        if select.lower() != "no" and select.lower() != "exit":
            for k1 in current.keys():
                if select.lower() in k1.lower():
                    lookup(paths + [k1])
