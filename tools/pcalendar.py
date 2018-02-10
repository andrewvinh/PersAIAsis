from imports import *
import pdata
import panalyze
import ptime

def allEvents(*args):
    pdata.checkDict("Calendar")

def checkCal(*args):
    local = pdata.getLocal("Calendar")
    if len(local) > 0:
        for key in sorted(local):
            later = ptime.compare(key)
            if later:
                cur = local[key]
                print key
                if isinstance(cur,list):
                    for item in cur:
                        print item
                else:
                    print cur
    else:
        print "Empty calendar"

def addEvent(words):
    print "Creating new calendar event"
    new = schema.newCal()
    key = ptime.today()
    count = 0
    while count < len(words):
        cur = words[count]
        if cur in new.keys() and count < len(words)-1:
            if isinstance(new[cur],list):
                new[cur] = new[cur] + [words[count+1]]
            else:
                new[cur] = panalyze.cleanString(words[count+1])
        elif cur.lower() == "date" and count < len(words)-1:
            key = words[count+1].replace(".","-")
        count = count + 1
    if key == ptime.today():
        print "Enter date (ex: 2018.02.14):"
        key = raw_input().replace(".","-").split("-")
        while len(key) != 3:
            print "Re-enter date: "
            key = raw_input().split("-")
        key[1] = "0" + key[1] if len(key[1]) == 1 else key[1]
        key[2] = "0" + key[2] if len(key[2]) == 1 else key[2]
        key = "-".join(key)
    for item in ["Name", "Start"]:
        if len(new[item]) == 0:
            print "Event", item, ":"
            new[item] = panalyze.cleanString(raw_input())
    if len(new["Notes"]) == 0:
        print "Any notes?"
        note = panalyze.cleanString(raw_input())
        if note.lower() != "no":
            new["Notes"] = new["Notes"] + [note]
    print "Final new: ", {key:[new]}
    pdata.dictAdd("Calendar", {key:[new]})

def dailyEvents():
    print "Hmm.. Let's see if we're doing anything today.."
    cal = pdata.getLocal("Calendar")
    today = ptime.today()
    #print ptime.time()
    show = 1
    if today in cal.keys():
        print "You have an event today! Would you like to see it?"
        show = raw_input().lower()
        if show == "yes":
            temp = cal[today]
            for event in temp:
                for item in ["Name", "Start", "Notes"]:
                    print item, ":", event[item]
        else:
            show = 0
    else:
        print "No events today! You're free to do whatever you'd like!"
        show = 0
    return show
