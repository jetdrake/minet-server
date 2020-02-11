from Models import MapFilter
import numpy as np

example_filter = MapFilter.MapFilter()

# np.random.seed(2018)
# start in centre, random radius
o = np.random.uniform(2, 8)

# random movement direction
dx = np.random.uniform(-0.25, 0.25)
dy = np.random.uniform(-0.25, 0.25)

# appear at centre
coord = example_filter.manager.getInitialStates()[0]
x = coord[0]
y = coord[1]

scale_factor = 20

for i in range(1000):

    # generate fake data
    realData = example_filter.manager.getObservableFromNearestLandmark((x,y))
    example_filter.setFakeData((x,y))
    example_filter.update(realData)

    '''
    jimiage = np.zeros((1, img_size, img_size))

    img = cv2.resize(
        np.squeeze(jimiage), (0, 0), fx=scale_factor, fy=scale_factor
    )

    # x_hat, y_hat, s_hat, dx_hat, dy_hat = pf.mean_state
    '''

    x += dx
    y += dy