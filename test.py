import classifier

rr = classifier.classifier('map')
#rr.getAccuracy()

point = {'x': '16.45051', 'y': '13.61105', 'z': '-43.274338', 'tesla': '48.25503434714092', 'azimuth': '-1.0102066', 'pitch': '0.065881215', 'roll': '-0.015606907', 'ID': 'Room not set', 'direction': 'W'}

this = rr.predictRawPoint(point)

print(this)