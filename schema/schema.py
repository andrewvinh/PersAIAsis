import pdata

def closedDict():
    #print "Closed Dict: [{},0]" 
    return [newDB(),0]

def newConfig():
    return {}

def newDB():
    return {"Misc":[]}

def newCal():
    return {
            "Name":"",
            "Date":"",
            "Duration":"",
            "Notes":[]
            }

def newContact():
    return {
            "Name":"",
            "Email":"",
            "Mobile":"",
            "Relation": []
            }


