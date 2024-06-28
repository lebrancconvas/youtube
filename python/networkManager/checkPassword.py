from subprocess import STDOUT, check_output

class CheckNetwork():
    def __init__(self, wifiName):
        self.wifiName = wifiName
        self.cons = [] #we'll store the stored network here

    def isExist(self):
        stored = check_output(['nmcli', '-t', '-f', 'NAME,TYPE', 'con', 'show'], universal_newlines=True, stderr=STDOUT) #to return no output in terminal 
        self.cons = [line.split()[0] for line in stored.splitlines()]
        for con in self.cons:
            if "802-11-wireless" in con:
                left, right = con.split(":")
                if self.wifiName == left:
                    return True


if __name__ == "__main__":
    CheckNetwork("wifiname").isExist() # just for testing, you should one your ssid
