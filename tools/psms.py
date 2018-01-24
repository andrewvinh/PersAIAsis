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

self = "+14087097097"
myself = "+14086938190"
henry = "+14085689536"
kris = "+14086213791"

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
                new[add[count]].append(panalyze.checkString(add[count+1]))
            else:
                new[add[count]] = panalyze.checkString(add[count+1])
                count = count + 1
        count = count + 1

    conts = pdata.getLocalContacts()
    conts[str(len(conts))] = new
    pdata.updateContacts(conts)
    

def outText(words):
    print "Attempting to text: ", words[0]
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = kris if words[0] == "kris" else myself, 
    from_ = self,
    body = ''.join(str(e+" ") for e in words[1::]))

