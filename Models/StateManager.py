from Helpers import mapper, knn
from collections import defaultdict
import operator
import numpy as np

class StateManager:
    # Handles all state related methods for the particle filter
    Mapper = None
    Map = None
    # State is a dict ((x,y)o) = {'x':123123, 'y':123123, 'z':123123 ... }
    States = None
    #list of states the particle Filter
    initialStates = []
    #scaled states for the map
    landmarks = []
    landmarkStates = defaultdict(list)
    #scores the landmarks most often used
    landmarkPopularity = defaultdict(int)
    popularLandmark = None
    #used to setup the landmarks for the size of the image
    scale = None

    def __init__(self, link='line.json', scale=48, n=100):
        self.Mapper = mapper.mapper(link)
        self.Map = self.Mapper.getMap()
        self.States = self.Mapper.getObservedStates()
        self.scale = scale
        self.createLandmarks()
        self.initStates(n)

    def getStatesFromLandmark(self, landmark):
        # gets the unscaled state
            return self.landmarkStates[landmark][0]

    def getMovementFromDirection(self, direction):
        movement = self.Mapper.directionToMovement(direction)
        scaler = self.scale * 2
        x_offset = self.scale / 2
        y_offset =  x_offset * 5

        movement[0] = movement[0] * scaler + x_offset
        movement[1] = movement[1] * scaler + y_offset

        return movement

    def getObservableFromNearestLandmark(self, landmark, direction=None):
        #handle direction: needs to be able to sort by contains (direction) - limit landmarks maybe
        directedLandmarks = [x for x in self.landmarks if direction in x[1]]
        
        nearestLandmark = knn.averagek(landmark, directedLandmarks if (directedLandmarks is not None and directedLandmarks != []) else self.landmarks, 1)
        self.landmarkPopularity[nearestLandmark] += 1
        state = self.getStatesFromLandmark(nearestLandmark)
        observable = self.getObservablefromState(state)
        return observable

    def getObservablefromState(self, state):
        #handles if orientation is available or not
        default = [{'x':0.0, 'y': 0.0, 'z': 0.0}]

        #first = [self.States[x] for x in self.States if x == state]
        first = self.States.get(state, default)
        first = first[0]

        #returns the valuable observable data
        return [first['x'], first['y'], first['z']]

    def initStates(self, n):
        for i in range(n):
            s = np.random.randint(0, len(self.landmarks)-1)
            self.initialStates.append(self.landmarks[s])

    def createLandmarks(self):
        scaler = self.scale * 2
        x_offset = self.scale / 2
        y_offset =  x_offset * 5

        for state in self.States:
            coord = state[0]
            landmark = (coord[0]*scaler+x_offset,coord[1]*scaler+y_offset), state[1]
            self.landmarks.append(landmark)
            self.landmarkStates[landmark].append(state)

    def getMostPopularLandmark(self):
        return self.popularLandmark

    def setMostPopularLandmark(self):
        sorted_dict = sorted(self.landmarkPopularity.items(), key=operator.itemgetter(1))
        sorted_dict.reverse()
        landmark = sorted_dict[0][0]
        self.popularLandmark = landmark
        self.landmarkPopularity.clear()

    def getPopularState(self):
        return self.getStatesFromLandmark(self.popularLandmark)

    def getStates(self):
        return self.States

    def getMap(self):
        return self.Map

    def getMapForPublish(self):
        mp = set([x[0] for x in self.States])
        return list(mp)

    def getLandmarks(self):
        return self.landmarks

    def getInitialStates(self):
        return self.initialStates


# used only in simulation

    def getRandomXCoord(self, n):
        x = []
        for i in range(n):
            x.append(self.initialStates[i][0][0])
        return x

    def getRandomYCoord(self, n):
        y = []
        for i in range(n):
            y.append(self.initialStates[i][0][1])
        return y
