#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 10/01/2018
# Modified: 06/14/2020

# Installing libraries needed using pacman
sudo pacman -S python-pip python-pyqt5 python-dateutil python-tk python-pyqtwebengine python-setuptools

# Next we install the libaries installed by pip
sudo pip3 install matplotlib
sudo pip3 install lxml
sudo pip3 install bs4
sudo pip3 install scrapy


# copying the files to a . folder.
mkdir /home/$USER/.AstroNinja

cd "${0%/*}"
cp -r ./* /home/$USER/.AstroNinja

chmod +x /home/$USER/.AstroNinja/AstroNinja.desktop
mv /home/$USER/.AstroNinja/AstroNinja.desktop /home/$USER/Desktop/

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
