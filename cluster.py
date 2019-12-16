from sklearn.datasets import make_blobs
import numpy as np
import json
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d


test = open('map.txt', 'r')
testObj = json.loads(test.read())

x_list = []
y_list = []
z_list = []

for obj in testObj:
    x_list.append(obj['x'])
    y_list.append(obj['y'])
    z_list.append(obj['tesla'])

x_list = np.array(x_list)
y_list = np.array(y_list)
z_list = np.array(z_list)


# f will be a function with two arguments (x and y coordinates),
# but those can be array_like structures too, in which case the
# result will be a matrix representing the values in the grid 
# specified by those arguments
f = interp2d(x_list,y_list,z_list,kind="linear")

x_coords = np.arange(min(x_list),max(x_list)+1)
y_coords = np.arange(min(y_list),max(y_list)+1)
Z = f(x_coords,y_coords)

fig = plt.imshow(Z,
           extent=[min(x_list),max(x_list),min(y_list),max(y_list)],
           origin="lower")

# Show the positions of the sample points, just to have some reference
fig.axes.set_autoscale_on(False)
plt.scatter(x_list,y_list,400,facecolors='none')