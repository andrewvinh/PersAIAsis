"""
curl 'https://api.twilio.com/2010-04-01/Accounts/AccountSID/Messages.json' -X POST \
--data-urlencode 'To=+14086938190' \
--data-urlencode 'From=+14087097097' \
-u AccountSID:AuthToken
"""
from imports import *
from twilio.rest import Client
import panalyze
import pdata
import schema

#paia listContacts 
#paia listContacts andrew
def listContacts(*args):
    conts = pdata.getLocal("Contacts")
    if len(conts) == 0:
        print "No contacts... loser."
    else:
        search = args[0][0].lower() if args[0] else ""
        if search:
            ids = getID(search)
            for item in sorted(ids):
                print "User ID: ", item
                print "Name: ", conts[item]["Name"]
                print "Mobile: ", conts[item]["Mobile"]
                print "Email: ", conts[item]["Email"]
                print "Relation: ", conts[item]["Relation"]
        else:
            count = 1
            while count < len(conts.keys())-1: #-1 because of Contact -1: Twilio Bot
                print "ID: ", count
                print "Name: ", conts[str(count)]["Name"]
                print "Mobile: ", conts[str(count)]["Mobile"]
                print "Email: ", conts[str(count)]["Email"]
                print "Relation: ", conts[str(count)]["Relation"]
                count = count + 1

def textMyself(words):
    account_sid = pdata.getConfig("twilID")
    auth_token  = pdata.getConfig("twilAuth")
    print "Texting the main body: ", words
    client = Client(account_sid, auth_token)
    to = getNumber("myself")
    self = getNumber("sender")
    print "To: ", to, " From: ", self
    message = ''.join(panalyze.cleanString(str(e+" ")) for e in words)
    for recipient in to:
        message = client.messages.create(
        to = recipient, 
        from_ = self,
        body = message)
    print(message.sid)

#paia textGroup family
def textGroup(words):
    if words:
        account_sid = pdata.getConfig("twilID")
        auth_token  = pdata.getConfig("twilAuth")
        client = Client(account_sid, auth_token)
        self = getNumber("sender")
        message = ''.join(panalyze.cleanString(str(e+" ")) for e in words[1::])
        ids = getID(words[0])
        print "To: ", ids
        print "Message: ", message
        for val in ids:
            print getNumber(val)
            message = client.messages.create(
            to = getNumber(val), 
            from_ = self,
            body = message)
            print(message.sid)

#paia addContact Name Test_Vinh Relation Testing Mobile 1666
def addContact(add):
    print "Add: ", add
    new = schema.newContact()
    count = 0
    while count < len(add):
        if add[count] in new.keys():
            if add[count] == "Relation":
                t1 = panalyze.cleanString(add[count+1]).lower()
                for t2 in t1.split():
                    new[add[count]].append(t2)
            else:
                new[add[count]] = panalyze.cleanString(add[count+1])
                count = count + 1
        count = count + 1
    conts = pdata.getLocal("Contacts")
    temp = getID(new["Name"].lower())
    if len(temp) == 0:
        print "Adding new contact!"
        conts[str(len(conts)-1)] = new
        pdata.updateContacts(conts)
        return 1
    else:
        print "Contact already present. Please call editContact to edit the contact"
        return 0

#paia editCL angel Relation dope
def editCL(words):
    user = panalyze.cleanString(words[0].lower())
    cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
    adds = []
    print "User: ", user, "cat:", cat
    for add in words[2::]:
        adds.append(panalyze.cleanString(add))
    conts = pdata.getLocal("Contacts")
    for found in getID(user): 
        cur = conts[found]
        print "Found match! Adding into ", cur["Name"]
        cur[cat] = cur[cat] + list(set(adds) - set(cur[cat]))
    pdata.updateLocal("Contacts", conts)

#paia removeCL angel Relation dope
def removeCL(words):
    user = panalyze.cleanString(words[0].lower())
    cat = panalyze.cleanString(words[1]) if len(words)>1 else panalyze.cleanString("String")
    removes = []
    for remove in words[2::]:
        removes.append(panalyze.cleanString(remove))
    conts = pdata.getLocal("Contacts")
    for found in getID(user):
        cur = conts[found]
        for rem in removes:
            try:
                updated = cur[cat].remove(rem)
                print "Removed", cat
            except:
                print cat, "not present"
    pdata.updateLocal("Contacts", conts)
        

#Args: UserID Category Change
def editContact(words):
    conts = pdata.getLocal("Contacts")
    user = words[0]
    cat = words[1]
    add = words[2]
    newID = getID(user)[0]
    user = conts[newID] if newID else conts["0"]
    #print "Found user: ", user
    user[cat] = panalyze.cleanString(add) if cat in user.keys() else user[cat]
    #print "New user: ", user
    conts[newID] = user
    #print "Confirmation: ", conts[newID]
    #print "Conts: ", conts
    pdata.updateContacts(conts)


def getID(search):
    search = panalyze.cleanString(search[0]) if isinstance(search, list) else panalyze.cleanString(search)
    conts = pdata.getLocal("Contacts")
    final = []
    for key in conts.keys():
        cur = conts[key]
        for k1 in cur.keys():
            c1 = cur[k1].lower() if isinstance(cur[k1],(str,unicode)) else cur[k1]
            #print "C1: ", c1
            if search in c1:
                #print "Found match"
                final.append(key)
                break
    return final

def getNumber(search):
    conts = pdata.getLocal("Contacts")
    if search not in conts.keys():
        ids = getID(search)
        final = []
        for item in ids:
            final.append(str("+" + conts[item]["Mobile"]))
        return final
    else:
        #Received input ID, returning matching number
        return str("+" + conts[search]["Mobile"])

