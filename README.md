# VeilCast - Evil Twin Framework

VeilCast is a semi-automated Evil Twin attack framework written in Python.  
It simplifies the process of setting up rogue Wi-Fi access points, launching captive portals, and capturing credentials—all while giving the user fine-tuned control over configurations and presets.

---

## 📌 Features

- ✅ Interface selection and setup
- ✅ Network scanning (live Wi-Fi scan)
- ✅ Hostapd automation (rogue AP deployment)
- ✅ DHCP server configuration
- ✅ Captive portal launch
- ✅ Manual and preset-based configuration
- ✅ Basic logging and user feedback
- ✅ Designed to run on Linux based systems

---

## ⚙️ Requirements

- Python 3.x  
- `hostapd`, `dnsmasq`, `iptables`, `airmon-ng`, `iw`, `iproute2`, `net-tools`  
- `colorama` (Python package)  
- Root privileges

---

## 🔧 Installation

```bash
git clone https://github.com/Sota-0/VeilCast-Evil-Twin-Framework.git
cd VeilCast-Evil-Twin-Framework
pip3 install -r requirements.txt
chmod +x veilcast.py
