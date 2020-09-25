#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 10/01/2018
# Modified: 09/23/2020

# First, we need to install the proper python 3 Libraries
sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-tk python3-pyqt5.qtwebengine python3-setuptools

# Next we install the libaries installed by pip
python3 -m pip install matplotlib lxml scrapy

# removes the folder, then copies the files to a . folder.
rm -rf /home/$USER/.AstroNinja
mkdir /home/$USER/.AstroNinja

cp -r ./* /home/$USER/.AstroNinja

# moving the desktop shortcut to the desktop
mv /home/$USER/.AstroNinja/AstroNinja.desktop /home/$USER/Desktop/

# Making both the desktop file and AstroNinjaMain.py executable
chmod +x /home/$USER/Desktop/AstroNinja.desktop
chmod +x /home/$USER/.AstroNinja/AstroNinjaMain.py

# Getting which distro the user is running
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME

#echo $OS
# If the user is running Linux Mint
if [ "$OS" = "Linux Mint" ] ; then
    # Removing an uneeded package that causes formatting errors in Linux Mint
    sudo apt-get remove qt5ct ;
    fi
fi
