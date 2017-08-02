from imports import *

def build():
    #print "Args in config: ", sys.argv
    f = open('tools/config.txt','r')
    pmods = f.read().split()
    #print "Modules: ", pmods
    functions = []
    for mod in pmods:
        #Finds the functions of each imported pclass
        com = inspect.getmembers(globals()[mod], predicate=inspect.isfunction)
        '''
        print "Item: ", item
        print globals()[item]
        print "Com: ", com
        '''
        for c in com:
            functions.append(c[0])
    #print "Functions: ", str(functions)
    mods = {'modules': pmods,
            'functions': functions}
    return mods
