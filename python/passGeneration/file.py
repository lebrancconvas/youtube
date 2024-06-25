from hashlib import sha512 as h
from os import getcwd

class hashGeneration():
    def __init__(self, file):
        self.filename = file


    def writeHash(self, password):
        if password is not None:
            hashedPassword = h(password.encode()).hexdigest()
            try: 
                with open(self.filename, "a") as f:
                    f.write(f"1. {hashedPassword}\n")
            except Exception as e:
                print(e)
    

    def matchHash(self, askPass):
        if askPass is not None:
            try:
                with open(self.filename, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.find(h(askPass.encode()).hexdigest()) != -1:
                            return True
            except FileNotFoundError:
                print("File not found lol.")

if __name__ == "__main__":
    app = hashGeneration(file=f"{getcwd()}/hashed.txt")
    app.matchHash("This is a password") #testing if this working
