from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.clients = {} # to have multiple clients and list them here
        self.addrs = {} # same as above

    #starting the server and accepting the clients
    def serverStart(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        print("We're ready master >_< ")

        while True:
            try:
                cliSock, cliAddr = self.sock.accept()
                print(f"Connection from {cliAddr}")

                self.clients[cliSock] = cliAddr # adding all the clients to self.clients arrays
                self.addrs[cliAddr] = cliSock

                Thread(target=self.handling, args=(cliSock,)).start()
            except Exception as e:
                print(e)


    #function to receieve texts and display them in the terminal
    def handling(self, cliSock):
        while True:
            try:
                msg = cliSock.recv(self.buffer).decode("utf8")
                ip, port = self.clients[cliSock] 
                if msg:
                    print(f"{msg} recieved from {port}")
                    self.sendText(msg)
            except Exception as e:
                print(e)

    def sendText(self, msg):
        for socket in self.clients:
            try:
                socket.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    try:
        Server("localhost", 8000).serverStart()
    except KeyboardInterrupt:
        print("Closed Connection.")
