import numpy as np
import json, math
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
    FigureMap = None

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

    def getFigureMap(self):
        return self.FigureMap

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
            f.close()
        except:
            print('failed to read map')

    def getDataFromJSON(self, link):
        try:
            f = open('Data/'+link+'.json', 'r')
            self.data = json.loads(f.read())
            f.close()
        except:
            print('failed to open map')

# Calls directionMapper, which creates the map and assigns the points
    def buildMapFromData(self):
        currentId = self.data[0]['meta']['stepId']
        for point in self.data:
            if point['meta']['stepId'] != currentId:
                self.directionMapper(point)
                currentId = point['meta']['stepId']
        self.normalizeStates()
        self.Map = self.buildMapFromStates()

    def buildFigureMap(self):
        self.FigureMap = self.buildMapFromStates(True)
    
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
        self.ObservedStates[((self.index[0], self.index[1]), self.point['meta']['direction'])].append(self.point['data'])
        self.index = [self.index[0]+movement[0], self.index[1]+movement[1]]
    

    def normalizeStates(self):
        values = self.getMapSizeFromObservedStates()
        self.ObservedStates = self.transform(self.ObservedStates, (values[2], values[3]))

    def transform(self, multilevelDict, modifier):
        return { ((key[0][0]+modifier[0], key[0][1]+modifier[1]), key[1]) : value for key, value in multilevelDict.items()}

    def buildMapFromStates(self, figure=False):
        values = self.getMapSizeFromObservedStates()
        coords = [x[0] for x in self.ObservedStates.keys()]
        a = [[0] * values[0] for i in range(values[1])]
        for i in range(len(a)):
            for j in range(len(a[i])):

                pair = (j,i)

                if pair in coords:
                    if figure is True:
                        observed = [self.ObservedStates[x] for x in self.ObservedStates.keys() if x[0] == pair][0][0]
                        a[i][j] = math.sqrt(observed['x']**2 + observed['y']**2 + observed['z']**2)
                    else:
                        a[i][j] = 1
                else:
                    a[i][j] = 0
                
        return a

    def getMeanAndStandardDeviation(self):
        val = []
        for observed in self.ObservedStates.values():
            val.append(math.sqrt(observed[0]['x']**2 + observed[0]['y']**2 + observed[0]['z']**2))
        mean = np.mean(val)
        std = np.std(val)
        minT = np.min(val)
        maxT = np.max(val)
        return mean, std, minT, maxT

    def getMapSizeFromObservedStates(self):
        states = [x[0] for x in self.ObservedStates.keys()]
        xMax = states[0][0]
        xMin = states[0][0]
        yMax = states[0][1]
        yMin = states[0][1]
        for state in states:
            if state[0] > xMax:
                xMax = state[0]
            if state[1] > yMax:
                yMax = state[1]
            if state[0] < xMin:
                xMin = state[0]
            if state[1] < yMin:
                yMin = state[1]
        xSize = abs(xMax - xMin)
        ySize = abs(yMax - yMin)

        #validation
        if xSize < 1:
            xSize = 1
            
        if ySize < 1:
            ySize = 1

        return xSize, ySize, abs(xMin), abs(yMin)


    def directionMapper(self, point):
        self.point = point
        direction = str(point['meta']['direction'])
        
        movement = self.directionToMovement(direction)

        self.buildObservedStates(movement)

    def directionToMovement(self, direction):
        movement = [0,0]
        if('N' in direction):
            movement[1]+=1
        if('E' in direction):
            movement[0]+=1
        if('S' in direction):
            movement[1]-=1
        if('W' in direction):
            movement[0]-=1
        return movement
    
