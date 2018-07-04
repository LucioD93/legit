import socket, threading, os, sys

class Commit():
    files = None
    host = None
    port = 8000

    def __init__(self, files, host):
        if files != []:
            self.files = files
            if host != None:
                self.host = host
            for file in self.files:
                self.sendFile(file)
        else:
            print('Can not commit nothing!')
            sys.exit(1)
    
    def printFiles(self):
        for i in self.files:
            print(i)
    
    def sendFile(self, file):
        commitSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        commitSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.host == None:
            self.host = socket.gethostname()
        commitSocket.connect((self.host, self.port))

        with open(file, 'rb') as f:
            while True:
                data = f.read(1024)
                commitSocket.send(data)
                if not data:
                    break
            f.close
        commitSocket.close()