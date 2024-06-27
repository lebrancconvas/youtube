from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.client = {}
        self.addrs = {}

    def serverStart(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("We're connected master >_< ")

        #let's get it started

        while True: 
            try:
                cliSock, cliAddr = self.sock.accept()
                print(f"Con received from {cliAddr}")

                self.client[cliSock] = cliAddr #to make multiple clients join the server and register in the client dict
                self.addrs[cliAddr] = cliSock
        
                Thread(target=self.handling, args=(cliSock,)).start()
            except Exception as e:
                print(f"{e} Con closed")

    # to messages and display them in terminal    
    def handling(self, cliSock):
        while True:
            msg = cliSock.recv(self.buffer).decode("utf8")
            print(cliSock)
            if msg:
                print(f"{msg} received.")
                self.sendTexts(msg)
    

    def sendTexts(self, msg):
        for socket in self.client:
            try:
                socket.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)



if __name__ == "__main__":
    try:
        Server("localhost", 8000).serverStart()
    except KeyboardInterrupt:
        print("Closed Con")
