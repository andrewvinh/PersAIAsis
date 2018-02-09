from imports import *

def now(*args):
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

def length(start):
    end = datetime.datetime.today()
    length = (end - start)
    print "--------\nTime Results\n-------"
    print "Start: ", start
    print "End: ", end
    print "%.3gs" % length.total_seconds() 

def today(*args):
    today = datetime.datetime.today()
    month = ("0" + str(today.month)) if today.month < 10 else str(today.month)
    day = ("0" + str(today.day)) if today.day < 10 else str(today.day)
    year = str(today.year)
    today = year+"-"+month+"-"+day
    #print today
    return today

def yesterday(*args):
    yesterday = (datetime.datetime.today() - timedelta(1)).strftime("%Y-%m-%d %H:%M:%S")
    #print yesterday
    return yesterday[0:10]

def getDate(date):
    print date
    cur = today()
    print cur

def time():
    today = datetime.datetime.today()
    time = str(today.hour)+":"+str(today.minute)+":"+str(today.second)
    return time

def convertHour(hour):
    print hour
