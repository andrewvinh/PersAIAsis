from imports import *
import pdata, schema, pconfig

"""
Check items individually
Cycle through dividers to check. pfunc the func
If string, recv string, then check if dict
If multi, recv both finalized dict and next starting position
"""
def addEntry(entries):
    print "Making new dict with: ", entries
    count = 0
    final = schema.newDB()
    divs = pconfig.getConfig("dividers")
    while count < len(entries):
        cur = checkString(entries[count])
        #print "AddEntry cur: ", cur 
        if "::" in cur:
            cur = cleanString(cur)
            #Uses the closing position to determine full multi dict in entries
            closed = closeDict(entries, count)
            mdict = entries[count+1:closed]
            #print "Closed dict: ", mdict, " Closed: ", closed
            ret = dictify(mdict)
            #print "Return: ", ret
            final[cur] = ret
            count = closed
        elif cur[-1] == ":":
            cur = cleanString(cur)
            if count+1 < len(entries):
                #print "Single dict: ", cur, " Next: ", entries[count+1]
                final[cur] = {"Misc":[checkString(entries[count+1])]}
                count = count + 1
            else:
                print "Empty dict: ", cur
                final[cur] = pdata.newDB()
        else:
            misc = final["Misc"]
            misc.append(cur)
            final["Misc"] = misc
        count = count + 1
    final = pdata.redAdd(pdata.getLocal("DB"),final)
    #print "AddEntry Final: ", final
    pdata.updateLocal("DB",final)
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
            #print "Reached end of args."
            count = cont
    #print "Closing: ", count, " ", cont
    return count

#Receives dict in list and transforms to full dict
def dictify(add):
    #print "Attemping to dictify: ", add
    final = schema.newDB()
    count = 0
    while count < len(add):
        cur = checkString(add[count])
        add[count] = cur
        if "::" in cur:
            cur = cleanString(add[count])
            newClose = closeDict(add,count)
            newD = add[count+1:newClose]
            #print "Cur: ", cur, " NewD: ", newD, " NewC: ", newClose
            temp = dictify(newD)
            #print "Temp: ", temp
            count = newClose
            #print "New Count: ", count
            final[cur] = temp
        elif ":" in cur:
            cur = cleanString(add[count])
            #print "Single dict: ", cur
            if count+1 < len(add):
                final[cur] = {"Misc":[checkString(add[count+1])]}
                count = count + 1
            else:
                final[cur] = pdata.newDB()
        else:
            misc = final["Misc"]
            misc.append(cur)
            final["Misc"] = misc
        count = count + 1
    #print "Final: ", final
    return final
        
def checkString(cur):
    replace = ""
    if "string" in cur.lower():
        print "Found string! What would you like to replace it with?"
        replace = raw_input()
        replace = cur.lower().replace("string",replace)
    return replace if replace else cur

def cleanString(cur):
    cur = checkString(cur)
    cur = cur.replace(":", "")
    cur = cur.replace("_", " ")
    return cur
