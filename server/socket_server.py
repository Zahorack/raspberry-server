import socket

s = socket.socket()
s.bind(('0.0.0.0', 54321))
s.listen(5)

while True:
    client, addr = s.accept()

    while True:
        content = client.recv(32)

        if len(content) == 0:
            break
        else:
            print(content)

    print("closing connection")
    client.close()