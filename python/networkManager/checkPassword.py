from subprocess import STDOUT, check_output, run, CalledProcessError

class CheckNetwork():
    def __init__(self, wifiName):
        self.wifiName = wifiName
        self.cons = []

    def isExist(self): #check if this is previously connected then return true
        stored = check_output(['nmcli', '-t', '-f', 'NAME,TYPE', 'con', 'show'], universal_newlines=True, stderr=STDOUT)
        self.cons = [line.split()[0] for line in stored.splitlines()]
        for con in self.cons:
            if "802-11-wireless" in con:
                left, right = con.split(":")
                if self.wifiName == left:
                    #print("Ok")
                    return True


    def isActive(self): 

        try:
            output = run(['nmcli', '-f', 'SSID,ACTIVE', 'dev', 'wifi', 'list'], capture_output=True, text=True, check=True)

            lines = output.stdout.strip().split('\n')
            for line in lines[1:]:
                columns = line.split()
                ssid = columns[0]
                active = columns[1]
                if active == 'yes':
                    if self.wifiName == ssid:
                        #print("True")
                        return True


        except CalledProcessError as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    CheckNetwork("a_5g").isActive()
    CheckNetwork("a_5g").isExist()
