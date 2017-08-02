

def readArgs(argv, bod):
    '''
    print "Attemping to read: ", argv
    print "Reading Bod: ", bod
    '''
    bod['inputArgs'] = {}
    functions = bod['functions']
    current = "Random"
    for c in range(1,len(argv)):
        temp = argv[c]
        '''
        print "Temp: ", temp
        print functions
        print temp in functions
        '''
        if temp in functions and temp not in bod['inputArgs']:
            bod['inputArgs'][temp] = []
            current = temp
        elif temp != current:
            bod['inputArgs'][current].append(temp)
    return bod
