from curses import A_UNDERLINE, echo, newpad, noecho, wrapper, curs_set, init_pair, COLOR_MAGENTA, COLOR_BLACK, color_pair, use_default_colors
from time import sleep
from subprocess import check_output

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
        center_y = 2
        center_x = (max_x // 2) - (len("Program Closed") // 2)
        if 0 <= select < len(self.wifi):
            wifiName = self.wifi[select]
            echo()
            self.stdscr.addstr(len(self.wifi) + 6, 0, "Enter password: ")
            self.stdscr.refresh()
            password = self.stdscr.getstr().decode("utf8")
            noecho()


    def run(self):
        self.showNetworks()
        while True:
            if self.stdscr.getch() == ord('q'): break


    





'''
    def run(self):
            height, width = self.stdscr.getmaxyx()

            while True:
                for x in range(width - len(self.message), -1, -1):
                    self.show(x)
                    sleep(0.1)
                
                for x in range(1, width - len(self.message) + 1):
                    self.show(x)
                    sleep(0.1)

        except KeyboardInterrupt:
            pass
            #if self.stdscr.getkey() == ord('c'): pass

                            
'''


def main(stdscr):
    print()
    use_default_colors()
    Curses(stdscr, "Wifi Manager").run()
            

if __name__ == "__main__":
    wrapper(main)
    
