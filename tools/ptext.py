

#Reverse line order
def reverse(x):
    f = open(x)
    t = f.readlines()
    r = list(reversed(t))
    #print "Raw: ", t
    #print "Input lines: ", t
    #print "Reversed: ", r
    f.close()
    return r

#Reverse all characters order
def flip(x):
    f = open(x, 'r')
    t = f.read()
    f = t[::-1]
    #print "Input lines: ", t
    #print "Flipped: ", f
    f.close()
    return f

#Search through lines and return lines that contain search phrase
def find(x):
    f = open(x, 'r')
    t = f.readlines()
    m = {}
    print "What phrase would you like to search for inside", str(x), "?"
    phrase = raw_input()
    print "Beginning search for: ", phrase
    for x in range(len(t)):
        if phrase in t[x]:
            m["Line "+str(x+1)] = t[x]
    print "Matches: ", m
    f.close()
    return m
