# AstroNinja-Alpha
AstroNinja is an all-around tracker of the space industry. It has launch schedules, launch tallies, live SpaceX launches, the weather on Mars, News articles, Hubble Images, and space station info. It is written in Python and depends heavily on the Pyqt5 and Scrapy libraries. This is the Alpha release of the app.


## Installation

### Debian-based Distros
Linux Mint/Ubuntu/Pop!OS

- Open the terminal and clone this repository to your directory of choice:
```bash
cd ~/Downloads/
git clone https://github.com/shiroininjaTech/AstroNinja-Alpha.git
cd AstroNinja-Alpha/
```
- Use chmod to change the permissions of the installation file and run it:
```bash
chmod +x install.sh
./install.sh
```

- Change username to your username in "icon" and "application" lines in the AstroNinja.desktop file using nano or a text editor:

```bash
nano ~/Desktop/AstroNinja.desktop
```


### Use AstroNinja
Ubuntu and Pop users: right-click on AstroNinja desktop icon and click "Allow Launching".
- It can also be launched from the terminal:

```bash
python3 AstroNinjaMain.py
```
## License

This software is licensed under the GPLv3 license. 

