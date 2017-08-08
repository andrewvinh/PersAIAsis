

def add(x):
    print "Attempting to add: ", x
    total = 0
    for count in range(len(x)):
        value = float(x[count])
        x[count] = value
        total = total + value
    print "Total: ", str(total)
    print "Summed: ", str(sum(x))
    return total

def multiply(x):
    print "Attempting to multiply: ", x
    total = 1
    for count in range(len(x)):
        value = float(x[count])
        x[count] = value
        total = total * value
    print "Multiplied: ", str(total)
    return total

