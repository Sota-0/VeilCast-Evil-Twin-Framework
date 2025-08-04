import time
import os

# ./tmp/recent-01.csv
# ./Network_Passwords
# ./temp_wordlist
# ./credentials
# ./hostapd.conf





# ./tmp/recent-01.csv

os.system("rm ./tmp/recent-01.csv")


# ./Network_Passwords
with open("./Network_Passwords", "w") as Network_Passwords:
    Network_Passwords.write('''

''')
    
# ./temp_wordlist
with open("./temp_wordlist.txt", "w") as temp_wordlist:
    temp_wordlist.write('''

''')

# ./credentials
with open("./credentials.txt", "w") as credentials:
    credentials.write('''

''')

# ./hostapd.conf
with open("./hostapd.conf", "w") as hostapd:
    hostapd.write('''interface=PLACEHOLDER
driver=nl80211
ssid=PLACEHOLDER
bssid=PLACEHOLDER
hw_mode=g
channel=PLACEHOLDER
auth_algs=1
ctrl_interface=/tmp/hostapd

''')