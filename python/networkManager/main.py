from curses import COLOR_MAGENTA, COLOR_RED, color_pair, echo, noecho, use_default_colors, wrapper, curs_set, init_pair, newwin #you don't need more than these
from curses.textpad import Textbox, rectangle
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
        init_pair(1, COLOR_MAGENTA, -1)
        init_pair(2, COLOR_RED, -1)
        self.magenta = color_pair(1)
        self.red = color_pair(2)

    def showNetworks(self):
                
        heading = "|_____Available Networks_____|"

        maxy, maxx = self.stdscr.getmaxyx() #getting the max terminal x and y conordinates
        centerX = (maxx // 2) - (len(heading) // 2)
        self.stdscr.clear()
        self.stdscr.addstr(0, (maxx // 2) - (len(self.message)), self.message, self.magenta)
        self.stdscr.refresh() #without refreshing it won't show
        self.stdscr.addstr(2, centerX, heading, self.magenta)
        self.stdscr.attron(self.red)
        self.stdscr.border()
        #list all the available networks with nmcli since this is available in most linux distro
        conlist = check_output(['nmcli', '-f', 'SSID', 'dev', 'wifi', 'list'], universal_newlines=True) #universal new lines use the /n
        

        self.wifi = [line.split()[0] for line in conlist.splitlines()[1:]]
        
        for idx, network in enumerate(self.wifi):
            self.stdscr.addstr(idx + 4, centerX, f"{idx + 1}. {network}")
        self.stdscr.border()
        self.stdscr.attroff(self.red) 

        self.stdscr.refresh()
        self.stdscr.addstr(len(self.wifi) + 5, centerX, "Choose Your Network: Press h to type hidden ssid")
        self.stdscr.refresh()
        while True:
            try:
                select = self.stdscr.getch()
                self.stdscr.refresh()
                #select = self.stdscr.getch() - ord('1')
                if select == ord('h'):
                    ssid = self.hiddenNetwork()
                    self.connect(ssid)
                    quit()
                else:
                    select -= ord('1')
                    self.validateWifi(select)
            except KeyboardInterrupt:
                self.stdscr.clear()
                self.stdscr.addstr((maxy // 2), centerX, "Program Ended, press q to close.")
    
    def validateWifi(self, index):
        if 0 <= index <= len(self.wifi):
            wifiName = self.wifi[index]
            self.connect(wifiName)



    def hiddenNetwork(self): #handles hidden network
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Type ssid: (hit Ctrl-G to send)")
        editwin = newwin(10,10, 1,1)
        rectangle(self.stdscr, 10, 10, 1, 1)
        self.stdscr.refresh()
        box = Textbox(editwin)
        box.edit()
        message = box.gather()
        if message is not None:
            select = message.strip()
            return select


    def connect(self, ssid):
        heading = "|_____Program Closed_____|"

        maxy, maxx = self.stdscr.getmaxyx()
        centerX = (maxx // 2) - (len(heading) // 2)
        

        #for later we need to create new file
        if self.checkPreviousPassword(ssid):
            self.stdscr.refresh()
            self.stdscr.clear()
            self.stdscr.addstr(len(self.wifi) + 4, centerX, heading)
            self.stdscr.refresh()
            self.stdscr.addstr(len(self.wifi) + 6, centerX, f"Connected to {ssid}. Press q to quit.")
            self.stdscr.refresh()
            if self.stdscr.getch() == ord('q'): quit()
        
        else:
            self.stdscr.refresh()
            self.stdscr.addstr(len(self.wifi) + 6, centerX, "Enter password: ") # prompt for the password
            self.stdscr.refresh()
            password = self.stdscr.getstr().decode("utf8") #get the inputted password
            noecho()
            self.connectToWifi(ssid, password)
            self.stdscr.clear()
            self.stdscr.addstr(len(self.wifi) + 8, centerX, f'Connected to {ssid}')
            self.stdscr.refresh()
            self.stdscr.addstr(len(self.wifi) + 10, centerX, heading)
            self.stdscr.refresh()
            self.stdscr.getch() #wait for user input to close


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
        while True:
            self.showNetworks()
            if self.stdscr.getch() == ord('q'): break # stops our program if we press q




def main(stdscr):
    use_default_colors()
    Curses(stdscr, "Wifi Manager").run()



if __name__ == "__main__":
    wrapper(main)

