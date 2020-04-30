import subprocess as con
from Helpers import ip
import sys

def startBroker():
    p = con.Popen("mosquitto -v", cwd="C:\Program Files\mosquitto", shell=True)
    print(p)

def startBrokerLinux():
    p = con.Popen("mosquitto -v", shell=True)
    print(p)

def initBroker():
    ip.setDBIP('ipv4')
    startBroker()

#main
if __name__ == '__main__':
    ipType = "linux"
    for i, arg in enumerate(sys.argv):
        if i == 1:
            if arg == "windows":
                ipType = "ipv4"
            else:
                ipType = "linux"
    #begin broker
    ip.setDBIP(ipType)
    if ipType == "ipv4":
        startBroker()
    else:
        startBrokerLinux()
