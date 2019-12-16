import json
from collections import defaultdict
import numpy as np

#

class dataProcessor:
    labels = None
    label_names = None
    features = None
    raw_data = None
    feature_names = None

    def parseRRData(self, filename):
        with open('data/'+filename+'.json', 'r') as data_file:
            self.raw_data = json.load(data_file)

        for element in self.raw_data:
            self.labels.append(element.pop('id', None))

        with open('data/classify/'+filename+'_data.json', 'w') as dataJ:
            json.dump(self.raw_data, dataJ)

        with open('data/classify/'+filename+'_labels.json', 'w') as labelJ:
            json.dump(self.labels, labelJ)

    def getDataFromFile(self, filename):
        with open('data/classify/'+filename+'_data.json', 'r') as dataJ:
            return json.load(dataJ)

    def getLabelsFromFile(self, filename):
        with open('data/classify/'+filename+'_labels.json', 'r') as labelJ:
            return json.load(labelJ)

    def parseLabelsAndLabelNames(self):
        if self.raw_data is not None:
            unique = list()
            self.labels = list()
            for element in self.raw_data:
                key = element['id']
                if key not in unique:
                    unique.append(key)
                self.labels.append(unique.index(key))
            self.label_names = unique
        else:
            print('need to parse raw data')

    def parseFeaturesAndFeatureNames(self):
        if self.raw_data is not None:
            #remove the id attributes
            for element in self.raw_data:
                element.pop('id', None)
                element.pop('ID', None)
                element.pop('direction', None)
            self.features = np.array([list(element.values()) for element in self.raw_data], dtype=float)
            self.feature_names = list(self.raw_data[0].keys())

    def ParseRawData(self, filename):
        with open('data/'+filename+'.json', 'r') as data_file:
            self.raw_data = json.load(data_file)
        
    def getFormattedData(self, filename=None):
        if filename is not None:
            self.ParseRawData(filename)

        if self.raw_data is not None:
            self.parseLabelsAndLabelNames()
            self.parseFeaturesAndFeatureNames()
        
        return self.features, self.feature_names, self.labels, self.label_names

    def getFeaturesFromDict(self, point):
        x = point['x']
        y = point['y']
        z = point['z']
        pitch = point['pitch']
        roll = point['roll']
        azimuth = point['azimuth']
        tesla = point['tesla']

        package = [pitch, azimuth, x, roll, y, z, tesla]

        array = np.array(package, dtype=float)
        array = array.reshape(1, -1)
        return array


if __name__ == '__main__':
    processor = dataProcessor()
    processor.parseRRData('map')