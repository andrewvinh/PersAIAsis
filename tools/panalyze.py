from imports import *
import pdata, schema

#print "Analyzing config: ", bod

def sAnalyze(entries):
    print "Analyzing: ", entries

"""
Check items individually
Cycle through dividers to check. pfunc the func
If string, recv string, then check if dict
If multi, recv both finalized dict and next starting position
"""
def addEntry(entries):
    print "Making new dict with: ", entries
    count = 0
    final = []
    divs = pdata.getConfig("dividers")
    while count < len(entries):
        cur = entries[count]
        print cur
        if "::" in cur:
            #Uses the closing position to determine full multi dict in entries
            closed = closeDict(entries, count)
            mdict = entries[count:closed]
            print "Closed dict: ", mdict
            pdata.redAdd(pdata.getLocalDB(),mdict)
            count = closed
        elif cur[-1] == ":":
            if count < len(entries):
                print "Single dict: ", cur, " Next: ", entries[count+1]
            else:
                print "Empty dict: ", cur
        count = count + 1
    return entries

#Returns the closing position of a new dict in entries
def closeDict(entries, count):
    print "Closing: ", entries[count]
    ops = 1
    cont = count + 1
    final = schema.closedDict()
    t1 = final[0]
    while cont < len(entries): 
        cur = entries[cont]
        #print "Cur: ", cur, " Cont: ", cont
        if cur.count("::"):
            #print "Found nested opener"
            ops = ops + 1
        else:
            for x in range(cur.count("/")):
                #print "Found closer: ", cur
                ops = ops - 1
            if ops <= 0:
                #print "Closed dict. Cont: ", cont, " Count: ", count
                count = cont
                cont = cont + 1
                break
        cont = cont + 1
        if cont == len(entries):
            print "Reached end of args. Cur: ", count, " Ops: ", ops, " Cont: ", cont 
            count = cont
    #print "Closing: ", count, " ", cont
    return count
