import os 
import time
import hostapd_write

# interface=wlan1

interface_name = None




def write_to_dnsmasq():
    time.sleep(3)
    with open("hostapd.conf", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("interface="):
                interface_name = line.split("=", 1)[1].strip()
                break  # Stop after first match

    with open("dnsmasq.conf", "w") as f:
        f.write(f'''interface={interface_name}
bind-interfaces
dhcp-range=10.0.0.10,10.0.0.100,12h
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1
log-queries
log-dhcp
address=/#/10.0.0.1

''')