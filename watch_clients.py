# chatGPT Wrote this

import subprocess
import sys
from colorama import Fore, init
import os
init(autoreset=True)

def watch_clients():
    bash_script = r'''
while true; do
    clear
    output=$(hostapd_cli -p /tmp/hostapd all_sta)
    macs=$(echo "$output" | grep -oE '([0-9a-f]{2}:){5}[0-9a-f]{2}')
    count=$(echo "$macs" | grep -c .)

    echo -e "\e[1;34m┌─────────────────────────────┐"
    echo -e "│ \e[1;32m📶  Hostapd Client Monitor\e[1;34m  │"
    echo -e "├─────────────────────────────┤"
    echo -e "│ \e[1;36mClients : \e[1;37m$count\e[1;34m"
    echo -e "│ \e[1;36mTime    : \e[1;37m$(date +'%H:%M:%S')\e[1;34m"
    echo -e "├─────────────────────────────┤"
    echo -e "│ \e[1;36mConnected MACs:\e[1;34m"
    echo "$macs" | sed 's/^/│   /'
    echo -e "└─────────────────────────────┘"
    sleep 5
done
'''

    subprocess.Popen([
        "xterm",
        "-fa", "Monospace",
        "-fs", "10",
        "-bg", "black",
        "-fg", "green",
        "-geometry", "40x20",
        "-hold",
        "-e",
        "bash", "-c", bash_script
])


# -------------- CHECK FUNCTIONALITY


def run_kick_sta_menu(interface="wlan0", control_path="/tmp/hostapd"):
    def check_root():
        if os.geteuid() != 0:
            print("❌ This script must be run as root (sudo).")
            return

    def get_connected_stas():
        try:
            output = subprocess.check_output(
                ["hostapd_cli", "-p", control_path, "-i", interface, "all_sta"],
                stderr=subprocess.DEVNULL
            ).decode()

            stas = []
            for line in output.strip().splitlines():
                if len(line.strip()) == 17 and ":" in line:
                    stas.append(line.strip())
            return stas
        except subprocess.CalledProcessError:
            print("❌ Failed to fetch connected STAs. Is hostapd running and control interface path correct?")
            return []

    def menu_select(stas):
        print("\n📡 Connected Stations:")
        for i, sta in enumerate(stas):
            print(f"[{i+1}] {sta}")
        
        try:
            choice = int(input("\nSelect a STA to kick (by number): ")) - 1
            if 0 <= choice < len(stas):
                return stas[choice]
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a number.")
        return None

    def kick_sta(sta_mac):
        try:
            subprocess.run(
                ["hostapd_cli", "-p", control_path, "-i", interface, "deauthenticate", sta_mac],
                check=True
            )
            print(Fore.GREEN + f"\n✅ Kicked {sta_mac}")
        except subprocess.CalledProcessError:
            print(f"\n❌ Failed to kick {sta_mac}")

    # --- Main Logic ---
    check_root()
    stas = get_connected_stas()
    if not stas:
        print("⚠️  No STAs currently connected.")
        return
    target_sta = menu_select(stas)
    if target_sta:
        kick_sta(target_sta)

