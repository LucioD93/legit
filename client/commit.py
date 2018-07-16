import socket, threading, os, sys


class Commit():
    files = None
    local = '192.168.43.178'
    host = '192.168.43.4'
    # host = socket.gethostname()
    port = 8000

    def __init__(self, files, host):
        if files != []:
            self.files = files
            if host != None:
                self.host = host
        else:
            print('Can not commit nothing!')
            sys.exit(1)

    def printFiles(self):
        for i in self.files:
            print(i)

    def sendAllFiles(self):
        for file in self.files:
                self.sendFile(file)

    def sendFile(self, file):
        if not os.path.isfile(file):
            print("El archivo no existe.")
            exit(0)

        proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    
    def updateOperation(self, file, option):
        proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxySocket.connect((self.host, self.port))

        proxySocket.send(option.encode("utf8"))

        answer = proxySocket.recv(1024).decode("utf8")

        if answer == "Ok":
            proxySocket.send(file.encode("utf8"))
            answer = proxySocket.recv(1024).decode("utf8")
            if answer == "Ok":
                storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                storageSocket.bind((self.local, 8009))
                # storageSocket.bind(('192.168.43.4', 8009))
                storageSocket.listen(1)

                storage, addr = storageSocket.accept()
                print("Storage connected")
                print("Asking for file")
                print(file)
                storage.send(file.encode("utf8"))
                print('Filename sended')
                with open(file, 'wb') as f:
                    while True:
                        data = storage.recv(1024)
                        if not data:
                            break
                        f.write(data)
                    f.close()

                storage.close()

            elif answer == "Error":
                print("No se pudo realizar update")
                sys.exit()