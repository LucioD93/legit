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
        proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.host == None:
            self.host = '192.168.1.122'
        proxySocket.connect((self.host, self.port))

        proxySocket.send("Commit".encode("utf8"))

        answer = proxySocket.recv(1024).decode("utf8")
        
        if answer == "Ok":
            proxySocket.send(file.encode("utf8"))
            response = proxySocket.recv(1024).decode("utf8")
            if response == "Ok":
                with open(file, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        proxySocket.send(data)
                        if not data:
                            break
                    f.close()
                print("File %s sended" % file)
            proxySocket.close()