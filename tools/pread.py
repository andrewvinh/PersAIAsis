

def readArgs(argv, bod):
    '''
    print "Attemping to read: ", argv
    print "Reading Bod: ", bod
    '''
    bod["inputArgs"] = {}
    modules = bod["modules"]
    functions = bod["functions"]
    current = "Random"
    for c in range(1,len(argv)):
        temp = argv[c]
        for function in functions:
            if temp == function.split(".")[1]:
                if temp not in bod['inputArgs']:
                    bod['inputArgs'][function] = []
                    current = function
                    break
            elif current in bod['inputArgs'].keys() and temp != current.split(".")[1]:
                bod['inputArgs'][current].append(temp)
                break
        #print current
    return bod
