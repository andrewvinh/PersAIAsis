from imports import *

def now(*args):
    now = datetime.datetime.today()
    return now

def length(start):
    print "Start: ", start
    end = datetime.datetime.today()
    length = (end - start)
    print length
    print length.total_seconds()
    print "%.3gs" % length.total_seconds() 
