import socket, os, sys, itertools

def commitOperation(proxySocket):
    proxySocket.send("Ok".encode("utf8"))

    file = proxySocket.recv(1024).decode("utf8")
    print("File to store: %s" % file)

    if os.path.isfile(file):
        oldFileName, extension = os.path.splitext(file)
        print('newfilename')
        print("%s_old%s" % (oldFileName, extension))
        os.rename(file, "%s_old%s" % (oldFileName, extension))

    proxySocket.send("Ok".encode("utf8"))
    with open(file, "wb") as f:
        while True:
            data = proxySocket.recv(1024)
            if not data:
                print("File %s writing finish" % file)
                break
            f.write(data)

    proxySocket.close()

def updateOperation(proxySocket):
    proxySocket.send("Ok".encode("utf8"))

    client = proxySocket.recv(1024).decode("utf8")

    print("Client")
    print(client)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((client, 7999))

    print("Connected to client")

    clientSocket.close()

    proxySocket.close()

def main(argv):
    # proxyAddress = socket.gethostname()
    proxyAddress = '192.168.1.122'
    proxyPort = 8000

    proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxySocket.connect((proxyAddress, proxyPort))

    proxySocket.send("NewServer".encode("utf8"))

    response = proxySocket.recv(1024).decode("utf8")

    if response == "Ok":
        # proxySocket.send(socket.gethostname().encode("utf8"))
        proxySocket.send((str(argv[1]).encode("utf8")))
    proxySocket.close()

    # 

    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host = socket.gethostname()
    host = '192.168.1.122'
    port = int(argv[1])

    print('host')
    print(host)

    storageSocket.bind((host, port))
    storageSocket.listen(5)

    while True:
        proxySocket, addr = storageSocket.accept()
        print("Got a connection from %s" % str(addr))

        option = proxySocket.recv(1024).decode("utf8")

        if option == "Commit":
            print('Commit')
            commitOperation(proxySocket)
        
        if option == "Update":
            print('Update')
            updateOperation(proxySocket)


if __name__ == '__main__':
    main(sys.argv)