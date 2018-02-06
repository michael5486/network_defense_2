studentNum = 6
numI = 0


def getSubdomain(studentNum, numI):
    dga1lookup = ("abc", "qwe", "jkl")
    dga1Val = (numI * 3) + studentNum
    p1 = dga1Val % 3
    p2 = (dga1Val % 26) + 97
    dga1subdomain = dga1lookup[p1] + chr(p2)
    return dga1subdomain

for numI in range(0,30):
    print ("{}: {}").format(numI, getSubdomain(studentNum, numI))    
    #print ("{}.student06.dga.tiwaz.net. IN A 192.168.88.106").format(getSubdomain(studentNum, numI))