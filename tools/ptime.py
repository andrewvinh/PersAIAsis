from imports import *

def now(*args):
    now = datetime.datetime.today()
    #time.sleep(2)
    #length(now)
    return now

def length(start):
    end = datetime.datetime.today()
    length = (end - start)
    #print length
    #print length.total_seconds()
    print "--------\nTime Results\n-------"
    print "Start: ", start
    print "End: ", end
    print "%.3gs" % length.total_seconds() 
