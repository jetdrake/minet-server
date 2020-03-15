# press ESC to exit the demo!
from Helpers.pfilter import (
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
from Models import StateManager
from Helpers import knn

sm = StateManager.StateManager()

# actually the observe function
def getObservableFromNearestLandmark(x, pose):
    y = np.zeros((x.shape[0], 3))
    for i, particle in enumerate(x):
       observable = sm.getObservableFromNearestLandmark((particle[0],particle[1]), pose)
       #observable will be a list with the magData[x,y,z]
       y[i] = observable
    return y

def getDirection():
    return ['E' for i in range(101)]

# names (this is just for reference for the moment!)
columns = ["x", "y", "orientation", "dx", "dy"]

# prior sampling function for each variable
# (assumes x and y are coordinates in the range 0-img_size)
# May adjust to select from a randomized group of states
prior_fn = independent_sample(
    [
        #the ouptput of all each of these is stacked [f1(n), f2(n), f3(n), f4(n), f5(n)]
        sm.getRandomXCoord,
        sm.getRandomYCoord,
        norm(loc=0, scale=0.5).rvs,
        norm(loc=0, scale=0.5).rvs,
        norm(loc=0, scale=0.5).rvs,
    ]
)

# names (this is just for reference for the moment!)
columns = ["x", "y", "radius", "dx", "dy"]

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

#direction is [x,y]
def directedMotionModel(x, movement):

    x[0] = x[0] + movement[0]
    x[1] = x[1] + movement[1]

    return x


def squared_errorDebug(x, y, sigma=1):
    # RBF kernel
    d = np.sum((x - y) ** 2, axis=(1))
    return np.exp(-d / (2.0 * sigma ** 2))

class MapFilter():

    fakeData = None

    def __init__(self):
        #holds all of the magnetic fingerprint data
        self.manager = sm

        # create the filter
        self.pf = ParticleFilter(
            prior_fn=prior_fn,
            observe_fn=getObservableFromNearestLandmark,
            n_particles=100,
            dynamics_fn=directedMotionModel,
            noise_fn=lambda x: x,
            weight_fn=lambda x, y: squared_errorDebug(x, y, sigma=1),
            resample_proportion=0.2,
            column_names=columns,
        )

    def update(self, realData, pose, v=True):

        # generate fake data
        self.realData = realData
        self.pf.setPose(pose)
        self.pf.setMovement(self.manager.getMovementFromDirection(pose))
        self.pf.update(realData)
        self.manager.setMostPopularLandmark()

        # x_hat, y_hat, s_hat, dx_hat, dy_hat = pf.mean_state

        #update visuals if desired
        self.visualMode = v
        if self.visualMode is True:

            self.initWindow()
            self.drawParticles()
            self.drawLandmarks()
            #self.drawMeanData()
            self.drawMostPopularLandmark()
            if self.fakeData is not None:
                self.drawFakeData()

            cv2.imshow("samples", self.color)
            result = cv2.waitKey(20)
            # break on escape
            if result == 27:
                self.quit()

    def setFakeData(self, fakeData):
        self.fakeData = fakeData

    def getMapForPublish(self):
        return self.manager.getMapForPublish()

    def getMeanState(self):
        return self.pf.mean_state

    def getMostPopularState(self):
        return self.manager.getPopularState()

    def initWindow(self, img_size=48, scale_factor=20):
        # create window
        cv2.namedWindow("samples", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("samples", scale_factor * img_size, scale_factor * img_size)

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

        self.color = cv2.cvtColor(img.astype(np.float32), cv2.COLOR_GRAY2RGB)

    def drawParticles(self):
        for particle in self.pf.particles:
                cv2.circle(
                    self.color,
                    tuple((int(particle[0]),int(particle[1]))),
                    5,
                    (0,0,255),
                    1
                )

    def drawLandmarks(self):
        for landmark in self.manager.getLandmarks():
            coord = landmark[0]
            cv2.circle(
                self.color,
                (int(coord[0]),int(coord[1])),
                10,
                (0,255,255),
                1
            )

    def drawMeanData(self):
        #highlight true data
        mean_state = self.pf.mean_state
        try:
            x = mean_state[0]
            y = mean_state[1]

            cv2.circle(
                self.color,
                (int(mean_state), int(mean_state)), #needs to get the nearest observable value
                35,
                (255,0,255),
                1
            )   
        except :
            print("MeanData not valid")
        

    def drawMostPopularLandmark(self):
        landmark = self.manager.getMostPopularLandmark()
        coord = landmark[0]
        cv2.circle(
            self.color,
            (int(coord[0]), int(coord[1])), #needs to get the nearest observable value
            15,
            (122,0,0),
            1
        )

    def drawFakeData(self):
        cv2.circle(
            self.color,
            (int(self.fakeData[0]), int(self.fakeData[1])), #needs to get the nearest observable value
            15,
            (255,0,255),
            1
        )

    def quit(self):
        cv2.destroyAllWindows()
