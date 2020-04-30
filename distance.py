import math
from Helpers import testlogger

def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist

tl = testlogger.logger()

while True:
    num1 = int(input('1: '))
    num2 = int(input('2: '))
    num3 = int(input('3: '))
    num4 = int(input('4: '))

    dist = calculateDistance(num1, num2, num3, num4)
    tl.append(str(dist))
    print(str(dist))

