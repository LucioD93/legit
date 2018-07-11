import socket, os, itertools
import heapq

LOGFILE = 'log.txt'

k = 4
serverList = []
fileServerList = dict()


def incrementFilename(filename):
    filename, extension = os.path.splitext(filename)
    n = 1
    yield filename + extension
    for n in itertools.count(start=1, step=1):
        yield '%s%d%s' % (filename, n, extension)

def createFileName(originalFilename):
    print('Create file name')
    for filename in incrementFilename(originalFilename):
        if not os.path.isfile(filename):
            return filename

def writeCommitInLog(filename, storageHost, storagePort):
    with open(LOGFILE, "a+") as f:
        f.write("Commit operation, file %s sended to storage server %s, port %s" %(filename, str(storageHost), str(storagePort)))
        f.write("\n")
        f.close()

def sendFileToStorage(filename, storageHost=socket.gethostname(), storagePort=8001):
    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    storageSocket.connect((storageHost, storagePort))
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

def commitOperation(clientSocket):
    print('Commit')
    clientSocket.send("Ok".encode("utf8"))
    file = clientSocket.recv(1024).decode("utf8")
    print("Filename: %s" % file)

    # Sobrenombrar archivo
    file = createFileName(file)
    print('file renamed')
    clientSocket.send("Ok".encode("utf8"))

    with open(file, "wb") as f:
        while True:
            data = clientSocket.recv(1024)
            if not data:
                print('Breaking from file write')
                break
            f.write(data)
            # print('Wrote to file', data.decode('utf-8'))
        f.close()
        print('Received')
    clientSocket.close()

    # Enviar el archivo a los servidores
    sendFileToStorage(file)

def registerNewStorageServer(clientSocket, newServerAddr):
    clientSocket.send("Ok".encode("utf8"))
    print('Register new server')
    newServerPort = clientSocket.recv(1024).decode("utf8")

    # Registrar nuevo servidor con newServerAddr y newServerPort
    print(str(newServerAddr[0]) + " " + newServerPort)
    heapq.heappush(serverList, (0, str(newServerAddr[0]), newServerPort))


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
        registerNewStorageServer(clientSocket, addr)