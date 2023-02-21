# BioBlitz


This is a "BioBlitz" game for "The Rockpool Project"

The aim of the game is to join teams and do real life "bioblitz" battles, finding and submitting sea creatures/life in real life for scores.

The game runs on a raspberry pi, the captive portal (https://github.com/Splines/raspi-captive-portal) spawns a wifi hotspot which redirects users to a "welcome page"
This welcome page then redirects the user (open pressing the start button) to the FastAPI server which hosts the bioblitz game.

------------------------------------------------

How-To start the game:

Install the imports for BioBlitz:
sudo apt install pip
pip install asyncio typing fastapi websockets uvicorn

Add main.py to rc.local and have it running on a new "screen":
sudo apt install screen
sudo nano /etc/rc.local
su -c "screen -dmS main /usr/bin/python /path/to/main.py" pi

For the captive portal:

clone into:
git clone https://github.com/Splines/raspi-captive-portal.git

cd ./raspi-captive-portal/

Customise the files in there to what you want:
(can't really help you there, but you can look at mine in this repo for what I used, changed ssid, pass and country code in raspi-captive-portal/access-point/hostapd.conf
and the welcome page (raspi-captive-portal/server/public/index.html) to redirect to 192.168.4.1:8000)
Once you've made all your changes to the files in captive portal, navigate to raspi-captive-portal and run:
sudo python setup.py

This will set up the captive portal and welcome page and add it to startup automatically.

------------------------------------------------
