# BioBlitz

BioBlitz is a game for "The Rockpool Project" that allows players to join teams and engage in real-life "bioblitz" battles by finding and submitting sea creatures/life for scores.

## How to Play

The game runs on a Raspberry Pi, and the captive portal ([https://github.com/Splines/raspi-captive-portal](https://github.com/Splines/raspi-captive-portal)) spawns a Wi-Fi hotspot that redirects users to a welcome page. The welcome page then redirects the user, upon pressing the start button, to the FastAPI server that hosts the BioBlitz game.

## Prerequisites

To play BioBlitz, you will need:

- A Raspberry Pi with Wi-Fi (or a dongle)
- An ethernet cable (unless you have two Wi-Fi chips, one onboard and one via dongle, as you need to be able to connect to the Pi and broadcast a Wi-Fi spot)
- An SD card and reader/adapter for your device
- Putty or your favorite SSH client ([https://putty.org](https://putty.org))
- Angry IP Scanner (if you need help finding the Pi's IP) ([https://angryip.org/download/](https://angryip.org/download/))

## Installation

1. Install the OS onto the Raspberry Pi and enable SSH/wireless config, etc.
   
   - Plug your SD card into a reader and into your PC.
   - Go to [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/) and download Raspberry Pi Imager.
   - Open up Raspberry Pi Imager and select operating system -> Raspberry Pi OS (other) -> Raspberry Pi OS Lite (32 bit).
   - Under "Storage," make sure the correct storage medium (the SD card) is selected.
   - IMPORTANT: Click the settings cog (under "write"), enable SSH, and set a username and password of your choice. If you do not have an Ethernet connection, you may want to configure wireless LAN to be able to access the Raspberry Pi. You can do this in the settings also. Now press save. PLEASE BE AWARE THAT USING AN ETHERNET IS A MUCH PREFERRED OPTION. IT WILL BE ANNOYING TO HAVE TO CONNECT VIA WIFI TO THE PI WHILE IT TRIES TO SET UP A WIFI HOTSPOT USING THE SAME WIFI CHIP. It is possible to use an onboard chip and a dongle, but this may require further setup.
   - Press "write" and wait for the process to complete.
   
2. SSH into your Raspberry Pi.

   - Once the SD card has finished being written to and the install is verified, take it out of your PC and reader and plug it into your Raspberry Pi.
   - If using an Ethernet, plug the Ethernet into the Pi and then plug in the power.
   - Try to find the IP of your Pi, either from the Ethernet or the Wi-Fi you supplied it with. You can do this by checking the connections to your router, or by using "Angry IP Scanner" to scan your network for it: [https://angryip.org/download/](https://angryip.org/download/) (The file shows up as ipscan-win64-3.9.1.exe if using the standalone exe.) The raspberry pi should show up as "raspberry.local" or similar (depending on if you customised the hostname or not)
   - Open up Putty and in the "host name or IP address" box type in your Pi's IP (the port will be 22 and should be there already), make sure connection type is "SSH," and at the bottom, click "open." This may pop up some text asking you to verify the fingerprint. If this happens, just press "yes" or "OK," and then you will be prompted to login as the user you created in the settings section above.
   - You should now be logged into the Pi!



# Setting up the Game.

1. Now logged into the pi, copy this: `wget https://raw.githubusercontent.com/Thorpy/BioBlitz/master/install.sh`
2. Right click in putty to paste the command into the terminal and press enter, this should download the script, type "ls" to list the content of the current directory and you should see "install.sh" in there.
3. You now need to make install.sh runnable as an executable, copy this: `sudo chmod +x install.sh`
4. Again, right click to paste it into the terminal and press enter.
5. Now you can run the script with: `sudo ./install.sh` (if you want to see what the script does, you can look at it here: https://raw.githubusercontent.com/Thorpy/BioBlitz/master/install.sh)
6. Sit back and wait for the script to finish running everything.

**YOU'RE DONE!**

The wifi hotspot "bioblitz game" should be broadcasting with the password "rockpool", the game is on 192.168.4.1:8000 if the captive portal isn't working on your device for some reason. This should happen when you join the hotspot with the password.


---------------------------------------------------------------------------

**Customisation:**

This script installs MY version of index.html and the game main.py, it also installs my version of the starter page and the access point information.
`BioBlitz/raspi-captive-portal/access-point/hostapd.conf` (see the file on here - `BioBlitz/raspi-captive-portal/access-point/hostapd.conf`)

The access point is "BioBlitz Game" with the password "rockpool", you can change this by using winscp and editing or via putty, cd into the directory and use whichever editor you like, such as `sudo nano hostapd.conf`.

You can also edit the landing page `index.html` here: `BioBlitz/raspi-captive-portal/server/public/` (see the file on here - https://github.com/Thorpy/BioBlitz/blob/master/raspi-captive-portal/server/public/index.html)

and the bioblitz game index, js and css etc here: `BioBlitz/bioblitz-game/static/` (https://github.com/Thorpy/BioBlitz/tree/master/bioblitz-game/static)

A big thank you to Splines - https://github.com/Splines
Splines made and maintains the captive portal used in this project (https://github.com/Splines/raspi-captive-portal)
