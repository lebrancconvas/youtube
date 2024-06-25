from hashlib import sha512 as h

class hashGeneration():
    def __init__(self, file):
        self.filename = file

    def writeHash(self, password):
        if password is not None:
            hashedPassword = h(password.encode()).hexdigest()
            try:
                with open(self.filename, "a") as file: 
                    file.write(f"1. {hashedPassword}\n")
            except Exception as e:
                print(e)
    def matchHash(self, askPass):
        if askPass is not None:
            try:
                with open(self.filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines: 
                        if line.find(h(askPass.encode()).hexdigest()) != -1: 
                            return True
            except FileNotFoundError:
                print("No password file. Please generate a password first.")
        #print(h(askPass.encode()).hexdigest()) 
if __name__ == "__main__":
    app = hashGeneration(file="/home/yoru/Projects/python/demo/learn/hashed.txt")
    app.matchHash("RX3n1eZY)otfpMBigr8u")


        
    
