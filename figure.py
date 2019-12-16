import json
import numpy as np
import mapper
import matplotlib.pyplot as plt
from scipy.stats import kde
from collections import defaultdict
import seaborn as sb


#test = open('file.txt', 'w')
'''
#main
mapper = mapper.mapper('map.json')
mapper.writeMaptoFile('map1')
'''
mapper = mapper.mapper()
mapper.readMapFromFile('map1', 'float')
map = mapper.getSubArray()

ax = sb.heatmap(map)

plt.show()
