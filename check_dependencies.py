import os
import time
from colorama import Fore, init

init(autoreset=True)




#============================
# Check Dependencies
#============================

dependencies = ["aircrack-ng", "hostapd", "dnsmasq", "xterm", "rxvt-unicode", "figlet"]


# check dependencies
def check_dependencies():

    to_install = []
    a = 0
    
    for i in dependencies:
        check = os.popen(f"dpkg -l | awk '$1 == \"ii\" {{print $2}}' | grep -x {i}").read().strip()
        if i not in check:
            print(Fore.RED + "[-]", i)
            to_install.append(i)
            time.sleep(.1)
            a = 1
        else:
            print(Fore.GREEN + "[+]", i)
            time.sleep(.1)

    if a == 1:
        print("install dependencies? (y / n) : ", to_install)

        while True:
                command = input(">>")

                if command == "y":
                    print("installing...")
                    for i in to_install:
                        os.system(f"sudo apt-get install {i}")
                    time.sleep(.5)
                    print("")
                    print(Fore.MAGENTA + "please re-run the script")
                    break

                elif command == "n":
                     print(Fore.RED + "missing dependencies will cause issues")
                     time.sleep(4)
                     break

                else:
                     print("Please Enter a valid answer: y or n")

    else:
        print("")
        time.sleep(.5)
        print("all requirements are met")
        time.sleep(2)
        os.system("clear")

    