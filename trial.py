# This script needs to run with admin priviledges

##->If want to reverse the effect run
##->reverse()

# Windows Generally Blocks CMD operations
# For that -->
# Open Command Prompt as Administrator:
# Run Group Policy Editor
# gpedit.msc

# Go Here
# User Configuration -> Administrative Templates -> System
# Disable Command Prompt
# Prevent access to the command prompt : " Select "Enabled"
# Apply the Policy
# and the run the script : script.py

import os
import subprocess
import ctypes

def disable_usb():
    os.system('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v "Start" /t REG_DWORD /d 4 /f')

def disable_bluetooth():
    subprocess.run(['sc', 'stop', 'bthserv'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(['sc', 'config', 'bthserv', 'start=disabled'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def disable_cmd():
    os.system('reg add HKCU\\Software\\Policies\\Microsoft\\Windows\\System /v "DisableCMD" /t REG_DWORD /d 2 /f')

def block_site(website):
    path = r"C:\Windows\System32\drivers\etc\hosts"
    with open(path, 'a') as hosts_file:
        hosts_file.write(f"127.0.0.1 {website}\n")

#Necessary to flush the DNS Cache for seeing the effect of Blocking
def clean_dns_cache():
    subprocess.run(['ipconfig', '/flushdns'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def enable_usb():
    os.system('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v "Start" /t REG_DWORD /d 3 /f')

def enable_bt():
    subprocess.run(['sc', 'config', 'bthserv', 'start=demand'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def enable_cmd():
    os.system('reg delete HKCU\\Software\\Policies\\Microsoft\\Windows\\System /v "DisableCMD" /f')

def unblock_site(website):
    path = r"C:\Windows\System32\drivers\etc\hosts"
    with open(path, 'r') as hosts_file:
        lines = hosts_file.readlines()
    with open(path, 'w') as hosts_file:
        for line in lines:
            if not line.startswith(f"127.0.0.1 {website}"):
                hosts_file.write(line)
def reverse():
    enable_usb()
    enable_bt()
    enable_cmd()
    unblock_site("facebook.com")
    clean_dns_cache()


if __name__ == "__main__":
    if os.name != 'nt' or not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please run using administrator priviledges.")
    else:
        print("Executing...")
        disable_usb()
        disable_cmd()
        block_site("facebook.com")
        clean_dns_cache()
        print("Done!!")


