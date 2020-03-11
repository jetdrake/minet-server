import paho.mqtt.client as mqtt
import json
from Helpers import ip
from Models import MapFilter
import numpy as np

'''
rr = classifier.classifier()
    def on_message(self, mqttc, obj, msg):
        try:
            msg = msg.payload.decode('UTF-8')
            point = json.loads(msg)
            #print(point)
            print(rr.predictRawPoint(point))
        except Exception as e:
            print(e)
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
'''
'''
    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)
'''

# takes a mqtt client and a particle filter and attempts localization.
class Localize(mqtt.Client):
    pf = MapFilter.MapFilter()

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        try:
            msg = msg.payload.decode('UTF-8')
            point = json.loads(msg)
            #print(point)
            #pose = [point['direction'], point['stepId']]
            realdata = [float(point['x']), float(point['y']), float(point['z'])]
            if realdata is not None:
                self.pf.update(np.array(realdata, dtype=float))
                self.publish("result", self.pf.getMostPopularState())
        except Exception as e:
            print('error:',e)
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def run(self):
        ipaddr = ip.getIPv4Linux()
        # rr.getAccuracy()
        self.connect(ipaddr, 1883, 60)
        self.subscribe("realtime", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = Localize()
rc = mqttc.run()

print("rc: "+str(rc))
