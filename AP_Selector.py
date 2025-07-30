import time
import os
import sys
import subprocess
from colorama import Fore, init
import csv

init(autoreset=True)

import main


# scan for AP
# save to file (scan/recent.csv)
# read from file
# split options and save to variables
# let users select AP
# write needed information to Hostapd
# continue Script


def get_frequency_band(channel):
    """Return the frequency band (2.4GHz/5GHz) based on channel number."""
    try:
        ch = int(channel)
    except ValueError:
        return "Unknown"
    
    if 1 <= ch <= 14:
        return "2.4 GHz"
    elif 32 <= ch <= 165:
        return "5 GHz"
    else:
        return "Unknown"


def AP_selector_Func():
    global interface_for_scan
    global selected_bssid
    global selected_channel
    global selected_essid

    blocked_bssids = ["02:11:22:33:44:55"]

    os.system("clear")

    # remove previous scan results
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, "scan", "recent-01.csv")
        os.remove(file_path)

    except FileNotFoundError:
        pass

    else:
        pass

    # scan
    print(Fore.GREEN + "Starting AP Scan")
    time.sleep(2)
    main.detect_network_interfaces()
    
    print(Fore.YELLOW + "This interface will be used for relevant functions")
    print("")
    interface_for_scan = input("Interface to scan with: ").strip()

    while True:
        try:
            scan_time = int(input("Scan Duration (seconds): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    print(Fore.YELLOW + f"Switching {interface_for_scan} to MONITOR" )
    main.enable_monitor_mode(interface_for_scan)

    print("")
    print("Please Wait...")
    subprocess.Popen([
        'xterm', '-hold', '-geometry', '100x50', '-e',
        f'sudo airodump-ng {interface_for_scan} --write ./scan/recent --output-format csv '
    ])
    time.sleep(scan_time)
    print(Fore.GREEN + "Killing airodump-ng")
    print("")
    subprocess.run(["sudo", "pkill", "airodump-ng"])
    print("")
    print(Fore.YELLOW + f"Switching {interface_for_scan} to MANAGED")
    main.disable_monitor_mode(interface_for_scan)
    print("")
    print(Fore.GREEN + "DONE")
    time.sleep(2)

    os.system("clear")
    print(Fore.GREEN + "Please Wait...")
    time.sleep(1.5)

    # Parse CSV results
    with open("./scan/recent-01.csv", "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            if line.strip().startswith("Station MAC"):
                break
            if line.strip():
                lines.append(line)

    reader = csv.DictReader(lines)
    reader.fieldnames = [h.strip() for h in reader.fieldnames]

    ap_list = []
    for row in reader:
        essid = row["ESSID"].strip()
        bssid = row["BSSID"].strip()
        channel = row["channel"].strip()
        if essid and bssid not in blocked_bssids:
            ap_list.append((essid, bssid, channel))

    # Display APs with band info
    print("Select a network:")
    for i, (essid, _, channel) in enumerate(ap_list):
        band = get_frequency_band(channel)
        color = Fore.CYAN if "5" in band else Fore.YELLOW
        print(f"{i + 1}. {essid} {color}({band})")

    while True:
        try:
            choice = int(input("\nEnter choice number: ")) - 1
            if 0 <= choice < len(ap_list):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

    selected_essid, selected_bssid, selected_channel = ap_list[choice]
    selected_band = get_frequency_band(selected_channel)

    print("")
    print("\nSelected AP:")
    print(f"ESSID  : ", Fore.GREEN + selected_essid)
    print(f"BSSID  : ", Fore.GREEN + selected_bssid)
    print(f"Channel: ", Fore.GREEN + selected_channel)
    print(f"Band   : ", Fore.GREEN + selected_band)


# Call the function if this script is run directly
if __name__ == "__main__":
    AP_selector_Func()
