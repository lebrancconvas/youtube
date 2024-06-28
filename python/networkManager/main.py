from curses import A_UNDERLINE, echo, noecho, wrapper, curs_set, init_pair, COLOR_MAGENTA, color_pair, use_default_colors
from subprocess import DEVNULL, check_output, run
from time import sleep
from checkPassword import CheckNetwork

class Curses():
    def __init__(self, stdscr, message):
        self.stdscr = stdscr
        self.message = message
        curs_set(0)  # Hide the cursor
        init_pair(1, COLOR_MAGENTA, -1)
        self.stdscr.clear()
        self.stdscr.refresh()
        self.wifi = [] #a list to keep all networks


    
    def showNetworks(self):
        max_y, max_x = self.stdscr.getmaxyx()
        center_y = 2
        center_x = (max_x // 2) - (len("|_______Available Networks________|") // 2)
        self.stdscr.clear()
        self.stdscr.addstr(center_y, center_x, "|_______Available Networks________|", color_pair(1))
        self.stdscr.refresh()
        conlist = check_output(["nmcli", '-f', 'SSID', 'dev', 'wifi', 'list'], universal_newlines=True)
        self.wifi = [line.split()[0] for line in conlist.splitlines()[1:]]

        for idx, network in enumerate(self.wifi):
            self.stdscr.addstr(int(idx) + 4, center_x, f"{int(idx) + 1}. {network}")

            
        self.stdscr.addstr(len(self.wifi) + 5, center_x, "Choose your network: ")
        self.stdscr.refresh()

        while True:
            try:
                select = self.stdscr.getch() - ord('1')
                self.connnect(select)
            except KeyboardInterrupt:
                self.stdscr.clear()
                self.stdscr.addstr(center_y, center_x, "Progarm closed, press q key to close")
                break




    def connnect(self, select):
        max_y, max_x = self.stdscr.getmaxyx()
        center_x = (max_x // 2) - (len("Program Closed") // 2)
        if 0 <= select < len(self.wifi):
            wifiName = self.wifi[select]
            echo()
            if self.checkPreviousPassword(wifiName):
                self.stdscr.refresh()
                self.stdscr.clear()
                self.stdscr.addstr(len(self.wifi) + 6, center_x, f"Connected to {wifiName}. Press q to quit.")
                self.stdscr.refresh()
                if self.stdscr.getch() == ord('q'): quit()

            else:
                self.stdscr.clear()
                self.stdscr.refresh()
                self.stdscr.addstr(len(self.wifi) + 6, center_x, "Enter password: ")
                self.stdscr.refresh()
                password = self.stdscr.getstr().decode("utf8")
                noecho()
                self.connectToWifi(wifiName, password)
                self.stdscr.clear()
                self.stdscr.addstr(len(self.wifi) + 8, center_x, f"Connected to {wifiName}")
                self.stdscr.refresh()
                self.stdscr.getch()
        else:
            self.stdscr.addstr(len(self.wifi) + 8, center_x, "Invalid network selection.")
            self.stdscr.refresh()
            self.stdscr.getch()

    def checkPreviousPassword(self, wifiName):
        if CheckNetwork(wifiName).isExist():
            run(['nmcli', 'con', 'up', wifiName], stdout=DEVNULL)
            return True
        else:
            self.stdscr.clear()
            self.stdscr.addstr(10,10, "Something went wrong.")
            self.stdscr.refresh()

    def connectToWifi(self, wifiName, password):
        try:
            run(['nmcli', 'dev', 'wifi', 'connect', wifiName, 'password', password], check=True, stdout=DEVNULL)
        except Exception as e:
            print(e)
            print(wifiName, password)


    def run(self):
        self.showNetworks()
        while True:
            if self.stdscr.getch() == ord('q'): break

def main(stdscr):
    print()
    use_default_colors()
    Curses(stdscr, "Wifi Manager").run()
            

if __name__ == "__main__":
    wrapper(main)
    
