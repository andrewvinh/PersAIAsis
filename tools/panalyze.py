from imports import *

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
            count = closeDict(entries, count)
        elif cur[-1] == ":":
            if count < len(entries):
                print "Single dict: ", cur, " Next: ", entries[count+1]
            else:
                print "Empty dict: ", cur
        count = count + 1
    return entries

def closeDict(entries, count):
    ops = 1
    cont = count + 1
    while cont < len(entries):
        print "Cont: ", cont
        cur2 = entries[cont]
        if cur2.count("::"):
            print "Found nested multidict"
            ops = ops + 1
        else:
            for x in range(cur2.count("/")):
                print "Found closer: ", cur2
                ops = ops - 1
            if ops <= 0:
                print "Closed the dict: ", cont, " Count: ", count, " Cont: ", cont
                count = cont
                cont = cont + 1
                break
        cont = cont + 1
        if cont == len(entries):
            print "Reached end of args. Cur: ", count, " Ops: ", ops, " Cont: ", cont 
    return count
