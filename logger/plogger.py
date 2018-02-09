from imports import *
import pdata
import ptime
import schema

def newLog(user, args):
    now = ptime.now()
    val = schema.newLog(user, args, now)
    old = pdata.getLocal("Log")
    oldKey = old.keys()[0][0:10] if len(old.keys()) > 0 else now[0:10]

def recordDay(log):
    print "Recording yesterday's log and resetting daily log"
    out = str(os.path.dirname(os.path.abspath(__file__))+"/dlogs/"+ptime.yesterday()+".txt")
    with open(out,'w') as f:
        f.write(json.dumps(log, sort_keys=False, indent=2))
    pdata.updateLocal("Log",schema.blankDict())
