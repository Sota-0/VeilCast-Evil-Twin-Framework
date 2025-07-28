import os
import time
from colorama import Fore, init, Style, Back

init(autoreset=True)


def main():
        
    os.system("clear")
    # main header
    print(''' 


    ██▒   █▓▓█████  ██▓ ██▓     ▄████▄   ▄▄▄        ██████ ▄▄▄█████▓
    ▓██░   █▒▓█   ▀ ▓██▒▓██▒    ▒██▀ ▀█  ▒████▄    ▒██    ▒ ▓  ██▒ ▓▒
    ▓██  █▒░▒███   ▒██▒▒██░    ▒▓█    ▄ ▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░
    ▒██ █░░▒▓█  ▄ ░██░▒██░    ▒▓▓▄ ▄██▒░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ 
    ▒▀█░  ░▒████▒░██░░██████▒▒ ▓███▀ ░ ▓█   ▓██▒▒██████▒▒  ▒██▒ ░ 
    ░ ▐░  ░░ ▒░ ░░▓  ░ ▒░▓  ░░ ░▒ ▒  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   
    ░ ░░   ░ ░  ░ ▒ ░░ ░ ▒  ░  ░  ▒     ▒   ▒▒ ░░ ░▒  ░ ░    ░    
        ░░     ░    ▒ ░  ░ ░   ░          ░   ▒   ░  ░  ░    ░      
        ░     ░  ░ ░      ░  ░░ ░            ░  ░      ░           
        ░                      ░                                    

    ''')

    print("Version:", Fore.CYAN + "V 1.0")
    print("Author ", Fore.LIGHTBLACK_EX + "-[", Style.BRIGHT + Fore.LIGHTWHITE_EX + "Sota-0", Fore.LIGHTBLACK_EX + "]-")
    print("Github: ", Fore.CYAN + "https://github.com/Sota-0/")
    print("")
    print("")
    print('Dependencies -[', Fore.CYAN + ' aircrack-ng suit + hostapd + dnsmasq + xterm + rxvt-unicode + figlet',' ]- ')
    print("")
    print("")

    # about section

    print(
    Style.BRIGHT + "VeilCast", '''is a semi-automated Evil Twin tool written in Python.
It handles interface setup, network scanning, launching Hostapd, handling DHCP, captive portals, and more.
While mostly automated, it also allows users to manually input configurations,
with an added PRESET functionality for Hostapd.
    ''')
    print("")
    print("")
    print(Fore.RED + "NOTE: ", "Save a valid handshake file in ./handshakes to enable password comparison")
    print("")


    print("Press [", Fore.CYAN + "Enter", "] To Continue")
    Command = input("")
    while True:
        if Command == "":
            break
        elif Command == "":
            break
    
    time.sleep(.5)
    os.system("clear")