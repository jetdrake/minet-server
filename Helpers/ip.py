import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess as con

#globals
# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase/serviceAccountKey.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://magneticlocalization.firebaseio.com/'
})

def getIPv6():
    data = con.check_output("ipconfig", shell=True).decode()
    this = data.split('\r\n')
    ipv6list = list()
    for line in this:
        if 'IPv6 Address.' in line:
            #gets the 2 byte ones
            if len(line) > 70:
                #gets rid of the fixed length header
                ipv6list.append(line[39:])

    return ipv6list[0]

def getIPv4():
    data = con.check_output("ipconfig", shell=True).decode()
    this = data.split('\r\n')
    ipv4list = list()
    for line in this:
        if 'IPv4 Address.' in line:
            #print(line)
            #gets the first address of the correct length
            if len(line) > 50:
                #gets rid of the fixed length header
                ipv4list.append(line[39:])

    return ipv4list[0]

def getIPv4Linux():
    data = con.check_output("ifconfig", shell=True).decode()
    this = data.split('inet')
    ip = this[1].split(' ')[1]
    #print(ip)

    #set ip in the db
    #print(ip, useIP)
    ref = db.reference('/')
    ref.set({"ip":ip})

    return ip

def printIPv6():
    print(getIPv6()) 

def printIPv4():
    print(getIPv4())

def setDBIP(ip):
    useIP = ''
    if ip == 'ipv4':
        useIP = getIPv4()
    elif ip == 'ipv6':
        useIP = getIPv6()
    elif ip == 'linux':
        useIP = getIPv4Linux()
    else:
        print("can only be 'ipv4' or 'ipv6'")
    if not useIP:
        return
    else:
        #set ip in the db
        print(ip, useIP)
        ref = db.reference('/')
        ref.set({"ip":useIP})

if __name__ == '__main__':
    getIPv4Linux()