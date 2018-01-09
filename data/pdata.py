from imports import *

#Changes to config path must be reflected in imports.py
path = os.path.dirname(os.path.abspath(__file__))
localConfig = path + '/localConfig.txt'

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



def getLocalConfig():
    bod = {}
    with open(localConfig,'r') as f:
        bod = json.load(f)
    return bod

def writeConfig(bod):
    with open(localConfig, 'w') as f:
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