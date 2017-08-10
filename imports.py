#Factory libraries
import re
import sys
import os
import inspect
import openpyxl
import datetime
import json

f = open('/Users/andrewvinh/Development/tools/config.txt','r')
loaded = json.load(f)
pdirs = loaded["dirs"].split()
pmods = loaded["modules"].split()
f.close()

#Adding personal directories to path
for pdir in pdirs:
    sys.path.insert(0,str("/Users/andrewvinh/Development/"+pdir+"/"))

'''
It is important that we import the module at the highest level
Functions from imports shall be called as MODULE.FUNCTION()
This will avoid flooding the namespace
'''
#Personal libraries
for lib in pmods:
    globals()[lib] = __import__(lib)
    '''
    print "Importing: ", lib
    print globals()[lib]
    print "Functions: ", inspect.getmembers(globals()[lib], predicate=inspect.isfunction)
    print [method for method in dir(lib) if callable(getattr(lib, method))]
    print dir(lib)
    '''

#Build Config
import config
