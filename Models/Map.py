from Helpers import mapper

class Map:
    # wraps Mapper to provide accessible methods for the filter
    Mapper = None
    Map = None
    States = None

    def __init__(self, link='Data/map.json'):
        self.Mapper = mapper.mapper(link)       
        self.Map = self.Mapper.getMap()
        self.States = self.Mapper.getObservedStates()

    def getObservablefromState(self, state):
        if state in self.States:
            return self.States[state]
        else:
            return  [{"pitch": 0, "id": " ", "direction": " ", "azimuth": 0, "x": 0, "roll": 0, "y": 0, "z": 0, "tesla": 0}]
    
    def getStates(self):
        return self.States

    def getMap(self):
        return self.Map