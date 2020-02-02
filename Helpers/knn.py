from collections import defaultdict
import operator
import math

def dist(a, b):
    return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))

def average(pointList):
    totalx = 0
    totaly = 0
    for point in pointList:
        totalx += point[0]
        totaly += point[1]
    return (totalx/len(pointList), totaly/len(pointList))

def averagek(state, landmarks, k):
    stateDist = defaultdict(float)
    for landmark in landmarks:
        stateDist[landmark] = dist(landmark, state)
    sorted_dict = sorted(stateDist.items(), key=operator.itemgetter(1))
    temp = sorted_dict[:k]
    return average(temp)
	
