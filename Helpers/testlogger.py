import datetime
class logger:
    def __init__(self, name="test"):
        self.file = open("logs/"+name+ "_log_" + str(datetime.datetime.now()),"w+")
    
    def append(self, data):
        self.file.write(data+"\n")