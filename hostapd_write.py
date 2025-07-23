import time
import os
import colorama
from colorama import Fore, init
init(autoreset=True)

#----------------------------------------------------------------------- CONFIG HANDELING

# set variables
interface = ""                  # Wireless interface (e.g., wlan0)
driver = "nl80211"              # Common Linux driver
ssid = ""                      # Network name (SSID)
bssid = "02:11:22:33:44:55"                     # Set AP MAC address
hw_mode = "g"                  # Band: a = 5GHz, g = 2.4GHz
channel = ""                   # Wi-Fi channel (1–14 for 2.4GHz, 36+ for 5GHz)
auth_algs = "1"                # Auth: 1=open, 2=shared, 3=both

# Try reading hostapd.conf on start
try:
    with open('hostapd.conf', 'r') as file:
        content = file.read()
except FileNotFoundError:
    content = ""

# tracking color state
color_handle1 = Fore.GREEN
color_handle2 = Fore.RED
color_handle3 = Fore.RED
color_handle4 = Fore.RED

def Options_Menu_hostapd():
    print(Fore.MAGENTA + "use ' SET [ Option ] [ New Value ] ' to change")
    print(Fore.RED + "RED = CHANGE")
    print(Fore.GREEN + "help menu = HELP\n")
    print(Fore.BLUE + "NOTE: Channels 1-14 → hw_mode = g | Channels 36-165 → hw_mode = a")
    print("----------------------------------------------\n")
    print(f"{color_handle2}[+] interface : ", interface)
    print(Fore.GREEN + "[+] driver : ", driver)
    print(f"{color_handle3}[+] ssid : ", ssid)
    print(f"{color_handle1}[+] bssid : ", bssid)
    print(Fore.GREEN + "[+] hw_mode : ", hw_mode)
    print(f"{color_handle4}[+] channel : ", channel)
    print(Fore.GREEN + "[+] auth_algs : ", auth_algs)
    print("")

def clear():
    os.system("clear")
    Options_Menu_hostapd()

def handle_set_command(command):
    parts = command.split()
    global color_handle1, color_handle2, color_handle3, color_handle4

    if len(parts) == 3 and parts[0].lower() == "set":
        option = parts[1].lower()
        new_value = parts[2].strip()

        if option == "interface":
            global interface
            interface = new_value
            print(Fore.GREEN + f"Updated interface to {interface}")
            color_handle2 = Fore.GREEN
            time.sleep(.5)
            clear()

        elif option == "bssid":
            global bssid
            bssid = new_value
            print(Fore.GREEN + f"Updated bssid to {bssid}")
            color_handle1 = Fore.GREEN
            time.sleep(.5)
            clear()

        elif option == "driver":
            global driver
            driver = new_value
            print(Fore.GREEN + f"Updated driver to {driver}")
            time.sleep(.5)
            clear()

        elif option == "ssid":
            global ssid
            ssid = new_value.strip()
            print(Fore.GREEN + f"Updated SSID to {ssid}")
            color_handle3 = Fore.GREEN
            time.sleep(.5)
            clear()

        elif option == "hw_mode":
            global hw_mode
            hw_mode = new_value
            print(Fore.GREEN + f"Updated hw_mode to {hw_mode}")
            time.sleep(.5)
            clear()

        elif option == "channel":
            global channel
            channel = new_value
            print(Fore.GREEN + f"Updated channel to {channel}")
            color_handle4 = Fore.GREEN
            time.sleep(.5)
            clear()

        elif option == "auth_algs":
            global auth_algs
            auth_algs = new_value
            print(Fore.GREEN + f"Updated auth_algs to {auth_algs}")
            time.sleep(.5)
            clear()

        else:
            print(Fore.RED + "Invalid option.")
    else:
        print(Fore.RED + "Invalid command format. Use: SET [Option] [New Value]")

folder_path = "hostapd_presets/"

def show_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    files = os.listdir(folder_path)
    if not files:
        print(Fore.BLUE + f"The folder '{folder_path}' is empty.")
        print(Fore.RED + "Please ensure you have previously saved a preset using Option 1.")
        return

    print(Fore.GREEN + "Type ", "' help '", Fore.GREEN + " for help menu\n")
    print(Fore.MAGENTA + "to load preset: ", "load [ preset ]")
    print(Fore.CYAN + "to show preset contents: ", "show [ preset ]\n")
    print(Fore.LIGHTRED_EX + "----", Fore.BLUE + "Presets", Fore.LIGHTRED_EX + "----\n")
    for file in files:
        x = file.replace(".conf", "")
        print("- ", Fore.MAGENTA + x)

def hostapt_config_display(content):
    a = input("Display Current Hostapd Config? y/n  >  ")
    if a == "y":
        print("\nCurrent Hostapd Config\n-----------------------\n")
        print(content)
    elif a != "n":
        print("Please Enter A Valid Option")
    print("")

def write_to_conf():
    # Strip trailing spaces on every config variable
    clean_interface = interface.strip()
    clean_driver = driver.strip()
    clean_ssid = ssid.strip()
    clean_bssid = bssid.strip()
    clean_hw_mode = hw_mode.strip()
    clean_channel = channel.strip()
    clean_auth_algs = auth_algs.strip()

    # Debug print to confirm what's being written
    print(Fore.YELLOW + "[INFO] Writing hostapd.conf with these values:")
    print(f"interface={clean_interface}")
    print(f"driver={clean_driver}")
    print(f"ssid={clean_ssid}")
    print(f"bssid={clean_bssid}")
    print(f"hw_mode={clean_hw_mode}")
    print(f"channel={clean_channel}")
    print(f"auth_algs={clean_auth_algs}\n")

    # Write cleaned config lines
    with open("hostapd.conf", "w") as a:
        a.write(f'''interface={clean_interface}
driver={clean_driver}
ssid={clean_ssid}
bssid={clean_bssid}
hw_mode={clean_hw_mode}
channel={clean_channel}
auth_algs={clean_auth_algs}
ctrl_interface=/tmp/hostapd
''')

    print(Fore.GREEN + "[SUCCESS] hostapd.conf written successfully without trailing spaces.")

    
def help_menu1():
    os.system("clear")
    print(''' 
        OVERVIEW
------------------------

this section of the tool is used to configure the hostapd.conf file

        HELP MENU
-------------------------

[ COMMANDS ]

clear                  - Clears the screen and refreshes the options menu
exit                   - Exits the script safely
HELP                   - Displays the help menu with command and option info
set <option> <value>   - Sets a configuration value (e.g. SET ssid MyNetwork)
PRESET <name>          - Saves the current hostapd setup as a preset
''')

def help_menu2():
    os.system("clear")
    print(''' 
        OVERVIEW
------------------------

this section is used to load previously saved hostapd configurations

        HELP MENU
-------------------------

[ COMMANDS ]

clear                  - Clears the screen and refreshes the options menu
exit                   - Exits the script safely
load < option >        - Loads a pre-saved preset from the list
show < option >        - Displays preset contents
''')

def hostapd_setup_input():
    os.system("clear")
    print("\nHostapd : 1.SETUP  or  2.PRESET")

    a = input("$> ")

    if a == "exit":
        print(Fore.MAGENTA + "Thank You For Using!")
        time.sleep(2)
        exit()

    elif a == "1":
        os.system("clear")
        Options_Menu_hostapd()

        while True:
            command = input("$> ")
            if command == "clear":
                clear()
            elif command.lower().startswith("set "):
                handle_set_command(command)
            elif command == "WRITE":
                write_to_conf()
                break
            elif command.lower() == "help":
                help_menu1()
            elif command == "PRESET":
                os.system("clear")
                print("Please Ensure ", Fore.RED + "NO SPACES ", "are in the name")
                preset_name = input("Preset Name: ").lower().strip(" ")
                with open(f'hostapd_presets/{preset_name}.conf', 'w') as file:
                    file.write(f'''interface={interface}
driver={driver}
ssid={ssid.strip()}
bssid={bssid}
hw_mode={hw_mode}
channel={channel}
auth_algs={auth_algs}
ctrl_interface=/tmp/hostapd
''')
                print(Fore.GREEN + f"Preset '{preset_name}' saved.")
            else:
                print("Please Enter Valid Input")


            ready_colors = [color_handle1, color_handle2, color_handle3, color_handle4]
            if all(item == Fore.GREEN for item in ready_colors):
                print(Fore.GREEN + "READY TO WRITE  -  ' WRITE ' in all caps to write .conf file")
                print(Fore.MAGENTA + "Type ' PRESET ' to save as preset")

    elif a == "2":
        os.system("clear")
        show_files_in_folder(folder_path)

        while True:
            command = input("$> ")
            if command == "clear":
                os.system("clear")
                show_files_in_folder(folder_path)
                print(Fore.GREEN + "type ' help ' to show options")
            elif command.lower() == "help":
                help_menu2()
            elif command == "exit":
                print("Thanks For Using!")
                exit()
            elif command.lower().startswith("load "):
                bb = command.split()
                if len(bb) == 2:
                    load_value = bb[1]
                    try:
                        with open(f'hostapd_presets/{load_value}.conf', 'r') as file:
                            preset_read = file.read()
                            time.sleep(.5)
                            print(Fore.GREEN + f"Loaded {load_value}")
                            with open("hostapd.conf", "w") as b:
                                b.write(preset_read)
                            break
                    except FileNotFoundError:
                        print(Fore.RED + f"Preset '{load_value}' not found.")
                else:
                    print(Fore.RED + "Usage: load <preset_name>")
                
            elif command.lower().startswith("show "):
                os.system("clear")
                show_files_in_folder(folder_path)
                cc = command.split()
                if len(cc) == 2:
                    read = cc[1]
                    with open(f"hostapd_presets/{read}.conf", "r") as read_file:
                        aaaaaa = read_file.read()
                        print(aaaaaa)
            else:
                print("Please Enter Valid Input")
                
    else:
        print("Please Enter Valid Input")
        time.sleep(2)
        hostapd_setup_input()

#----------------------------------------------------------------


