from imports import *
import pdata

def getConfig(*args):
    local = pdata.getLocalConfig() 
    #print "Received local config: ", local
    return local

def checkConfig(self,**kwargs):
    #Implement multi-level searching
    if "data" in kwargs:
        print kwargs["key"], ": ", kwargs["data"]
    else:
        bod = pdata.getLocalConfig()
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
