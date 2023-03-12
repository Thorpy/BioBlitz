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

# Add startup command to rc.local to start main.py in a screen session as the current user
sed -i -e '/^exit 0/i # Export home_dir and user\nexport home_dir=\/home\/$SUDO_USER\nexport user=$SUDO_USER\n\n# Run main.py in screen session\nsu -c "screen -dmS main \/usr\/bin\/python3 $home_dir\/BioBlitz\/bioblitz-game\/main.py" $user\n' /etc/rc.local

echo "Installation complete. The system will now reboot."
reboot
