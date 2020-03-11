from collections import defaultdict
import operator
import math

def dist(a, b):
    return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))

def average(pointList):
    totalx = 0
    totaly = 0
    #ignores orientation
    for point in [x[0] for x in pointList]:
        totalx += point[0][0]
        totaly += point[0][1]
    return (totalx/len(pointList), totaly/len(pointList))

def averagek(state, landmarks, k):
    stateDist = defaultdict(float)
    #directedLandmarks = [x for x in landmarks if state[1] in x[1]]
    for landmark in landmarks:
        stateDist[landmark] = dist(landmark[0], state)
    sorted_dict = sorted(stateDist.items(), key=operator.itemgetter(1))
    temp = sorted_dict[:k]
    # only used as the nearest/ average(temp) for k neighbors
    return temp[0][0]
	
