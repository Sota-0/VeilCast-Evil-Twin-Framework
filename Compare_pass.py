import os
import re
import subprocess
from colorama import Fore, init

init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.txt")
HANDSHAKE_DIR = os.path.join(BASE_DIR, "handshakes")
TEMP_WORDLIST = os.path.join(BASE_DIR, "temp_wordlist.txt")
NETWORK_PASSWORDS_LOG = os.path.join(BASE_DIR, "Network_Passwords")

# Global to store selected filename
selected_cap_filename = None

def get_latest_password(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
            if not lines:
                print(Fore.RED + "[-] Credentials file is empty.")
                return None
            latest_line = lines[-1].strip()
            if "Password:" in latest_line:
                return latest_line.split("Password:")[-1].strip()
            else:
                print(Fore.RED + "[-] Password not found in the latest line.")
    except FileNotFoundError:
        print(Fore.RED + f"[-] Credentials file not found at {path}.")
    return None

def list_handshakes(directory):
    if not os.path.exists(directory):
        print(Fore.RED + f"[-] Handshake directory '{directory}' not found.")
        return []
    return sorted([f for f in os.listdir(directory) if f.endswith(".cap")])

def select_handshake(handshakes):
    global selected_cap_filename
    print(Fore.YELLOW + "\n[?] Select a handshake file:")
    for idx, file in enumerate(handshakes):
        print(f"  {idx+1}) {file}")
    while True:
        choice = input(Fore.CYAN + "[>] Enter number: ")
        if not choice.isdigit():
            print(Fore.RED + "[-] Invalid input.")
            continue
        choice = int(choice)
        if 1 <= choice <= len(handshakes):
            selected_cap_filename = handshakes[choice - 1]
            return os.path.join(HANDSHAKE_DIR, selected_cap_filename)
        else:
            print(Fore.RED + "[-] Choice out of range.")

def run_aircrack(password, handshake_path):
    with open(TEMP_WORDLIST, "w") as f:
        f.write(password + "\n")

    print(Fore.CYAN + f"[+] Testing password '{password}' on handshake '{handshake_path}'")

    result = subprocess.run(
        ["aircrack-ng", handshake_path, "-w", TEMP_WORDLIST],
        capture_output=True,
        text=True
    )
    return result.stdout

def extract_ssid_from_output(output):
    match = re.search(r"SSID\s+\.+:\s+(.*)", output)
    if match:
        return match.group(1).strip()
    return "Unknown_SSID"

def popup_xterm(ssid, password):
    cyber_text = f"""
PASS MATCH

File -[ {selected_cap_filename}
Pass -[ {password}

saved to ./Network_Passwords.txt
"""
    subprocess.Popen([
        'xterm',
        '-fa', 'Monospace',
        '-fs', '11',
        '-bg', 'black',
        '-fg', 'green',
        "-geometry", "40x20",
        '-hold',
        '-e', f'echo "{cyber_text}" && read -n 1'
    ])

def append_to_log(ssid, password):
    line = f"{selected_cap_filename} - {password}\n"
    with open(NETWORK_PASSWORDS_LOG, "a") as f:
        f.write(line)
    print(Fore.GREEN + f"[+] Saved to {NETWORK_PASSWORDS_LOG}: {line.strip()}")

def main():
    password = get_latest_password(CREDENTIALS_FILE)
    if not password:
        print(Fore.YELLOW + "[-] No valid password to test.")
        return None

    handshakes = list_handshakes(HANDSHAKE_DIR)
    if not handshakes:
        print(Fore.RED + "[-] No handshake files found.")
        return None

    selected_handshake = select_handshake(handshakes)

    output = run_aircrack(password, selected_handshake)
    print(Fore.GREEN + "\n[*] aircrack-ng Output:\n")
    print(output)

    ssid = extract_ssid_from_output(output)

    if "KEY FOUND!" in output:
        print(Fore.MAGENTA + f"\n[!!!] Password FOUND for SSID '{ssid}': {password}")
        append_to_log(ssid, password)
        popup_xterm(ssid, password)
        return ssid, password
    else:
        print(Fore.RED + "\n[-] Password NOT found.")
        return None

if __name__ == "__main__":
    main()
