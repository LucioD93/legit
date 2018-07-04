import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 8000

serversocket.bind((host, port))

serversocket.listen(5)

while(True):

    clientsocket, addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))

    file = 'f.txt'

    with open(file, "wb") as f:
        while True:
            data = clientsocket.recv(1024)
            if not data:
                print('Breaking from file write')
                break
            f.write(data)
            print('Wrote to file', data.decode('utf-8'))
        f.close()
        print('Received')
    clientsocket.close()