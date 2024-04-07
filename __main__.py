import argparse

from rpi.hunter import let_the_hunt_begin

parser = argparse.ArgumentParser()
parser.add_argument('--list', action='store_true',
		help='list available payloads')
parser.add_argument('--no-scan', dest='no_scan', action='store_true',
		help='disable arp scanning')
parser.add_argument('-r', dest='ip_range', type=str, default='--localnet',
		help='ip range to scan')
parser.add_argument('-f', dest='ip_list', type=str, default='./scan/rpi_list',
		help='ip list to use (default ./scan/rpi_list)')

parser.add_argument('-u', dest='uname', type=str, default='pi',
		help='username to use when ssh\'ing')
parser.add_argument('-c', dest='creds', type=str, default='raspberry',
		help='password to use when ssh\'ing')

parser.add_argument('--payload', type=str, default='whoami',
		help='(name of, or raw) payload [ex. reverse_shell or \'whoami\']')

parser.add_argument('-H', dest='host', type=str,
		help='(if using reverse_shell payload) host for reverse shell')
parser.add_argument('-P', dest='port', type=str,
		help='(if using reverse_shell payload) port for reverse shell')

parser.add_argument('--safe', action='store_true',
		help='print sshpass command, but don\'t execute it')
parser.add_argument('-q', dest='quiet', action='store_true',
		help='don\'t print banner or arp scan output')
args = parser.parse_args()

let_the_hunt_begin(args)
    