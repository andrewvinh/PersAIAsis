from imports import *

def build():
    
    f = open('tools/config.txt','r')
    bod = json.load(f)
    pmods = bod["modules"].split()
    '''
    print "Args in config: ", sys.argv
    print "Bod: ", bod
    print "Modules: ", pmods
    '''
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
            functions.append(str(mod+"."+c[0]))
    #print "Functions: ", str(functions)
    bod["functions"] = functions
    f.close()
    return bod
