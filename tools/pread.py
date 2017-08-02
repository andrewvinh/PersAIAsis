

def readArgs(argv, bod):
    '''
    print "Attemping to read: ", argv
    print "Reading Bod: ", bod
    '''
    bod['commands'] = {}
    functions = bod['functions']
    current = "None"
    for c in range(1,len(argv)):
        temp = argv[c]
        '''
        print "Temp: ", temp
        print functions
        print temp in functions
        '''
        if temp in functions and temp not in bod['commands']:
            bod['commands'][temp] = []
            current = temp
        elif temp != current:
            bod['commands'][current].append(temp)
    print bod
