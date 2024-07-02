from itertools import product
from hashlib import sha512
from string import printable
from dictionary import Dictionary

class Password():
    def hashPassword(self, password):
        return sha512(password.encode()).hexdigest()

    def bruteForce(self, hashedPassword):
        characters = printable #we could also type all the characters
        #characters = "abchdofsooisjfj{}sdfsdfj""'dsf" # like this, but we can use the library

        attempts = 0
        
        for i in range(1, 9): #check password hashed in range of 1 to 13
            for j in product(characters, repeat=i):
                j = "".join(j)
                hashed = self.hashPassword(j)
                if hashed == hashedPassword:
                    print(f"Password cracked {j}")
                    return j
                attempts += 1
                if attempts % 1000000 == 0: #after this many check if not found it'll show a text
                    print(f"Fuck this, trying hard. wait {attempts}")
        print("Password could not be cracked, sorry")
        return None

if __name__ == "__main__":
    hashedPassword = Password().hashPassword("me12")
    if Dictionary().checkForPassword("pass.txt", hashedPassword):
        quit()
    else:
        Password().bruteForce(hashedPassword) # let's do easy password for demostration, hard ones will take long time
