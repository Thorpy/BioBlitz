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

# Create a systemd service file to start main.py at boot time
cat <<EOF > /etc/systemd/system/bioblitz.service
[Unit]
Description=BioBlitz

[Service]
Type=simple
ExecStart=/usr/bin/python3 $home_dir/BioBlitz/bioblitz-game/main.py
User=$user
Group=$user
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd configuration and enable the service
systemctl daemon-reload
systemctl enable bioblitz.service

echo "Installation complete. The system will now reboot."
reboot
