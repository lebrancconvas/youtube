from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread 

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.clients = {}
        self.addrs = {}

    
    def serverStart(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            print("We're connected master >_< -w-")

        except OSError:
            print("Please close previous connection first.")
    
        while True: #this recieves clients
            try:
                cliSock, cliAddr = self.sock.accept()
                print(f"Connection from {cliAddr}")

        #add the client details in the arrays

                self.clients[cliSock] = cliAddr
                self.addrs[cliAddr] = cliSock

        #start a thread to keep recieving clients

                Thread(target=self.handling, args=(cliSock,)).start()
            except Exception as e:
                print(e)
    
    def handling(self, cliSock):
        while True:
            try:
                msg = cliSock.recv(self.buffer).decode("utf8")
                if msg:
                    ip, port = self.clients[cliSock]
                    print(f"{msg} Recived from {port}")
                    self.sendTexts(msg)
            except Exception as e:
                print(e)

    

    def sendTexts(self, msg):
        for socket in self.clients:
            try:
                socket.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)




if __name__ == "__main__":
    try:
        Server("localhost", 8000).serverStart()
    except KeyboardInterrupt:
        print("Connection closed")

