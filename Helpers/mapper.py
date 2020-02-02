import numpy as np
import json
from collections import defaultdict

class mapper:
    index = None
    subArray = None
    dataIds = None
    #used for the classifier?
    dataPoints = None
    #the Observable data
    point = None
    #the data that is used to build the map
    data = None
    #maps the state <x,y> to the observable <mag(x,y,z), acc(pitch, yah, roll), other stuff I store>
    ObservedStates = None
    Map = None

    #can create a map automatically if given a list of data or a link to data json
    def __init__(self, data=None):
        self.index = [0,0]
        self.subArray = np.array([[0,0],[0,0]], dtype=float)
        self.dataIds = defaultdict(str)
        self.dataPoints = defaultdict(tuple)
        self.point = dict()
        self.ObservedStates = defaultdict(list)

        if data is not None:
            if (type(data) is list):
                self.data = data
            elif(type(data) is str):
                print(data)
                self.getDataFromJSON(data)
            else:
                print("Use the directionMapper() function on a sequence of points")


        if self.data is not None:
            self.buildMapFromData()

    def getSubArray(self):
        return self.subArray

    def getDataIds(self):
        return self.dataIds

    def getPoint(self):
        return self.point

    def getIndex(self):
        return self.index

    def getDataPoints(self):
        return self.dataPoints
    
    def getObservedStates(self):
        return self.ObservedStates
        
    def getMap(self):
        return self.Map

    # don't add extension when using
    def writeMaptoFile(self, filename):
        try:
            np.savetxt(filename.join('.txt'), self.subArray, delimiter=',')
            f = open(''.join(filename+'.json'), 'w')
            f.write(json.dumps(self.dataIds))
        except:
            print("could not write to file")
        finally:
            f.close()
        
    def readMapFromFile(self, filename, dtype):
        try:
            f = open(''.join(filename+'.json'), 'r')
            self.subArray = np.loadtxt(filename.join('.txt'), dtype=dtype, delimiter=',')
            self.dataIds = json.loads(f.read())
        except:
            print('failed to read map')
        finally:
            f.close()

    def getDataFromJSON(self, link):
        try:
            f = open(''.join(link), 'r')
            self.data = json.loads(f.read())
        except:
            print('failed to open map')
        finally:
            f.close()

# Calls directionMapper, which creates the map and assigns the points
    def buildMapFromData(self):
        for point in self.data:
                self.directionMapper(point)
        self.buildMapFromStates()

    '''
    # for MatLabPlotting
    def getPlotables(self):
        self.buildDataPoints()
        points = self.dataPoints
        x_list = [key[0] for key in points.keys()]
        y_list = [key[1] for key in points.keys()]
        #print(points.values())
        v_list = [value['tesla'] for value in points.values()]
        return x_list, y_list, v_list
    '''

#creates a list of points 
    def buildObservedStates(self, movement):
        self.ObservedStates[((self.index[0], self.index[1]), self.point['direction'])].append(self.point)
        self.index = [self.index[0]+movement[0], self.index[1]+movement[1]]

    def buildMapFromStates(self):
        rows, cols = self.getMapSizeFromObservedStates()
        a = [[0] * rows for i in range(cols)]
        for i in range(len(a)):
            for j in range(len(a[i])):

                pair = (j,i)
                '''
                a[i][j] = pair
                counter += 1
                '''
                if pair in [x[0] for x in self.ObservedStates.keys()]:
                    a[i][j] = 1
                else:
                    a[i][j] = 0
                
        self.Map = a
                

    def getMapSizeFromObservedStates(self):
        xMax = 0
        yMax = 1
        for state in [x[0] for x in self.ObservedStates.keys()]:
            if state[0] > xMax:
                xMax = state[0]
            if state[1] > yMax:
                yMax = state[1]
        return xMax, yMax

    def directionMapper(self, point):
        self.point = point
        direction = str(point['direction'])
        movement = [0,0]
        if('N' in direction):
            movement[1]+=1
        if('E' in direction):
            movement[0]+=1
        if('S' in direction):
            movement[1]-=1
        if('W' in direction):
            movement[0]-=1

        self.buildObservedStates(movement)
    
