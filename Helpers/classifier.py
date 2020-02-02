import sklearn
import dataProcessor

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
class classifier:
    model = None
    test = None
    test_labels = None
    processor = None
    label_names = None
    feature_names = None
    #room recognition classifer

    def __init__(self, filename='map'):
        self.getRRclassifier(filename)

    def getRRclassifier(self, filename='map'):
        self.processor = dataProcessor.dataProcessor()

        data = self.processor.getFormattedData('map')
        #returns features, feature_names, labels, label_names

        # Organize our data
        self.label_names = data[3]
        labels = data[2]
        self.feature_names = data[1]
        features = data[0]

        # Split our data
        train, test, train_labels, test_labels = train_test_split(features,
                                                            labels,
                                                            test_size=0.33,
                                                            random_state=42)

        # Initialize our classifier
        gnb = GaussianNB()

        # Train our classifier
        model = gnb.fit(train, train_labels)
        #assign to class
        self.test = test
        self.test_labels = test_labels
        self.model = model

    def getAccuracy(self):
        preds = self.model.predict(self.test)
        acc = accuracy_score(self.test_labels, preds)
        print(acc)
        return acc

    def predictRawPoint(self, point):
        test = self.processor.getFeaturesFromDict(point)
        result = self.model.predict(test)
        return self.label_names[result[0]]

