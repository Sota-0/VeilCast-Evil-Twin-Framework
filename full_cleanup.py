import subprocess
import psutil
from colorama import Fore, init

init(autoreset=True)

import check_dependencies

list = check_dependencies.dependencies

def full_cleanup(interface=None):
    print(Fore.RED + "\n[!] Starting Cleanup...\n")

    # Kill rogue processes
    for proc in list:
        subprocess.run(["sudo", "pkill", proc])
        print(f"    [-] Killed {proc}")

    # Stop dhcpcd just in case
    subprocess.run(["sudo", "systemctl", "stop", "dhcpcd"])

    # Remove iptables rule if interface specified
    if interface:
        try:
            subprocess.run([
                "sudo", "iptables", "-t", "nat", "-D", "PREROUTING",
                "-i", interface, "-p", "tcp", "--dport", "80",
                "-j", "REDIRECT", "--to-port", "80"
            ], check=True)
            print(f"    [-] Removed iptables rule for interface {interface}")
        except subprocess.CalledProcessError:
            print(f"    [!] No iptables rule found or failed to remove for interface {interface}")

        # Disable IP forwarding
        try:
            subprocess.run(["sudo", "sh", "-c", "echo 0 > /proc/sys/net/ipv4/ip_forward"], check=True)
            print("    [-] Disabled IP forwarding")
        except Exception as e:
            print(f"    [!] Failed to disable IP forwarding: {e}")

    # Revert interfaces
    for iface in psutil.net_if_addrs().keys():
        if iface == "lo":
            continue
        try:
            subprocess.run(["sudo", "ip", "link", "set", iface, "down"])
            subprocess.run(["sudo", "iw", iface, "set", "type", "managed"])
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", iface])
            subprocess.run(["sudo", "ip", "link", "set", iface, "up"])
            print(f"    [-] Reverted interface: {iface}")
        except Exception as e:
            print(f"    [!] Skip {iface}: {e}")

    # Restart NetworkManager
    subprocess.run(["sudo", "service", "NetworkManager", "start"])
    print(Fore.GREEN + "\n[✓] Cleanup Complete.\n")
