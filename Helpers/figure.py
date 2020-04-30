import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
from collections import defaultdict
import seaborn as sb

def generateHeatMap(map):
    g = sb.heatmap(map, vmin=0)
    plt.show()
