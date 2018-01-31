"""
curl 'https://api.twilio.com/2010-04-01/Accounts/AccountSID/Messages.json' -X POST \
--data-urlencode 'To=+14086938190' \
--data-urlencode 'From=+14087097097' \
-u AccountSID:AuthToken
"""
from imports import *
from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = pdata.getConfig("twilID")
# Your Auth Token from twilio.com/console
auth_token  = pdata.getConfig("twilAuth")

def textMyself(words):
    print "Texting the main body: ", words
    client = Client(account_sid, auth_token)
    """
    message = client.messages.create(
    to = myself, 
    from_ = self,
    body = ''.join(str(e+" ") for e in words))
    print(message.sid)"""

def addContact(add):
    print "Add: ", add
    new = schema.contact()
    count = 0
    while count < len(add):
        if add[count] in new.keys():
            if add[count] == "Relation":
                new[add[count]].append(panalyze.checkString(add[count+1]).lower())
            else:
                new[add[count]] = panalyze.checkString(add[count+1])
                count = count + 1
        count = count + 1
    conts = pdata.getLocalContacts()
    #print "New: ", new["Name"]
    temp = getID(new["Name"].lower())
    #print "Temp: ", temp
    if len(temp) == 0:
        conts[str(len(conts))] = new
        pdata.updateContacts(conts)
        return 1
    else:
        print "Contact already present."
        return 0
    

def outText(words):
    print "Attempting to text: ", words[0]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = kris if words[0] == "kris" else myself, 
    from_ = self,
    body = ''.join(str(e+" ") for e in words[1::]))

def addRelation(words):
    user = panalyze.checkString(words[0])
    conts = pdata.getLocalContacts()
    print "User: ", user
    print "New relations: ", words[1::]
    print "Search: ", getID(user)
    for found in getID(user):
        print conts[found]

#Args: UserID Category Change
def editContact(words):
    conts = pdata.getLocalContacts()
    user = words[0]
    cat = words[1]
    add = words[2]
    print "User: ", user, " Category: ", cat, " Edit: ", add
    if user in conts.keys():
        user = conts[user]
    else:
        print "User not found, defaulting to self"
        user = conts[getID(user)[0]] if getID(user) else conts["0"]
    print user


def getID(search):
    search = panalyze.checkString(search[0]) if isinstance(search, list) else panalyze.checkString(search)
    #print "Search: ", search
    conts = pdata.getLocalContacts()
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
    #print "All ID's that match: ", final
    return final
