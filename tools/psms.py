"""
curl 'https://api.twilio.com/2010-04-01/Accounts/ACcdd91d351f6c22afb8f270c755b0c8e1/Messages.json' -X POST \
--data-urlencode 'To=+14086938190' \
--data-urlencode 'From=+14087097097' \
-u ACcdd91d351f6c22afb8f270c755b0c8e1:AuthToken
"""
from imports import *
from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = "ACcdd91d351f6c22afb8f270c755b0c8e1"
# Your Auth Token from twilio.com/console
auth_token  = pdata.getConfig("twilioAuth")

self = "+14087097097"
myself = "+14086938190"
henry = "+14085689536"
kris = "+14086213791"

def textMyself(words):
    print "Texting the main body: ", words
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = myself, 
    from_ = self,
    body = ''.join(str(e+" ") for e in words))
    print(message.sid)

def addContact(new):
    print "Adding to contacts: ", new
    conts = pdata.getLocalContacts()

def outText(words):
    print "Attempting to text: ", words[0]
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    to = kris if words[0] == "kris" else myself, 
    from_ = self,
    body = ''.join(str(e+" ") for e in words[1::]))

