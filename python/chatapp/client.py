import tkinter as tk 
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Client():
    def __init__(self,window, host, port):

        self.window = window

        self.messageBox = tk.Listbox(window, height=20, width=100, bg="#e75480")
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg="#f5f5dc", fg="#0F0F0F")
        self.msgEntry.pack()

        self.button = tk.Button(window, text="Send", width=50,bg="#E75480", command=self.sendTexts)
        self.button.pack()


        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.sock.connect((self.host, self.port))

        Thread(target=self.recvTexts).start()

    
    def sendTexts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))

    def recvTexts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                #print(msg)
                self.messageBox.insert(tk.END, msg)
            except OSError:
                break


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chat app")
    Client(window, "localhost", 8000)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()

