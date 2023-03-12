#!/bin/bash

# Install required packages
apt-get update
apt-get install -y git python3-pip screen

# Get the home directory of the current user
home_dir=/home/$SUDO_USER
user=$SUDO_USER

# Clone the BioBlitz repository to the user's home directory
cd $home_dir
git clone https://github.com/Thorpy/BioBlitz

# Install requirements for main.py
cd $home_dir/BioBlitz/bioblitz-game
pip3 install -r requirements.txt

# Run setup.py script
cd $home_dir/BioBlitz/raspi-captive-portal
yes Y | sudo python $home_dir/BioBlitz/raspi-captive-portal/setup.py

# Add a command to run main.py in a screen session at startup
sudo sed -i '/exit 0/d' /etc/rc.local
sudo sh -c "echo 'su $user -c \"screen -dmS bioblitz python3 $home_dir/BioBlitz/bioblitz-game/main.py\"' >> /etc/rc.local"
sudo sh -c "echo 'exit 0' >> /etc/rc.local"

# Change the owner of the BioBlitz directory to the user
chown -R $user:$user $home_dir/BioBlitz

echo "Installation complete. The system will now reboot."

reboot
