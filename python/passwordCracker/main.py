from itertools import product
from hashlib import sha512
from string import printable
from dictionary import Dictionary

class Passowrd():
    def hashPassword(self, password):
        return sha512(password.encode()).hexdigest()

    def bruteForce(self, hashedPassowrd):
        characters = printable #we could also do this 
        #character = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"\#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        # but see the other characters make it hard, instead use the library


        # this is the cracking part
        attempts = 0
        
        for i in range(1, 13): #for password in length 8 after this lenth it becomes hard for bruteforce 
            for j in product(characters, repeat=i): #i is the length of passwords
                j = "".join(j) # j is attempt count 
                hashed = self.hashPassword(j)
                if hashed == hashedPassowrd:
                    print(f"paassowrd cracked {j}")
                    return j 
                attempts += 1
                if attempts % 100000000000 == 0:
                    print("Fuck this is hard, still trying.")
        print("Passowrd not found, damnit.")
        return None

if __name__ == "__main__":
    hashedPassword = Passowrd().hashPassword("aabb")
    if Dictionary().crackPass("rockyou.txt", hashedPassword):
        quit()
    else:
        Passowrd().bruteForce(hashedPassword)
