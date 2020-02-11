#from Helpers import classifier

#rr = classifier.classifier('map')
#rr.getAccuracy()

#point = {'x': '16.45051', 'y': '13.61105', 'z': '-43.274338', 'tesla': '48.25503434714092', 'azimuth': '-1.0102066', 'pitch': '0.065881215', 'roll': '-0.015606907', 'ID': 'Room not set', 'direction': 'W'}

#this = rr.predictRawPoint(point)

#print(this)
'''
from Helpers import mapper

Map = mapper.mapper('Data/map.json')

print(Map.getSubArray())
print(Map.getDataIds())
#print(Map.getDataPoints())
'''

from Models import Map


thisMap = Map.Map()
print(thisMap.getObservablefromState((1,0)))
vismap = thisMap.getMap()
print(vismap)
