#!/usr/local/bin python
from imports import *

#OLD!!!
args = {'files': [],
        'commands': []}

#Current
bod = config.build()

def run():
    if(len(sys.argv) > 0):
        '''
        print "Input args: ", sys.argv
        print "Main bod: ", bod
        '''
        orgArgs = pread.readArgs(sys.argv, bod)
        db = database.loadDB()
        newRead()
    else:
        print "No commands found. What would you like?"

def newRead():
    #print "newRead: ", bod["inputArgs"]
    for key,val in bod["inputArgs"].items():
        #print key
        #print val
        myClass = __import__(key.split(".")[0])
        myFunc = key.split(".")[1]
        #print "myClass: ", myClass, "\nmyFunc: ", myFunc
        method = None
        try:
            method = getattr(myClass, myFunc)
            method(val)
            #break;time this
        except AttributeError:
            print ("Unable to call selected function with inputArgs:")
        

def oldRead():
        for item in sys.argv[1:]:
            '''
            print item
            print "Found file" if re.search(r"\b\w+\.\w+\b", item) else "Nope"
            '''
            if all([re.search(r"\b\w+\.\w+\b", item)]):   
                if 'files' not in args:
                    args['files'] = [item]
                else:
                    args['files'] = args['files'] + [item]
            #Regex checker needs to check length of longest known command and use that to determine if an input was command. #Security
            else: #Needs to cross-reference command-list before adding to commands
                if 'commands' not in args:
                    args['commands'] = [item]
                else:
                    args['commands'] = args['commands'] + [item]
        
        files = args['files']
        '''
        print "Args: ", args
        print "Files: ", files
        '''
        if len(args['commands']) > 0:
            if len(files) == 0:
                #checks through in chronorder
                for command in args['commands']:
                    if command == 'reverse':
                        ptext.reverse(args['files'][0])
                    elif command == 'flip':
                        ptext.flip(args['files'][0])
                    elif command == 'find':    
                        ptext.find(args['files'][0])
                    elif command == 'add':
                        pmath.add(bod['commands']['add'])
                    elif command == 'printRows':
                        pexcel.printRows(files[0])
                    elif command == 'combineCols':
                        pexcel.combineCols(files[0])
                    elif command == 'multiply':
                        pmath.multiply(bod['commands']['multiply'])

            else:
                print "Which files would you like to modify?"
                for c in range(len(files)):
                    print "%d) %s" % (c+1,files[c])
                print "Select files: "
                selection = raw_input().split(" ")
                print "Selected: ", selection
                if 'add' in args['commands']:
                    pmath.add(bod['commands']['add'])
                if 'multiply' in args['commands']:
                    pmath.multiply(bod['commands']['multiply'])
                for item in selection:
                    if 'reverse' in args['commands']:
                        ptext.reverse(files[int(item)-1])
                    elif 'flip' in args['commands']:
                        ptext.flip(files[int(item)-1])
                    elif 'find' in args['commands']:
                        ptext.find(files[int(item)-1])
                    elif 'printRows' in args['commands']:
                        pexcel.printRows(item)
                    elif 'combineCols' in args['commands']:
                        pexcel.combineCols(item)

        else: 
            print "What would you like?"

if __name__ == '__main__':
    run()
