# Usage: python3 legitProxy.py ip_proxy_host
import socket, os, itertools, sys
import heapq

LOGFILE = 'log.txt'

k = 1
serverList = []
# fileServerList = {'file_name': [(priority, address, port)]}
fileServerList = dict()


def writeCommitInLog(filename, storageHost, storagePort):
    with open(LOGFILE, "a+") as f:
        f.write("Commit operation, file %s sended to storage server %s, port %s" %(filename, str(storageHost), str(storagePort)))
        f.write("\n")
        f.close()


def sendFileToStorage(filename, storageHost, storagePort):
    # storageHost = socket.gethostbyaddr(storageHost[0])[0]
    print('Trying to connect to')
    print(storageHost)
    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    storageSocket.connect((storageHost, int(storagePort)))
    # storageSocket.connect((socket.gethostname(), storagePort))
    print("Storage socket connected")
    storageSocket.send("Commit".encode("utf8"))

    response = storageSocket.recv(1024).decode("utf8")
    if response == "Ok":
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

def dropServerInServerList(host, port):
    for server in enumerate(serverList):
        if server[1] == host and server[2] == port:
            serverList.remove(server)

def addPriorityServerInServerList(host, port):
    for i, server in enumerate(serverList):
        if server[1] == host and server[2] == port:
            serverList[i] = (server[0] + 1, host, port)
            return None

def processFile(file):
    if file in fileServerList:
        servers = fileServerList[file]
    else:
        servers = heapq.nsmallest(k+1, serverList)
        for i, s in enumerate(servers):
            addPriorityServerInServerList(s[1], s[2])
            servers[i] = (0, s[1], s[2])

    print('Save in servers')
    print(servers)

    for s in servers:
        # Esto se convertira en hilos
        sendFileToStorage(file, s[1], s[2])

    fileServerList[file] = servers

    print('all servers')
    print(serverList)
    print('-------')


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


def registerNewStorageServer(clientSocket, newServerAddr):
    clientSocket.send("Ok".encode("utf8"))
    print('Register new server')
    print(newServerAddr[0])
    newServerPort = int(clientSocket.recv(1024).decode("utf8"))
    print(newServerPort)
    # Registrar nuevo servidor con newServerAddr y newServerPort
    heapq.heappush(serverList, (0, newServerAddr[0], newServerPort))

def updateOperation(clientSocket, clientAddr, option):
    clientSocket.send("Ok".encode("utf8"))
    file = clientSocket.recv(1024).decode("utf8")
    print('Update file')
    print(file)
    if file not in fileServerList:
        clientSocket.send("Error".encode("utf8"))
        return 1

    print('Posible update servers')
    print(fileServerList[file])

    server = heapq.heappop(fileServerList[file])
    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            storageSocket.connect((server[1], server[2]))
            # storageSocket.connect((socket.gethostname(), server[2]))
            break
        except:
            print('Servidor caido: ' + server[1] + ' ' + str(server[2]))
            dropServerInServerList(server[1], server[2])
            if len(fileServerList[file]) == 0:
                print('Error: no more servers')
                clientSocket.send("Error".encode("utf8"))
                return 1
            server = heapq.heappop(fileServerList[file])

    print('Final update server')
    print(server)

    storageSocket.send(option.encode("utf8"))

    response = storageSocket.recv(1024).decode("utf8")
    if response == "Ok":
        clientSocket.send("Ok".encode("utf8"))
        storageSocket.send(clientAddr.encode("utf8"))
    
    heapq.heappush(fileServerList[file], server)
    clientSocket.close()
    storageSocket.close()


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]
port = 8000

serverSocket.bind((host, port))

serverSocket.listen(5)

while(True):

    clientSocket, addr = serverSocket.accept()
    print("Got a connection from %s" % str(addr))

    option = clientSocket.recv(1024).decode("utf8")

    if option == "Commit":
        commitOperation(clientSocket)

    if option == "NewServer":
        registerNewStorageServer(clientSocket, addr)

    if option == "Update":
        updateOperation(clientSocket, addr[0], "Update")

    if option == "Checkout":
        updateOperation(clientSocket, addr[0], "Checkout")
