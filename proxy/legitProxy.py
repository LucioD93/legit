import socket, os, itertools
import heapq

LOGFILE = 'log.txt'

k = 4
serverList = []
fileServerList = dict()

def writeCommitInLog(filename, storageHost, storagePort):
    with open(LOGFILE, "a+") as f:
        f.write("Commit operation, file %s sended to storage server %s, port %s" %(filename, str(storageHost), str(storagePort)))
        f.write("\n")
        f.close()

def sendFileToStorage(filename, storageHost, storagePort):
    storageHost = socket.gethostbyaddr(storageHost)[0]
    # storageHost = 'edgar-Aspire-ES1-572'
    print('Trying to connect to')
    print(storageHost)
    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    storageSocket.connect((storageHost, int(storagePort)))
    print("Storage socket connected")
    storageSocket.send(filename.encode("utf8"))

    response = storageSocket.recv(1024).decode("utf8")
    if response == "Ok":
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                storageSocket.send(data)
                if not data:
                    break
            f.close()
            print("File %s sended" % filename)

    storageSocket.close()

    # Escribir la operacion en el log
    writeCommitInLog(filename, storageHost, storagePort)

def processFile(file):
    if file in fileServerList:
        servers = fileServerList[file]
    else:
        servers = heapq.nsmallest(k+1, serverList)

    print('Save in servers')
    print(servers)

    for s in servers:
        # s[0] = s[0]+1
        # Esto se convertira en hilos
        sendFileToStorage(file, s[1], s[2])

def commitOperation(clientSocket):
    print('Commit')
    clientSocket.send("Ok".encode("utf8"))
    file = clientSocket.recv(1024).decode("utf8")
    print("Filename: %s" % file)

    # Sobrenombrar archivo
    clientSocket.send("Ok".encode("utf8"))

    with open(file, "wb") as f:
        while True:
            data = clientSocket.recv(1024)
            if not data:
                print('Breaking from file write')
                break
            f.write(data)
        f.close()
        print('Received')
    clientSocket.close()

    # Enviar el archivo a los servidores
    processFile(file)

def registerNewStorageServer(clientSocket):
    clientSocket.send("Ok".encode("utf8"))
    print('Register new server')
    newServerAddr = clientSocket.recv(1024).decode("utf8")
    newServerPort = clientSocket.recv(1024).decode("utf8")

    # Registrar nuevo servidor con newServerAddr y newServerPort
    print(newServerAddr + " " + newServerPort)
    heapq.heappush(serverList, (0, newServerAddr, newServerPort))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 8000

serverSocket.bind((host, port))

serverSocket.listen(5)

while(True):

    clientSocket, addr = serverSocket.accept()
    print("Got a connection from %s" % str(addr))

    option = clientSocket.recv(1024).decode("utf8")
    print(option)

    if option == "Commit":
        commitOperation(clientSocket)

    if option == "NewServer":
        registerNewStorageServer(clientSocket)