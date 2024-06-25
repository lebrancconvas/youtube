import tkinter as tk 
from random import sample
from file import hashGeneration
from os import getcwd


class passwordGeneration():
    def __init__(self, window):
        self.window = window

        #show password
        self.label = tk.Label(window, text="Enter Password lenght")
        self.label.pack()

        self.entry = tk.Entry(window, width=10) #you can change the width
        self.entry.pack()


        self.button = tk.Button(self.window, text="Submit", command=self.generate)
        self.button.pack(padx=10, pady=10)

        #show here

        self.show_pass = tk.Label(window)
        self.show_pass.pack()

        #check for password

        self.label = tk.Label(window, text="Enter Password")
        self.label.pack()

        self.passEntry = tk.Entry(window, width=10) #you can change the width
        self.passEntry.pack()


        self.button = tk.Button(self.window, text="Submit", command=self.checkPassword)
        self.button.pack(padx=10, pady=10)




    def generate(self):
        charList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
        entryValue = self.entry.get().strip()
        if entryValue is None:
            self.show("No value is provided")
        else:
            password = "".join(sample(charList, int(entryValue)))
            print(password)
            self.show(password)
            app = hashGeneration(file=f"{getcwd()}/hashed.txt")
            app.writeHash(password)
    

    def checkPassword(self):
        entryValue = self.passEntry.get().strip()
        if entryValue is not None:
            app = hashGeneration(file=f"{getcwd()}/hashed.txt")
            if app.matchHash(entryValue):
                self.show("Match found in database.")
            else:
                self.show("It's a wrong password, not found")
        else:
            self.show("Ran into some fucked up problem. Please a password to match.")



    def show(self, text):
        self.show_pass.config(text=text, fg="#ff77ff")



if __name__ == "__main__":
    window = tk.Tk()
    entry1 = tk.Entry(window)
    window.title("Password generator")
    app = passwordGeneration(window)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
