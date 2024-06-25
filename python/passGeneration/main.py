from random import sample
import tkinter as tk
from file import hashGeneration
from os import getcwd
from tkinter import messagebox as msgbox



class passwordGenertion():
    def __init__(self, window):
        self.window = window
        #match password
        self.label = tk.Label(window, text="Enter password:")
        self.label.pack()

        self.passEntry = tk.Entry(window, width=10)
        self.passEntry.pack() 

        self.button = tk.Button(self.window, text="Submit", command=self.checkPassword)
        self.button.pack(pady=10)

        self.show_matched_pass = tk.Label(window)
        self.show_matched_pass.pack()
        
        #show password 
        self.label = tk.Label(window, text="Enter lenght of password:")
        self.label.pack()

        self.entry = tk.Entry(window, width=10)
        self.entry.pack() 

        self.button = tk.Button(self.window, text="Submit", command=self.generate)
        self.button.pack(pady=10)
        
        self.show_pass = tk.Label(window)
        self.show_pass.pack()


    def generate(self):
        charList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
        entry_value = self.entry.get().strip()
        if entry_value is None:
            self.show("No value given")
        else:
            password = "".join(sample(charList, int(entry_value)))
            print(password)
            self.show(password)
            app = hashGeneration(file=f"{getcwd()}/hashed.txt")
            app.writeHash(password)
    
    
    def show(self, text):
        self.show_pass.config(text=text, fg='#fc6c85')


    def checkPassword(self):
        entry_value = self.passEntry.get().strip()
        if entry_value is not None:
            app = hashGeneration(file=f"{getcwd()}/hashed.txt")
            if app.matchHash(entry_value):
                print("It's matched")
                self.showMatched("Correct Password")
            else:
                self.showMatched("Wrong Password")
        else:
            msgbox.showerror("Ran into some fucked up error")
    
    def showMatched(self, text):
        self.show_matched_pass.config(text=text, fg="#fc6c85")


    


        
if __name__ == "__main__":
    window = tk.Tk()
    e1 = tk.Entry(window)
    window.title("Password Generator")
    app = passwordGenertion(window)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
