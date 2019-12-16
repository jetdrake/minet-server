# minet-server
The desktop portion of minet

--The firebase json files have been omitted for security

Main:
  broker.py - begins the broker and puts the current ip address into firebase
  Client.py - the eclipse paho mqtt client that subscribes to the app
    -currently does basic Room Recognition with a trained classifier
  mapper.py - creates a map array from a list of dictionary objects - can be used to make figures

Helpers:
  classifier.py - contains the code to train a classifier for magnetic data and return a room
  ip.py - accesses the computers ip and stores it in firebase
  dataProcessor.py - used by classifier.py to get data in the correct format to be trained
  figure.py - creates a heatmap or other figures from a map array

In Testing:
  cluster.py - a non-working branch that with cluster data based on similarity
  test.py - just a blank script I use sometimes
  testclassifer.ipynb - mispelled and used to test the classifier code
  
requirements.txt - has all the venv info


