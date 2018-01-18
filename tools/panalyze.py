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
    final = {}
    divs = pdata.getConfig("dividers")
    while count < len(entries):
        cur = checkString(entries[count])
        print "AddEntry cur: ", cur 
        if "::" in cur:
            cur = cur.replace(":","")
            #Uses the closing position to determine full multi dict in entries
            closed = closeDict(entries, count)
            mdict = entries[count+1:closed]
            print "Closed dict: ", mdict, " Closed: ", closed
            ret = dictify(mdict)
            print "Return: ", ret
            final[cur] = ret
            count = closed
        elif cur[-1] == ":":
            cur = cur.replace(":","")
            if count < len(entries):
                print "Single dict: ", cur, " Next: ", entries[count+1]
            else:
                print "Empty dict: ", cur
        count = count + 1
    print "AddEntry Final: ", final
    return entries

#Returns the closing position of a new dict in entries
def closeDict(entries, count):
    #print "Closing: ", entries[count]
    ops = 1
    cont = count + 1
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
            print "Reached end of args."
            count = cont
    #print "Closing: ", count, " ", cont
    return count

#Receives dict in list and transforms to full dict
def dictify(add):
    print "Attemping to dictify: ", add
    final = pdata.newDB()
    count = 0
    while count < len(add):
        cur = checkString(add[count])
        print "Dictify cur: ", cur
        #print "CheckString return: ", cur
        add[count] = cur
        if "::" in cur:
            #temp = dictify(add[count:closeDict(add,count)])
            print "Temp: ", temp
        elif ":" in cur:
            cur = cur.replace(":","")
            print "Single dict: ", cur
            print "Single dict return: ", singleDict(add[count::])
            if count+1 < len(add):
                final[cur] = singleDict(add[count::])
                count = count + 1
            else:
                final[cur] = pdata.newDB()
        else:
            misc = final["Misc"]
            misc.append(cur)
            final["Misc"] = misc
        count = count + 1
    print "Final: ", final
    return final
        
def singleDict(entries):
    cur = entries[0]
    return {"Misc":entries[1]} if len(entries)>1 else pdata.newDB()

def checkString(cur):
    replace = ""
    if "string" in cur.lower():
        print "Found string! What would you like to replace it with?"
        replace = raw_input()
        replace = cur.lower().replace("string",replace)
    return replace if replace else cur

def cleanString(cur):
    cur = cur.replace(":","")
    return cur
