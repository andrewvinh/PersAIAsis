from imports import *

def build():
    
    f = open('/Users/andrewvinh/Development/tools/config.txt','r')
    bod = json.load(f)
    pmods = bod["modules"].split()
    '''
    print "Args in config: ", sys.argv
    print "Bod: ", bod
    print "Modules: ", pmods
    '''
    functions = []
    fcalls = []
    for mod in pmods:
        #Finds the functions of each imported pclass
        com = inspect.getmembers(globals()[mod], predicate=inspect.isfunction)
        '''
        print "Mod: ", mod
        print globals()[mod]
        print "Com: ", com
        '''
        for c in com:
            #print "Appending to functions: ", str(mod+"."+c[0])
            functions.append(str(mod+"."+c[0]))
            #fcalls.append({c[0]:mod.c[0]})
            #print c[0]
            globals()[c[0]] = c[0]
    #print "Functions: ", str(functions)
    bod["functions"] = functions
    f.close()
    return bod
