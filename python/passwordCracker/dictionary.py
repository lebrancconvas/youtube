from hashlib import sha512

class Dictionary():
    def hashing(self, password):
        return sha512(password.encode()).hexdigest()

    def loadFile(self, fileName):
        encodings = ['utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open(fileName, "r", encoding=encoding) as fp:
                    comPass = [line.strip() for line in fp]
                return comPass #returns the list of the password in dictionary format
            except UnicodeDecodeError:
                print(f"Couldn't open file in {encoding}")

    def checkForPassword(self, fileName, hashedPassword):
        attempts = 0
        comPass = self.loadFile(fileName)
        for password in comPass:
            hashedComPassword = self.hashing(password)
            if hashedComPassword == hashedPassword:
                print(f"Password Found {password}")
                return True
        attempts += 1


if __name__ == "__main__":
    hashedPassword = Dictionary().hashing("helloworld")
    Dictionary().checkForPassword("pass.txt", hashedPassword)
