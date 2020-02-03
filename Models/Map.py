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
        #handles if orientation is available or not
        if len(state) == 1:
            first = [x for x in self.States if x[0] == state][0][0] #very ugly I know
        else:
            if state in self.States:
                #currently returns a list of dicts, in case there are more than one reading at each landmark
                #will need to figure out how to integrate that. Right now just the first reading is passed
                first = self.States[state][0]
            else:
                first = [{"pitch": 0, "id": " ", "direction": " ", "azimuth": 0, "x": 0, "roll": 0, "y": 0, "z": 0, "tesla": 0}][0]
        #returns the valuable observable data
        return [first['x'], first['y'], first['z']]

        
    def getStates(self):
        return self.States

    def getMap(self):
        return self.Map