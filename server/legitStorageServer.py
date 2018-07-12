import socket, os, sys

def main(argv):

    proxyAddress = socket.gethostname()
    proxyPort = 8000

    proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxySocket.connect((proxyAddress, proxyPort))

    proxySocket.send("NewServer".encode("utf8"))

    response = proxySocket.recv(1024).decode("utf8")

    if response == "Ok":
        proxySocket.send(socket.gethostname().encode("utf8"))
        proxySocket.send((str(argv[1]).encode("utf8")))
    proxySocket.close()

    # 

    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = int(argv[1])

    print('host')
    print(host)

    storageSocket.bind((host, port))
    storageSocket.listen(5)

    while True:
        proxySocket, addr = storageSocket.accept()
        print("Got a connection from %s" % str(addr))

        file = proxySocket.recv(1024).decode("utf8")
        print("File to store: %s" % file)

        proxySocket.send("Ok".encode("utf8"))
        with open(file, "wb") as f:
            while True:
                data = proxySocket.recv(1024)
                if not data:
                    print("File %s writing finish" % file)
                    break
                f.write(data)

        proxySocket.close()


if __name__ == '__main__':
    main(sys.argv)