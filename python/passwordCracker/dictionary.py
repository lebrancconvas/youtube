from hashlib import sha512

class Dictionary():
    def hashing(self, password):
        return sha512(password.encode("utf8")).hexdigest()

    def loadFile(self, filename):
        encodings_to_try = ['utf-8', 'latin-1']
        for encodings in encodings_to_try:
            try:    
                with open(filename, "r", encoding=encodings) as fp:
                    comPass = [line.strip() for line in fp]
                return comPass
            except UnicodeDecodeError:
                print(f"Failed to open {filename} with {encodings}")

    def crackPass(self, filename, hashedpassword):
        attempts = 0
        comPass = self.loadFile(filename)
        print(comPass)
        for password in comPass:
            hashedComPassword = sha512(password.encode()).hexdigest()
            if hashedComPassword == hashedpassword:
                print(f"Password Found {password}")
                return True
            attempts += 1

if __name__ == "__main__":
    hashedPassword = Dictionary().hashing("hello") 
    Dictionary().crackPass("rockyou.txt", hashedPassword)
