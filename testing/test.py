from imports import *
import psms
import pcalendar

def runCheck(words):
    print "Running DB check"
    pdata.lookup("")
    print "-------"
    print "Running Contact check"
    psms.listContacts(["andrew"])
    print "-------"
    psms.listContacts(["family"])
    print "-------"
    print "Running Calendar check"
    pcalendar.checkCal()
    print "-------"
    print "Adding temp category to contacts"
    pdata.addCat(["Contacts","temp"])
    psms.listContacts("andrew")
    print "-------"
    print "Removing temp category from contacts"
    pdata.removeCat(["Contacts","temp"])
    psms.listContacts("andrew")
