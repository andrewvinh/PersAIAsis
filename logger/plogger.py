from imports import *

localLog = "/Users/andrewvinh/Development/logger/log.txt"

def writeLog(newLog):
    with open(localLog,'w') as f:
        f.write(json.dumps(newLog, sort_keys=False, indent=2))
    #print "New Log: ", newLog

def loadLog():    
    log = []
    if os.path.isfile(localLog):
        with open(localLog,'r') as f:
            log = json.load(f)
    else:
        writeLog(log)
    #print "Loaded DB: ", db
    return log

def addLog(entry):
    print "Log Entry: ", entry[0]
    print "Json load: ", json.load(entry[0])
    if os.path.isfile(localLog):
        with open(localLog,'r') as f:
            log = f.read()
            print "Local log: ", log, "\nLength: ", len(log)
            log = entry if len(log) == 0 else log.append(entry)
    writeLog(log)
            
