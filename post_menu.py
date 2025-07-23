import os
import time
from colorama import Fore, init, Style
import subprocess
import sys

init(autoreset=True)

# file imports

import DeAuth
import watch_clients
import full_cleanup
from captive_portal import launch_captive_portal
import Compare_pass



def ATK_Menu():
    border = Fore.LIGHTBLACK_EX
    title = Fore.CYAN + Style.BRIGHT
    num_color = Fore.GREEN + Style.BRIGHT
    text_color = Fore.LIGHTWHITE_EX
    exit_color = Fore.RED + Style.BRIGHT

    print(border + "╔════════════════════════════════════════╗")
    print(border + "║" + title + "        Post-Hostapd Control Panel      " + border + "║")
    print(border + "╠════════════════════════════════════════╣")
    print(border + "║ " + num_color + "[1]" + text_color + " Start Captive Portal               " + border + "║")
    print(border + "║ " + num_color + "[2]" + text_color + " Launch Deauth Attack               " + border + "║")
    print(border + "║ " + num_color + "[3]" + text_color + " Stop Deauth Attack                 " + border + "║")
    print(border + "║ " + num_color + "[4]" + text_color + " Compare Password with Handshake    " + border + "║")  # moved here
    print(border + "║ " + num_color + "[5]" + text_color + " View Connected Clients             " + border + "║")
    print(border + "║ " + num_color + "[6]" + text_color + " Disconnect Client (Deauth by MAC)  " + border + "║")
    print(border + "║ " + num_color + "[7]" + text_color + " Restart Fake AP (hostapd + dnsmasq)" + border + "║")
    print(border + "║ " + exit_color + "[0]" + text_color + " Exit Script                        " + border + "║")
    print(border + "╚════════════════════════════════════════╝")









def post_menu():
    ATK_Menu()
    while True:
        command = input("$> ").strip()

        if command == "1":  # Captive Portal
            launch_captive_portal()
        
        elif command == "2":  # DeAuth
            DeAuth.DeAuth()
            time.sleep(1)
            os.system("clear")
            ATK_Menu()
        
        elif command == "3":  # stop deauth
            print("Stopping Deauth...")
            print("")
            print(Fore.GREEN + "Killing", "Aireplay-ng")
            os.system("sudo pkill aireplay-ng")
        
        elif command == "4":  # Compare Password with Handshake (NEW)
            Compare_pass.main()
            print()
            ATK_Menu()

        elif command == "5":  # check for connected clients
            watch_clients.watch_clients()
            pass
        
        elif command == "6":  # kick clients
            watch_clients.run_kick_sta_menu()
            pass
        
        elif command == "7":  # Restart Fake AP
            os.system("sudo pkill hostapd")
            print(Fore.RED + "killing hostapd")
            os.system("sudo pkill dnsmasq")
            print(Fore.RED + "killing dnsmasq")
            time.sleep(1)

            print(Fore.GREEN + "Starting hostapd...")
            subprocess.Popen(['xterm', '-hold', '-e', 'sudo hostapd hostapd.conf'])

            time.sleep(5)

            print(Fore.GREEN + "Starting dnsmasq...")
            time.sleep(1)
            subprocess.Popen(['xterm', '-hold', '-e', 'sudo dnsmasq --no-resolv --conf-file=./dnsmasq.conf --log-queries --log-dhcp --no-daemon'])
        
        elif command == "0":  # exit script
            print(Fore.CYAN + "Exiting Script...")
            full_cleanup.full_cleanup()
            sys.exit()
        
        elif command == "clear":  # clear
            os.system("clear")
            ATK_Menu()
        
        else:
            print(Fore.RED + "Invalid option, try again.")
        
