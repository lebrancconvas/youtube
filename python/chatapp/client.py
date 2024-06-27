import tkinter as tk 
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client():
    def __init__(self, window, host, port):
        self.window = window
        #define tk inter

        self.messageBox = tk.Listbox(window, height=20, width=100, bg="#fc6c85")
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg="#fc6c85", fg="#000000")
        self.msgEntry.pack()

        self.button = tk.Button(window, text="Send Text", width=50, bg="#fc6c85", command=self.sendTexts) # yet to implement
        self.button.pack()

        self.host = host
        self.port = port
        self.buffer = 1024
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        Thread(target=self.recvTexts).start() #we'll implement self.recvTexts later

    def recvTexts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                self.messageBox.insert(tk.END, msg)
            except OSError:
                break


    def sendTexts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Simples chat app in tkinter")
    Client(window, "localhost", 8000)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
