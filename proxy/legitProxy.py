import socket, os, itertools

LOGFILE = 'log.txt'

def incrementFilename(filename):
    filename, extension = os.path.splitext(filename)
    n = 1
    yield filename + extension
    for n in itertools.count(start=1, step=1):
        yield '%s%d%s' % (filename, n, extension)

def createFileName(originalFilename):
    for filename in incrementFilename(originalFilename):
        if not os.path.isfile(filename):
            return filename

def writeCommitInLog(filename, storageHost, storagePort):
    with open(LOGFILE, "a+") as f:
        f.write("Commit operation, file %s sended to storage server %s, port %s" %(filename, str(storageHost), str(storagePort)))
        f.close()

def sendFileToStorage(filename, storageHost=socket.gethostname(), storagePort=8001):
    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    storageSocket.connect((storageHost, storagePort))
    print("Storage socket connected")
    storageSocket.send(filename)

    response = storageSocket.recv(1024).decode("utf8")
    if response == "Ok":
        with open(file, 'rb') as f:
            while True:
                data = f.read(1024)
                storageSocket.send(data)
                if not data:
                    break
            f.close()
            print("File %s sended" % file)

    storageSocket.close()
    # Escribir la operacion en el log
    writeCommitInLog(filename, storageHost, storagePort)

    

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 8000

serverSocket.bind((host, port))

serverSocket.listen(5)

while(True):

    clientSocket, addr = serverSocket.accept()
    print("Got a connection from %s" % str(addr))

    file = clientSocket.recv(1024).decode("utf8")
    print("Filename: %s" % file)
    # Sobrenombrar archivo
    file = createFileName(file)
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
