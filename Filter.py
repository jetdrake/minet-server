# press ESC to exit the demo!
from pfilter import (
    ParticleFilter,
    gaussian_noise,
    cauchy_noise,
    squared_error,
    independent_sample,
)
import numpy as np

# testing only
from scipy.stats import norm, gamma, uniform
import skimage.draw
import cv2

#minet imports
from Models import Map
from Helpers import knn


#holds all of the magnetic fingerprint data
magMap = Map.Map()
landmark_scalar = 100
landmark_offset_x = 24
landmark_offset_y = 120
raw_landmarks = list(magMap.getStates().keys())
landmarks = [(x[0][0]*landmark_scalar + landmark_offset_x, x[0][1]*landmark_scalar+landmark_offset_y) for x in magMap.getStates().keys()]

img_size = 48

def getRawState(state):
    for i, landmark in enumerate(landmarks):
        if landmark == state:
            return raw_landmarks[i]


# actually the observe function
def getObservableFromNearestLandmark(x):
    y = np.zeros((x.shape[0], 3))
    for i, particle in enumerate(x):
       '''
        rr, cc = skimage.draw.circle(
            particle[0], particle[1], max(particle[2], 1), shape=(img_size, img_size)
        )
        y[i, rr, cc] = 1
       '''
       #ignoreing heading for now
       state = knn.averagek((particle[0],particle[1]), landmarks, 1)
       observable = magMap.getObservablefromState(getRawState(state))
       #observable will be a list with the magData[x,y,z]
       y[i] = observable
    return y

# names (this is just for reference for the moment!)
columns = ["x", "y", "radius", "dx", "dy"]
initialStates = []
def initStates(n):
    global initialStates
    for i in range(n):
        s = np.random.randint(0, len(landmarks)-1)
        initialStates.append(landmarks[s])

def getRandomXCoord(n):
    global initialStates
    initStates(n)
    x = []
    for i in range(n):
        x.append(initialStates[i][0])
    return x


def getRandomYCoord(n):
    global initialStates
    y = []
    for i in range(n):
        y.append(initialStates[i][1])
    return y


# prior sampling function for each variable
# (assumes x and y are coordinates in the range 0-img_size)
# May adjust to select from a randomized group of states
prior_fn = independent_sample(
    [
        #the ouptput of all each of these is stacked [f1(n), f2(n), f3(n), f4(n), f5(n)]
        getRandomXCoord,
        getRandomYCoord,
        norm(loc=0, scale=0.5).rvs,
        norm(loc=0, scale=0.5).rvs,
        norm(loc=0, scale=0.5).rvs,
    ]
)

# names (this is just for reference for the moment!)
columns = ["x", "y", "orientation", "dx", "dy"]

# very simple linear dynamics: x += dx
def velocity(x):
    dt = 1.0
    xp = (
        x
        @ np.array(
            [
                [1, 0, 0, dt, 0],
                [0, 1, 0, 0, dt],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ]
        ).T
    )

    return xp

def squared_errorDebug(x, y, sigma=1):
    # RBF kernel
    d = np.sum((x - y) ** 2, axis=(1))
    return np.exp(-d / (2.0 * sigma ** 2))

def example_filter():
    # create the filter
    pf = ParticleFilter(
        prior_fn=prior_fn,
        observe_fn=getObservableFromNearestLandmark,
        n_particles=100,
        dynamics_fn=velocity,
        noise_fn=lambda x: x,
        weight_fn=lambda x, y: squared_errorDebug(x, y, sigma=1),
        resample_proportion=0.2,
        column_names=columns,
    )

    # np.random.seed(2018)
    # start in centre, random radius
    o = np.random.uniform(2, 8)

    # random movement direction
    dx = np.random.uniform(-0.25, 0.25)
    dy = np.random.uniform(-0.25, 0.25)

    # appear at centre
    coord = initialStates[1]
    x = coord[0]
    y = coord[1]

    scale_factor = 20

    # create window
    cv2.namedWindow("samples", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("samples", scale_factor * img_size, scale_factor * img_size)

    for i in range(1000):

        # generate fake data
        realData = getObservableFromNearestLandmark(np.array([[x, y, o]]))
        pf.update(realData)

        jimiage = np.zeros((1, img_size, img_size))

        img = cv2.resize(
            np.squeeze(jimiage), (0, 0), fx=scale_factor, fy=scale_factor
        )

        cv2.putText(
            img,
            "ESC to exit",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        color = cv2.cvtColor(img.astype(np.float32), cv2.COLOR_GRAY2RGB)

        # x_hat, y_hat, s_hat, dx_hat, dy_hat = pf.mean_state

        #highlight true data
        cv2.circle(
            color,
            tuple((int(x),int(y))),
            15,
            (255,0,255),
            1
        )

        '''
        # draw individual particles
        for particle in pf.original_particles:
            xa, ya, sa, _, _ = particle
            sa = np.clip(sa, 1, 100)
            cv2.circle(
                color,
                (int(ya * scale_factor), int(xa * scale_factor)),
                max(int(sa * scale_factor), 1),
                (1, 0, 0),
                1,
            )
        '''
        for particle in pf.particles:
            cv2.circle(
                color,
                tuple((int(particle[0]),int(particle[1]))),
                5,
                (0,0,255),
                1
            )

        '''
        # x,y exchange because of ordering between skimage and opencv
        cv2.circle(
            color,
            (int(y_hat * scale_factor), int(x_hat * scale_factor)),
            max(int(sa * scale_factor), 1),
            (0, 1, 0),
            1,
            lineType=cv2.LINE_AA,
        )
        cv2.line(
            color,
            (int(y_hat * scale_factor), int(x_hat * scale_factor)),
            (
                int(y_hat * scale_factor + 5 * dy_hat * scale_factor),
                int(x_hat * scale_factor + 5 * dx_hat * scale_factor),
            ),
            (0, 0, 1),
            lineType=cv2.LINE_AA,
        )
        '''
        for landmark in landmarks:
            cv2.circle(
                color,
                landmark,
                10,
                (0,255,255),
                1
            )

        cv2.imshow("samples", color)
        result = cv2.waitKey(20)
        # break on escape
        if result == 27:
            break
        x += dx
        y += dy

    cv2.destroyAllWindows()


if __name__ == "__main__":
    example_filter()
