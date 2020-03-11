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

    def getObservableFromNearestLandmark(self, landmark, direction=None):
        nearestLandmark = knn.averagek(landmark, self.landmarks, 1)
        self.landmarkPopularity[nearestLandmark] += 1
        state = self.getStatesFromLandmark(nearestLandmark)
        observable = self.getObservablefromState(state)
        return observable

    def getObservablefromState(self, state):
        #handles if orientation is available or not
        if len(state) == 1:
            first = [self.States[x] for x in self.States if x == state][0] #very ugly I know
        else:
            
            #currently returns a list of dicts, in case there are more than one reading at each landmark
            #will need to figure out how to integrate that. Right now just the first reading is passed
            first = [self.States[x] for x in self.States if x == state][0][0]
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
        sorted_dict = sorted(self.landmarkPopularity.items(), key=operator.itemgetter(1))
        sorted_dict.reverse()
        self.landmarkPopularity.clear()
        return sorted_dict[0]

    def getMostPopularState(self):
        landmark = self.getMostPopularLandmark()
        return self.getStatesFromLandmark(landmark)

    def getStates(self):
        return self.States

    def getMap(self):
        return self.Map

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
