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
import importlib
import datetime
import time
from datetime import timedelta


path = os.path.dirname(os.path.abspath(__file__))
#print "Path: ", path
#Changes to config path must be reflected in config.py
with open(path+'/data/localConfig.txt','r') as f:
    loaded = json.load(f)
    pdirs = loaded["dirs"].split()
    pmods = loaded["modules"].split()

#Adding personal directories to path
for pdir in pdirs:
    #print "Setting pdir: ", pdir
    temp = str(path+"/"+pdir+"/")
    sys.path.insert(0,temp)
    #os.path.expanduser(temp)
#print "Dirs: ", sys.path

#Personal libraries
import ptext
import pmath
import pexcel
import pconfig
import plogger
import panalyze
import pdata
import test
import schema
import psms
import calendar
import ptime

'''
It is important that we import the module at the highest level
Functions from imports shall be called as MODULE.FUNCTION()
This will avoid flooding the namespace
'''

functions = []
for lib in pmods:
    globals()[lib] = __import__(lib)
    com = inspect.getmembers(globals()[lib], predicate=inspect.isfunction)
    """
    globals().update(importlib.import_module(lib).__dict__)

    module = importlib.import_module(lib)

    globals().update(
        {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
        else 
        {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
    })
    com = inspect.getmembers(lib, predicate=inspect.isfunction)
    
    print "Mod: ", lib
    print "Com: ", com
    """
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
pdata.updateLocal("Config",loaded)

