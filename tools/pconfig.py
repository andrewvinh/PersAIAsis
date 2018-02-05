from imports import *
import pdata

def getConfig(name):
    bod = pdata.getLocal("Config")
    return bod[name] if name in bod.keys() else bod

def checkConfig(self,**kwargs):
    #Implement multi-level searching
    if "data" in kwargs:
        print kwargs["key"], ": ", kwargs["data"]
    else:
        bod = pdata.getLocal("Config")
        #print "Bod: ", bod
        print "Config: ", bod.keys()
        select = ""
        print "Would you like to lookup further?"
        select = raw_input()
        if select.lower() != "no":
            try:
                temp = bod[select]
                kwargs = {"data":temp, "key":select}
                checkConfig(self,**kwargs)
            except KeyError as e:
                print "Key not found =["
