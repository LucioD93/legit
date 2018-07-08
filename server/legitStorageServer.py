import socket, os, sys

def main(argv):

    storageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = int(argv[1])

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