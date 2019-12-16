import subprocess as con
import ip

def startBroker():
    p = con.Popen("mosquitto -v", cwd="C:\Program Files\mosquitto", shell=True)
    print(p)

def initBroker():
    ip.setDBIP('ipv4')
    startBroker()

#main
if __name__ == '__main__':
    #begin broker
    ip.setDBIP('ipv4')
    startBroker()
