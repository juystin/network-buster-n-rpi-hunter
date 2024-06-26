# network-buster 'n' rpi-hunter
* Automate discovering and joining vulnerable networks, 'n' then automate discovering and dropping payloads on LAN Raspberry Pi's via ssh

Original: [BusesCanFly/rpi-hunter](https://github.com/BusesCanFly/rpi-hunter)

## Installation

1. Install dependencies:  
   (Linux) `sudo pip install -U argparse termcolor` and `sudo apt -y install arp-scan tshark sshpass`  
   (Mac) `sudo pip3 install -U argparse termcolor`, `brew cask install wireshark`, `brew install arp-scan`,  
   and `brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb`
2. Download the repo: `git clone https://github.com/juystin/network-buster-n-rpi-hunter`  
3. Run the script: `python ./network-buster-n-rpi-hunter`

## Usage
Run `python network-buster-n-rpi-hunter --help` for instructions in CLI.

```
python network-buster-n-rpi-hunter [-h] [--list] [--payload PAYLOAD]

Optional arguments:
  -h, --help           show this help message and exit
  --list               List available payloads
  --payload PAYLOAD    (Name of, or raw) payload [ex. password or 'reboot'], defaults to 'whoami'
```

## Updating Known Credentials
Update `known_credentials/router` and `known_credentials/pi` accordingly.

## Disclaimer

The standard internet fun disclaimer applies. Don't commit crimes, be responsible.  
We are in no way responsible for anything and everything you do with network-buster-n-rpi-hunter.