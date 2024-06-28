from curses import echo, noecho, use_default_colors, wrapper, curs_set #you don't need more than these 
from subprocess import DEVNULL, check_output, run
from checkPassword import CheckNetwork


class Curses():
    def __init__(self, stdscr, message):
        self.stdscr = stdscr
        self.message = message
        curs_set(0)
        self.stdscr.clear()
        self.stdscr.refresh()
        self.wifi = []

    def showNetworks(self):
        heading = "|_____Available Networks_____|"

        maxy, maxx = self.stdscr.getmaxyx() #getting the max terminal x and y conordinates
        centerX = (maxx // 2) - (len(heading) // 2)
        self.stdscr.clear()
        self.stdscr.addstr(0, (maxx // 2) - (len(self.message)), self.message)
        self.stdscr.refresh() #without refreshing it won't show
        self.stdscr.addstr(2, centerX, heading)
        #list all the available networks with nmcli since this is available in most linux distro
        conlist = check_output(['nmcli', '-f', 'SSID', 'dev', 'wifi', 'list'], universal_newlines=True) #universal new lines use the /n
        self.wifi = [line.split()[0] for line in conlist.splitlines()[1:]]
        
        for idx, network in enumerate(self.wifi):
            self.stdscr.addstr(idx + 4, centerX, f"{idx + 1}. {network}")

        self.stdscr.addstr(len(self.wifi) + 5, centerX, "Choose Your Network: ")
        self.stdscr.refresh() #never forget to refresh after a new input

        while True:
            try:
                select = self.stdscr.getch() - ord('1')
                self.connect(select)
            except KeyboardInterrupt:
                self.stdscr.clear()
                self.stdscr.addstr((maxy // 2), centerX, "Program Ended, press q to close.")
                break


    def connect(self, select):
        heading = "|_____Program Closed_____|"

        maxy, maxx = self.stdscr.getmaxyx()
        centerX = (maxx // 2) - (len(heading) // 2)
        if 0 <= select <= len(self.wifi): #take input in range of 0 to the max numbers of wifi
            wifiName = self.wifi[select]
            echo()

            #for later we need to create new file
            if self.checkPreviousPassword(wifiName):
                self.stdscr.refresh()
                self.stdscr.clear()
                self.stdscr.addstr(len(self.wifi) + 6, centerX, f"Connected to {wifiName}. Press q to quit.")
                self.stdscr.refresh()
                if self.stdscr.getch() == ord('q'): quit()
        
            else:
                self.stdscr.refresh()
                self.stdscr.addstr(len(self.wifi) + 6, centerX, "Enter password: ") # prompt for the password
                self.stdscr.refresh()
                password = self.stdscr.getstr().decode("utf8") #get the inputted password
                noecho()
                self.connectToWifi(wifiName, password)
                self.stdscr.clear()
                self.stdscr.addstr(len(self.wifi) + 8, centerX, f'Connected to {wifiName}')
                self.stdscr.refresh()
                self.stdscr.getch() #wait for user input to close
        else:
            self.stdscr.addstr(len(self.wifi) + 8, centerX, "Invalid network selection, quit and restart again")
            self.stdscr.refresh()
            self.stdscr.getch()

    def checkPreviousPassword(self, wifiName):
        if CheckNetwork(wifiName).isExist():
            run(['nmcli', 'con', 'up', wifiName], stdout=DEVNULL)
            return True




    def connectToWifi(self, wifiName, password):
        try:
            run(['nmcli', 'dev', 'wifi', 'connect', wifiName, 'password', password], check=True, stdout=DEVNULL) #devnull so that it doesn't return any value on our screen
        except Exception as e:
            print(e)


    def run(self):
        self.showNetworks()
        while True:
            if self.stdscr.getch() == ord('q'): break # stops our program if we press q




def main(stdscr):
    use_default_colors()
    Curses(stdscr, "Wifi Manager").run()



if __name__ == "__main__":
    wrapper(main)

