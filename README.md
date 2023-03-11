# BioBlitz


This is a "BioBlitz" game for "The Rockpool Project"

The aim of the game is to join teams and do real life "bioblitz" battles, finding and submitting sea creatures/life in real life for scores.

The game runs on a raspberry pi, the captive portal (https://github.com/Splines/raspi-captive-portal) spawns a wifi hotspot which redirects users to a "welcome page"
This welcome page then redirects the user (open pressing the start button) to the FastAPI server which hosts the bioblitz game.

------------------------------------------------

Install the OS onto the raspberry pi and enable ssh/wireless config etc

1. Plug your sd card into a reader and into your pc.
2. Go to https://www.raspberrypi.com/software/ and download Raspberry Pi Imager.
3. Open up Raspberry pi imager and select operating system -> raspberry pi os (other) -> raspberry pi os lite (32 bit)
4. under "Storage" make sure the correct storage medium (the sd card) is selected.
5. --IMPORTANT-- click the settings cog (under "write"), enable SSH and set a username and password of your choice, if you do not have an ethernet connection, you may want to configure wireless lan to be able to access the raspberry pi, you can do this in the settings also, now press save.
6. You can now press "write" and go get yourself a nice coffee while it does it's thing. (if it pops up any window saying to open (H:) or any other drive just click cancel, it's just mounting the SD card ready for writing.


SSH into your raspberry pi.

1. Once the sd card has finished being written to and the install is verified, take it out of your pc and reader and plug it into your raspberry pi
2. At this stage, if using an ethernet, plug the ethernet into the pi and then plug in the power.
3. It's now time to try and find the IP of your pi, either from the ethernet or the wifi you supplied it with. I do this by checking the connections to my router, but there are other options such as using "angry ip scanner" to scan your network for it: https://angryip.org/download/ (shows up as ipscan-win64-3.9.1.exe) if using the standalone exe.
4. Now you know your pi's ip (mine is 192.168.1.10), you need something to connect to the pi with. I use "Putty" and "WinSCP" but there are other ssh clients, putty to interact with the pi's console and WinSCP to view and edit files on the pi. You can download putty here: https://putty.org/ and WinSCP from here: https://winscp.net/eng/download.php
5. Open up Putty and in the "host name or ip address" box type in your pi's ip (the port will be 22 and should be there already), make sure connection type is "SSH" and at the bottom, click "open", this may pop up some text asking you to verify the fingerprint, if this happens just press "yes" or "OK" and then you will be prompted to login as: you log in as the user you created in the settings section above (5 --important--). You should now be logged into the pi!


Setting up the Game.

1. Now logged into the pi, copy this: wget https://raw.githubusercontent.com/Thorpy/BioBlitz/master/install.sh
2. Right click in putty to paste the command into the terminal and press enter, this should download the script, type "ls" to list the content of the current directory and you should see "install.sh" in there.
3. You now need to make install.sh runnable as an executable, copy this: sudo chmod +x install.sh
4. Again, right click to paste it into the terminal and press enter.
5. Now you can run the script with: sudo ./install.sh (if you want to see what the script does, you can look at it here: https://raw.githubusercontent.com/Thorpy/BioBlitz/master/install.sh)
6. Sit back and wait for the script to finish running everything.

YOU'RE DONE!




Customisation:

This script installs MY version of index.html and the game main.py, it also installs my version of the starter page and the access point information.
BioBlitz/raspi-captive-portal/access-point/hostapd.conf (see the file on here - BioBlitz/raspi-captive-portal/access-point/hostapd.conf)

The access point is "BioBlitz Game" with the password "rockpool", you can change this by using winscp and editing or via putty, cd into the directory and use whichever editor you like, such as "sudo nano hostapd.conf".

You can also edit the landing page index.html here: BioBlitz/raspi-captive-portal/server/public/ (see the file on here - https://github.com/Thorpy/BioBlitz/blob/master/raspi-captive-portal/server/public/index.html)

and the bioblitz game index, js and css etc here: BioBlitz/bioblitz-game/static/ (https://github.com/Thorpy/BioBlitz/tree/master/bioblitz-game/static)


A big thank you to Spines - https://github.com/Splines
Spines made and maintains the captive portal used in this project (https://github.com/Splines/raspi-captive-portal)
