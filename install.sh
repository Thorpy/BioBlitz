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
# Create systemd service file
cat << EOF | sudo tee /etc/systemd/system/bioblitz.service > /dev/null
[Unit]
Description=BioBlitz Game
After=network-online.target

[Service]
User="$user"
WorkingDirectory=$home_dir/BioBlitz/bioblitz-game
ExecStart=/usr/bin/screen -dmS bioblitz bash -c "python3 main.py"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the systemd service
sudo systemctl enable bioblitz.service
sudo systemctl start bioblitz.service

echo "Installation complete. The system will now reboot."
reboot
