#!/bin/bash

# Install required packages
apt-get update
apt-get install -y git python3-pip screen

# Clone the BioBlitz repository to /home/pi/
cd /home/pi/
git clone https://github.com/Thorpy/BioBlitz

# Install requirements for main.py
cd /home/pi/BioBlitz/bioblitz-game
pip3 install -r requirements.txt

# Run setup.py script
python /home/pi/BioBlitz/raspi-captive-portal/setup.py

# Add startup command to rc.local
sed -i -e '$i su -c "screen -dmS main /usr/bin/python3 /home/pi/BioBlitz/bioblitz-game/main.py" pi\n' /etc/rc.local

# Start the main.py script in a new screen session
screen -dmS main /usr/bin/python3 /home/pi/BioBlitz/bioblitz-game/main.py