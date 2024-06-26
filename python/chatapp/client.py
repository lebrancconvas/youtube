import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client():
    def __init__(self, window, host, port):
        self.window = window

        self.messageBox = tk.Listbox(window, height=20, width=100, bg="#fc6c85")
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg="#fc6c85", fg="#000000")
        self.msgEntry.pack()

        self.button = tk.Button(window, text="Send", width=50, bg="#fc6c85", command=self.sendTexts)
        self.button.pack()


        #define hosts and port
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.sock.connect((self.host, self.port))

        Thread(target=self.recvTexts).start() 

        #we don't need extra functin since we won't apply any extra functionality.


    def sendTexts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))

    def recvTexts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                self.messageBox.insert(tk.END, msg)
            except OSError:
                break



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Simplest gui chatapp")
    Client(window, "localhost", 8000)
    try: 
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
