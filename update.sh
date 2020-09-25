#!/bin/sh

# A simple Bash shell script that installs packages depended on by AstroNinja
# Created by: Tom Mullins
# Created: 09/24/2020
# Modified: 09/25/2020

# First, we need to install the proper python 3 Libraries
sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-tk python3-pyqt5.qtwebengine python3-setuptools

# Next we install the libaries installed by pip
python3 -m pip install matplotlib lxml scrapy

# removes the folder, then copies the files to a . folder.
rm -rf /home/$USER/.AstroNinja
mkdir /home/$USER/.AstroNinja

cp -r /home/$USER/Downloads/AstroNinja-Alpha/* /home/$USER/.AstroNinja
