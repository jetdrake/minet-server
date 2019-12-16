import numpy as np
import json
from collections import defaultdict

class mapper:
    index = None
    subArray = None
    dataIds = None
    dataPoints = None
    point = None
    data = None

    #can create a map automatically if given a list of data or a link to data json
    def __init__(self, data=None):
        self.index = [0,0]
        self.subArray = np.array([[0,0],[0,0]], dtype=float)
        self.dataIds = defaultdict(str)
        self.dataPoints = defaultdict(tuple)
        self.point = dict()

        if data is not None:
            if (type(data) is list):
                self.data = data
            elif(type(data) is str):
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

    #don't add extension when using
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

    def buildMapFromData(self):
        for point in self.data:
                self.directionMapper(point)

    def getDataFromJSON(self, link):
        try:
            f = open(''.join(link), 'r')
            self.data = json.loads(f.read())
        except:
            print('failed to open map')
        finally:
            f.close()

    def buildDataPoints(self):
        for i, row in enumerate(self.subArray):
            for j, item in enumerate(row):
                if (item > 0):
                    key = str(item)
                    #print(self.dataIds[key])
                    self.dataPoints[(i,j)] = self.dataIds[key]
                else:
                    self.dataPoints[(i,j)] = {'tesla' : 0.0}

    def getPlotables(self):
        self.buildDataPoints()
        points = self.dataPoints
        x_list = [key[0] for key in points.keys()]
        y_list = [key[1] for key in points.keys()]
        #print(points.values())
        v_list = [value['tesla'] for value in points.values()]
        return x_list, y_list, v_list

    def assignment(self):
        index = self.index
        sa = self.subArray

        id = str(float(len(self.dataIds) + 1))
        saList = sa.tolist()
        saList[index[1]][index[0]] = id
        
        self.subArray = np.array(saList, dtype=float)
        self.dataIds[id] = self.point

    def tester(self, movement):
        sa = self.subArray
        index = self.index
        x = movement[0]
        y = movement[1]
        if x > 0:
            if (index[0]+x) <= 0:
                sa = np.hstack((sa, np.zeros((sa.shape[0], 1), dtype=sa.dtype))) #add to left
            elif (index[0]+x) >= sa.shape[0]:
                sa = np.hstack((sa, np.zeros((sa.shape[0], 1), dtype=sa.dtype))) #add to right
            
            index[0]+=x
        
        if y > 0:
            if (index[1]+y) <= 0:
                sa = np.vstack((sa, np.zeros((1, sa.shape[1]), dtype=sa.dtype))) #add to top
            elif (index[0]+y >= sa.shape[1]):
                sa = np.vstack((sa, np.zeros((1, sa.shape[1]), dtype=sa.dtype))) #add to bottom
            
            index[1]+=y

        self.subArray = sa
        self.index = index


    def directionMapper(self, point):
        self.point = point
        direction = str(point['direction'])
        movement = [0,0]
        if('N' in direction):
            movement[1] = movement[1]-1
        if('E' in direction):
            movement[0]+=1
        if('S' in direction):
            movement[1]+=1
        if('W' in direction):
            movement[0]-=1

        self.tester(movement)
        self.assignment()

    





