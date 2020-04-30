import paho.mqtt.client as mqtt
import json, sys
from Helpers import ip, testlogger
from Models import MapFilter
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase/serviceAccountKey.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://magneticlocalization.firebaseio.com/'
}, name="client")

# takes a mqtt client and a particle filter and attempts localization.
class Localize(mqtt.Client):
    def __init__ (self, useMap):
        super().__init__()
        self.pf = MapFilter.MapFilter(useMap)
        self.tl = testlogger.logger("exp1")

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))
        
    def on_message(self, mqttc, obj, msg):
        try:
            print(msg.topic, str(msg.qos), str(msg.payload))
            if msg.topic == "realtime":
                msg = msg.payload.decode('UTF-8')
                point = json.loads(msg)
                #print(point)
                pose = point['direction']
                realdata = [float(point['x']), float(point['y']), float(point['z'])]
                if realdata is not None:
                    self.pf.update(np.array(realdata, dtype=float), pose)
                    state = self.pf.getMostPopularState()
                    print(state)
                    self.tl.append(str(state[0]))
                    self.publish("result", str(state[0]))
            elif msg.topic == "connect":
                mp = self.pf.getMapForPublish()
                mp = json.dumps(mp)
                self.tl.append("connected")
                self.publish("map", str(mp))
                print(mp)
        except Exception as e:
            print('error:',e)
        

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))
        self.tl.append(str(mid))

    def run(self):
        ref = db.reference('/')
        data = ref.get("ip", None)
        ipaddr = data[0]['ip']
        # rr.getAccuracy()
        self.connect(ipaddr, 1883, 60)
        self.subscribe("realtime", 0)
        self.subscribe("connect", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


if __name__ == '__main__':
    useMap = "project"
    for i, arg in enumerate(sys.argv):
        if i == 1:
            useMap = arg
            
    mqttc = Localize(useMap=useMap)
    rc = mqttc.run()

    print("rc: "+str(rc))
