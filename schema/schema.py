
def closedDict():
    #print "Closed Dict: [{},0]" 
    return [newDB(),0]

def newDB():
    return {"Misc":[]}

def newCal(**kwargs):
    return {
            "Name":"",
            "Start":"",
            "Notes":[]
            }

def newContact():
    return {
            "Name":"",
            "Email":"",
            "Mobile":"",
            "Relation": []
            }

def newLog(user, args, ts):
    return {
            "User":user,
            "Input":args,
            "Timestamp":ts
            }

def blankDict():
    return {}
