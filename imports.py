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

#Changes to config path must be reflected in config.py
with open('/Users/andrewvinh/Development/tools/localConfig.txt','r') as f:
    loaded = json.load(f)
    pdirs = loaded["dirs"].split()
    pmods = loaded["modules"].split()

#Adding personal directories to path
for pdir in pdirs:
    temp = str("/Users/andrewvinh/"+pdir+"/")
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
    '''
    print "Mod: ", mod
    print globals()[mod]
    print "Com: ", com
    '''
    for c in com:
        #print "Appending to functions: ", str(mod+"."+c[0])
        functions.append(str(lib+"."+c[0]))
        #fcalls.append({c[0]:mod.c[0]})
        #print c[0]
        globals()[c[0]] = c[0]
loaded["functions"] = functions
pconfig.writeConfig(loaded)

#Build Config
#import pconfig
bod = pconfig.getConfig()
