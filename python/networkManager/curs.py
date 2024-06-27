from curses import A_UNDERLINE, newpad, wrapper, curs_set, init_pair, COLOR_MAGENTA, COLOR_BLACK, color_pair, use_default_colors
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
        self.stdscr.clear()
        self.stdscr.addstr(10, 10, "|_______Available Networks________|", color_pair(1))
        self.stdscr.refresh()

        conlist = check_output(["nmcli", '-f', 'SSID', 'dev', 'wifi', 'list'], universal_newlines=True, shell=True)
        self.wifi = [line.split()[0] for line in conlist.splitlines()[1:]]

        for idx, network in enumerate(self.wifi):
            self.stdscr.addstr(idx + 2 + 2, f"{idx + 1}. {network}")
        self.stdscr.addstr(len(self.wifi) + 4, 0, "Choose your network: ")
        self.stdscr.refresh()

    def run(self):
        self.showNetworks()
        while True:
            if self.stdscr.getch() == ord('q'): break


    





'''
    def run(self):
        try:
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
    use_default_colors()
    Curses(stdscr, "Wifi Manager").run()
            

if __name__ == "__main__":
    wrapper(main)
    
