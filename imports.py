#Factory libraries
import re
import sys
import inspect
import openpyxl
import datetime
import json
sys.path.insert(0,'/Users/andrewvinh/Development/tools/')


'''
It is important that we import the module at the highest level
Functions from imports shall be called as MODULE.FUNCTION()
This will avoid flooding the namespace
'''
f = open('tools/config.txt','r')
pmods = json.load(f)["modules"].split()
f.close()

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
