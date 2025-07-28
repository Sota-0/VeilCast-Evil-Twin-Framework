# library imports
import os
import time
from colorama import Fore, init
import subprocess
import psutil
import sys
import threading

init(autoreset=True)

# file imports
import hostapd_write
import dnsmasq_write
import check_dependencies
import AP_Selector
import post_menu
import banner


# =======================================[ FUNCTIONS

def clean_processes():
    os.system("clear")
    print(Fore.GREEN + "Cleaning Up Processes")
    time.sleep(1)
    os.system("sudo pkill hostapd")
    print("killing hostapd")
    os.system("sudo pkill dnsmasq")
    print("killing dnsmasq")
    os.system("sudo pkill aireplay-ng")
    print("killing aireplay-ng")
    os.system("sudo pkill xterm")
    print("killing xterm")
    os.system("sudo pkill dhclient")
    print("killing dhclient")
    os.system("sudo systemctl stop dhcpcd")
    print("killing dhcpcd")
    os.system("sudo service NetworkManager stop")
    print("killing NetworkManager")
    time.sleep(1)
    os.system("clear")


def ensure_ctrl_interface_dir(path="/tmp/hostapd"):
    if not os.path.isdir(path):
        print(Fore.RED + f"Directory {path} does not exist, creating it...")
        os.makedirs(path, exist_ok=True)
    else:
        print(Fore.GREEN + f"Directory {path} already exists.")


def enable_monitor_mode(interface): # enable_monitor_mode()
    try:
        subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["sudo", "iw", interface, "set", "monitor", "control"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
        print(f"[+] Monitor mode enabled on {interface}")
    except subprocess.CalledProcessError:
        print(f"[-] Failed to enable monitor mode on {interface}")


def disable_monitor_mode(interface):    # disable_monitor_mode()
    try:
        subprocess.run(["sudo", "ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["sudo", "iw", interface, "set", "type", "managed"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", interface, "up"], check=True)
        print(f"[+] Monitor mode disabled on {interface}")
    except subprocess.CalledProcessError:
        print(f"[-] Failed to disable monitor mode on {interface}")


def detect_network_interfaces():

    print("Found Network Interfaces:")
    print("============================")
    for interface, addrs in psutil.net_if_addrs().items():
        stats = psutil.net_if_stats().get(interface)
        if stats:
            print(f"\n {interface}", " - ", f"{Fore.GREEN + 'Up' if stats.isup else Fore.RED + 'Down'}")
        else:
            pass
    print("")
    print("============================")


def get_interfaces():
    return psutil.net_if_addrs().keys()


def scan_for_targets():
    scan_question = input("do u want to scan for target information? y / n: ")

    if scan_question == "y":
        print("")
        detect_network_interfaces()
        print("")
        print(Fore.YELLOW + "this interface will be reset after scan")
        print("")
        interface_for_scan = input("interface to scan with: ").strip()

        while True:
            try:
                scan_time = int(input("Scan Duration (seconds): "))
                break
            except ValueError:
                print("Please enter a valid number.")

        print(Fore.YELLOW + f"Switching ", interface_for_scan, Fore.YELLOW + " to MONITOR" )
        enable_monitor_mode(interface_for_scan)

        print("")
        print("Please Wait...")
        subprocess.Popen(['xterm', '-hold', '-geometry', '100x50', '-e', f'sudo airodump-ng {interface_for_scan}'])
        time.sleep(scan_time)
        print(Fore.GREEN + "Killing airodump-ng")
        subprocess.run(["sudo", "pkill", "airodump-ng"])
        print(Fore.YELLOW + f"Switching ", interface_for_scan, Fore.YELLOW + " to MANAGED" )
        disable_monitor_mode(interface_for_scan)
        print(Fore.GREEN + "DONE")
        time.sleep(2)


def find_interface_in_hostapd():
    global interface_name, bssid_mac, channel_number
    interface_name = None
    bssid_mac = None
    channel_number = None

    with open("hostapd.conf", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("interface="):
                interface_name = line.split("=", 1)[1].strip()
            elif line.startswith("bssid="):
                bssid_mac = line.split("=", 1)[1].strip()
            elif line.startswith("channel="):
                channel_number = line.split("=", 1)[1].strip()


def find_second_interface():
    global second_interface
    print("")
    print("First Interface: ", Fore.BLUE + interface_name)
    print("")
    second_interface = input("second interface to use (DeAuth Interface) : ").strip()
    while True:
        print("")
        print("First Interface: ", Fore.BLUE + interface_name)
        print("")
        if second_interface == interface_name:
            print(Fore.RED + "Cant select the same 2 interfaces")
            time.sleep(2)
            os.system("clear")
            print(Fore.GREEN + "Detecting network interfaces...\n")
            detect_network_interfaces() 
            find_second_interface()
            break
        else:
            print("")
            print(Fore.GREEN + f"First interface set to: {Fore.LIGHTBLUE_EX}{interface_name}", " - Host")
            print(Fore.GREEN + f"Second interface set to: {Fore.LIGHTBLUE_EX}{second_interface}", " - DeAuth")
            print("")
            print(Fore.GREEN + "Interface Setup Complete")
            break


def assigning_ip_addr():
    print(Fore.GREEN + "Assigning Host IP")
    os.system(f"sudo ip link set {interface_name} down")
    time.sleep(1)
    os.system(f"sudo ip link set {interface_name} up")
    time.sleep(1)
    os.system(f"sudo ip addr flush dev {interface_name}")
    time.sleep(.5)
    os.system(f"sudo ip addr add 10.0.0.1/24 dev {interface_name}")
    time.sleep(.5)
    os.system(f"sudo ip link set {interface_name} up")
    time.sleep(.5)
    print(Fore.GREEN + "DONE")
    print(Fore.GREEN + f"IP info for {interface_name}:")
    os.system(f"ip addr show {interface_name}")


def auto_manual():
    os.system("clear")

    print("Setup Options")
    print("1. Automatic Setup")
    print("2. Manual Setup")

    command = input("$> ")

    while True:

        if command == "1":
            print("Selected ", Fore.GREEN + "Automatic Setup")
            time.sleep(1)
            os.system("clear")
            print("this interface setup will be used for hosting")
            print("")
            time.sleep(4)
            AP_Selector.AP_selector_Func()

            from AP_Selector import selected_essid, selected_bssid, selected_channel, interface_for_scan

            print("")
            print("bssid preference:")
            print("[1] Use default BSSID")
            print("[2] Use original BSSID from target")

            while True:
                command = input("$>")

                if command == "1":
                    print()
                    selected_bssid = "02:11:22:33:44:55"
                    break
                elif command == "2":
                    selected_bssid = selected_bssid
                    break
                else:
                    print("invalid input")

            with open("hostapd.conf", "w") as a:
                a.write(f'''interface={interface_for_scan}
driver=nl80211
ssid={selected_essid}
bssid={selected_bssid}
hw_mode=g
channel={selected_channel}
auth_algs=1
ctrl_interface=/tmp/hostapd
''')
            break

        elif command == "2":
            print("Selected ", Fore.GREEN + "Manual Setup")
            time.sleep(1)
            os.system("clear")
            scan_for_targets()
            hostapd_write.hostapd_setup_input()
            break




    


# =======================================[ MAIN FUNCTION


def main():
    
    #==========[ Check Dependencies

    check_dependencies.check_dependencies()


    #==========[ Prepare

    # dialog
    os.system("clear")
    print(Fore.GREEN + "initializing network setup...")
    print(Fore.RED + "Please ensure interfaces arn't connected to wifi")
    time.sleep(5)

    clean_processes()

    #==========[ /tmp/hostapd check
    print("Checking for DIR: /tmp/hostapd")
    ensure_ctrl_interface_dir()
    time.sleep(2)


    #==========[ Auto or Manual option

    auto_manual()

    #==========[ extract hostapd config data

    find_interface_in_hostapd()
    time.sleep(2)

    # interface_name
    # bssid_mac
    # channel_number


    #==========[ Assigning IP

    assigning_ip_addr()

    #==========[ write to DNSMASQ

    os.system("sudo pkill dnsmasq")
    os.system("sudo pkill dhclient")
    os.system("sudo systemctl stop dhcpcd")
    time.sleep(3)
    print(Fore.GREEN + "Setting up dnsmasq")
    os.system("")
    time.sleep(2)
    dnsmasq_write.write_to_dnsmasq()
    print(Fore.GREEN + "dnsmasq.conf DONE")

    #==========[ Start Hostapd

    print(Fore.GREEN + "Starting hostapd...")
    subprocess.Popen(['xterm', '-hold', '-e', 'sudo hostapd hostapd.conf'])

    time.sleep(5)

    #==========[ Start DNSMASQ

    print(Fore.GREEN + "Starting dnsmasq...")
    time.sleep(1)
    subprocess.Popen(['xterm', '-hold', '-e', 'sudo dnsmasq --no-resolv --conf-file=./dnsmasq.conf --log-queries --log-dhcp --no-daemon'])

    #==========[ End Menu

    
    post_menu.post_menu()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root (sudo). Exiting.")
        sys.exit(1)
    os.system("clear")
    banner.main()
    main()
