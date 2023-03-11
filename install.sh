#!/bin/bash

# Install required packages
apt-get update
apt-get install -y git python3-pip screen

# Get the home directory of the current user
home_dir=$HOME

# Clone the BioBlitz repository to the user's home directory
cd $home_dir
git clone https://github.com/Thorpy/BioBlitz

# Install requirements for main.py
cd $home_dir/BioBlitz/bioblitz-game
pip3 install -r requirements.txt

# Run setup.py script
cd $home_dir/BioBlitz/raspi-captive-portal
yes Y | sudo python $home_dir/BioBlitz/raspi-captive-portal/setup.py

# Add startup command to rc.local
sed -i -e '$i su -c "screen -dmS main /usr/bin/python3 $home_dir/BioBlitz/bioblitz-game/main.py" $USER\n' /etc/rc.local

# Start the main.py script in a new screen session
screen -dmS main /usr/bin/python3 $home_dir/BioBlitz/bioblitz-game/main.py
