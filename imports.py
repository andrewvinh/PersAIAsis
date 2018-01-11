#Factory libraries
import re
import sys
import os
import inspect
import openpyxl
import datetime
import json
import string
import copy

path = os.path.dirname(os.path.abspath(__file__))
#print "Path: ", path
#Changes to config path must be reflected in config.py
with open(path+'/data/localConfig.txt','r') as f:
    loaded = json.load(f)
    pdirs = loaded["dirs"].split()
    pmods = loaded["modules"].split()

#Adding personal directories to path
for pdir in pdirs:
    print "Setting pdir: ", pdir
    temp = str(path+"/"+pdir+"/")
    sys.path.insert(0,temp)
    #os.path.expanduser(temp)
#print "Dirs: ", sys.path

'''
It is important that we import the module at the highest level
Functions from imports shall be called as MODULE.FUNCTION()
This will avoid flooding the namespace
'''
#Personal libraries
functions = []
for lib in pmods:
    globals()[lib] = __import__(lib)
    com = inspect.getmembers(globals()[lib], predicate=inspect.isfunction)
    
    print "Mod: ", lib
    print globals()[lib]
    print "Com: ", com
    
    #Adding functions to config and setting functions values in globals
    for c in com:
        #print "Appending to functions: ", str(mod+"."+c[0])
        functions.append(str(lib+"."+c[0]))
        #fcalls.append({c[0]:mod.c[0]})
        #print c[0]
        globals()[c[0]] = c[0]
#diff = [x for x in loaded["functions"] if x not in functions] 
diff = set(loaded["functions"]).symmetric_difference(set(functions))
#print ("Editing functions: ", diff) if len(diff) > 0 else ""
loaded["functions"] = functions
pdata.writeConfig(loaded)

