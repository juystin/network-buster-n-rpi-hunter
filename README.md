# network-buster 'n' rpi-hunter
* Automate discovering and joining vulnerable networks, 'n' then automate discovering and dropping payloads on LAN Raspberry Pi's via ssh

Original: [BusesCanFly/rpi-hunter](https://github.com/BusesCanFly/rpi-hunter)

## Installation

1. Install dependencies:  
   (Linux) `sudo pip install -U argparse termcolor` and `sudo apt -y install arp-scan tshark sshpass`  
   (Mac) `sudo pip3 install -U argparse termcolor` `brew cask install wireshark` `brew install arp-scan`   
   `brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb`
2. Download the repo: `git clone https://github.com/juystin/network-buster-n-rpi-hunter`  
3. Run the script: `python ./network-buster-n-rpi-hunter`

## Disclaimer

The standard internet fun disclaimer applies. Don't commit crimes, be responsible.  
We are in no way responsible for anything and everything you do with rpi-hunter.