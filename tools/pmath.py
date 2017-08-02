

def add(f):
    print "Attempting to add: ", f
    total = 0
    for count in range(len(f)):
        value = float(f[count])
        f[count] = value
        total = total + value
    print "Total: ", str(total)
    print "Summed: ", str(sum(f))
    return total

def multiply(f):
    print "Attempting to multiply: ", f
    total = 1
    for count in range(len(f)):
        value = float(f[count])
        f[count] = value
        total = total * value
    print "Multiplied: ", str(total)
    return total

