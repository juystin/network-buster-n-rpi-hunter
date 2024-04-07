import argparse

from rpi.hunter import let_the_hunt_begin
from network_buster.buster import bust

from termcolor import cprint

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

# Prints the introduction message, originally inserted BusesCanFly.
# Kept (but updated) for the their sake!
def intro():
	print("\n")
	cprint("                        NETWORK BUSTER 'N' RPI-HUNTER                        ", "red")
	cprint("-----------------------------------------------------------------------------", "yellow")
	cprint("            Originally by BusesCanFly, Forked & Modified by Team             ", "blue")
	cprint("-----------------------------------------------------------------------------", "yellow")
	print("\n")

intro()
if bust():
	let_the_hunt_begin(args)
    