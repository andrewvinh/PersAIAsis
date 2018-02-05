from imports import *
import pdata
import panalyze


def checkCalendar(*args):
    pdata.checkDict("Calendar")

def addEvent(words):
    print "Creating new calendar event"
    local = pdata.getLocal(words[0])
    new = schema.newCal()
    if isinstance(local, dict):
        print local
    else:
        print "Local branch not found. Note: Keys are case-senstitive"
