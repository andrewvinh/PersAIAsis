from imports import *

path = os.path.dirname(os.path.abspath(__file__))
tpath = os.getcwd()
localDB = path + "/db.txt"

def newDB():
    return {"Misc":[]}

def getLocalDB():
    db = {}
    if os.path.isfile(localDB):
        with open(localDB,'r') as f:
            db = json.load(f)
    else:
        updateDB({})
    #print "Loaded DB: ", db
    return db

def updateDB(newDB):
    with open(localDB,'w') as f:
        f.write(json.dumps(newDB, sort_keys=False, indent=2))
    #print "Newly written DB: ", newDB
