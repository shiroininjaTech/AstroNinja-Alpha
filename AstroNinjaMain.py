#!/usr/bin/env python3

"""
   This the Library file for the front end modules for AstroNinja, a space launch tracker and space news app for the
   Linux desktop. It scrapes data from across the web and displays it in an interactive GUI using scrapy and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.85
   * Date Created:  10/13/17
   * Date Modified: 06/22/20
"""
"""
   * Changelog:
   * Version 0.06: Added a greeting page with data on the next launch. Minor formatting fixes
   * Version 0.10: Added a schedule page with data on the next few launches
   * Version 0.50: Added Space agency logos to the next launch data on welcome tab
   * Version 0.60: Added the new astroGraph module, which tallies the launches remaining in the current month and displays them in
   *               a graph on the new graphs tab. Also added a settings menu with different theme options using the new astroThemes module.
   *               Various other formatting fixes.
   * Version 0.65: Added the new xNews module, which scrapes articles and images from various websites and displays it in the news tab. Added
   *                a new them to astroThemes named broco. Added the function to skip launches on the welcome screen if the date has passed.
   *                Various refactoring of code in the back end modules toward more object orientated solutions. Various formatting fixes.
   *
   * Version 0.70: Refactored various backend functions into reusuable code. Moved launches remaining graph to welcome page. Added ability for
   *                the graph to skip already occured launches. Added the Hubble Views tab, showing the current week's newest image from the
   *                Hubble Space Telescope and previous images. Added multithreading support to the web scraping functions of xNews.py. Added max
   *                launches shown by the launch schedule tab.
   *
   * Version 0.75: Fixed formatting errors when running on Linux Mint. Several icons changed to better fit layout of the gui. Added sources option to the
   *                main menu, giving the user links to view the source websites. An easy to run bash script was added to give the user an easy way to install
   *                the dependancies needed for the program to run. Added multiproccessing support to the scraping functions of xNews.py. Added functionality enabling
   *                graph colors to change with app themes.
   *
   * Version 0.80: Font size changes. Added high DPI scaling. Added second graph to welcome
   *                page showing total launches for the current year by org. Changed default theme to the
   *                SpaceX theme, and changed old default theme to 'Marine'. Added ability to skip launches
   *                to the next launch item on welcome page. Added new logos for newly reported companies in launch schedule.
   *                Added the ability to reload window via menu and when choosing a new UI theme. Redesign of Welcome tab.
   *                Added SpaceX lens, a portal to video of the company's last launch or livestream of the current launch. Various bug fixes.
   *
   * Version 0.85: Alpha release. This version included the full rewriting of all backend web scraping and data cleansing modules
   *                to switch from beautifulSoup4 to Scrapy spiders. New features added include: ISS Portal tab, as well as launch history graphs and
                    added more sources to the news tab. This version also added the Mars weather section to the welcome tab. The astroTheme module was also Refactored
                    to make it more compatible with a new release of PyQt5. Several bug fixes have been done, such as solving crashing when an article has no image,
                    and catching crashes caused by the scraping of the launch schedule. Many modules were also refactored to remove hundreds of lines of repetitive code using
                    functions. As this is the alpha version of the app, an install script was included as well.



"""

import re
import time, os
from os.path import expanduser

from datetime import date
import calendar
from dateutil import parser
import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QUrl
import astroGraphV85
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from configparser import ConfigParser
import astroThemesV85
import urllib.request, urllib.parse
import astroNinjaV85
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import youtubeTest
import xNewsV85
import issPortal
import scrapy
from scrapy.crawler import CrawlerProcess
from astro_spider.astro_spider.spiders import launchHistory
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from astro_spider.astro_spider.spiders import news_spider
from astro_spider.astro_spider.spiders import crewSpider
from astro_spider.astro_spider.spiders import scheduleSpider
from astro_spider.astro_spider.spiders import hubbleSpider
from astro_spider.astro_spider.spiders import MoreNews

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# Setting up the GUI window class and methods.

class App(QMainWindow):



    def __init__(self):
        super().__init__()

        #self.setGeometry(0, 0, 0, 0)
        self.setWindowTitle('AstroNinja')
        self.setWindowIcon(QIcon(os.path.expanduser("~/.AstroNinja/Images/Icons/rocket.png")))

        #self.showMaximized()
        self.initUI()

        #self.show()


    # The the method to setup the window.
    def initUI(self):


        # The about button method
        def clickMethod(self):
            aboutBox = QMessageBox()
            aboutBox.setIcon(QMessageBox.Question)
            aboutBox.setWindowTitle("About AstroNinja")
            aboutBox.setText("Version 0.85 Alpha\nCreated By: Tom Mullins")
            aboutBox.exec_()

        def sourceMethod(self):
            sourcelinks = ['https://www.spaceflightnow.com', 'https://www.spacenews.com', 'https://www.space.com/', 'https://www.spacetelescope.org']
            sourceMessage = "Launch Schedule Information From: <br><a href='{}'>     spaceflightnow.com</a><br><br>News Articles From:<br><a href='{}'>spacenews.com</a><br><a href='{}'>space.com</a><br><br>Hubble Images Courtesy Of: <br><a href='{}'>spacetelescope.org</a>".format(sourcelinks[0], sourcelinks[1], sourcelinks[2], sourcelinks[3])
            sourceBox = QMessageBox()
            sourceBox.setIcon(QMessageBox.Information)
            sourceBox.setWindowTitle("Sources")
            sourceBox.setText(sourceMessage)
            sourceBox.exec_()

        """
            Restarts the program
            To be used to reload the window when selecting a new theme
        """
        def restart_program():
            python = sys.executable
            os.execl(python, python, * sys.argv)

        """
            The functions for the Theme menu items
        """
        def Marine():
            themeConfig.set('theme', 'key1', 'marine')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        def Spacex():
            themeConfig.set('theme', 'key1', 'spaceX')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        def broco():
            themeConfig.set('theme', 'key1', 'broco')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        """
            The functions for changing article sortment in the settings menu.
            Added in V0.85
        """

        # Selecting newest.
        def newest():
            themeConfig.set('articleSorting', 'key1', 'Newest')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        # Selecting oldest.
        def oldest():
            themeConfig.set('articleSorting', 'key1', 'Oldest')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        """
            The functions for changing hubble image sortment in the settings menu.
            Added in V0.85
        """

        # Selecting newest.
        def newestHubble():
            themeConfig.set('hubbleSorting', 'key1', 'Newest')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        # Selecting oldest.
        def oldestHubble():
            themeConfig.set('hubbleSorting', 'key1', 'Oldest')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
            restart_program()

        # Set the central widget
        central_widget = QWidget(self)          # Create a central widget
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)         # Create a QGridLayout
        central_widget.setLayout(grid_layout)   # Set Layout to central widget

        # Setting fonts
        fontVar = QFont("Noto Sans", 25)        # Create a QFont instance
        fontVar.setBold(True)

        smallerHeader =  QFont("Noto Sans", 17)
        smallerHeader.setBold(True)

        welcomeFont = QFont("Noto Sans", 15)                                # A smaller Font
        welcomeFont.setBold(False)

        basicFont = QFont("Noto Sans", 13)                                # An even smaller Font
        basicFont.setBold(False)

        #=================================================================================================
        # Setting up the theme config file
        #=================================================================================================

        # initialize
        # Checking if the config file is present, and making one if it isnt. This prevents the configuration from being over written.

        global sortingSelected, HubblesortingSelected

        if not os.path.isfile("config.ini"):
            themeConfig = ConfigParser()
            themeConfig.read('config.ini')
            themeConfig.add_section('theme')
            themeConfig.set('theme', 'key1', 'spaceX')
            themeSelected = themeConfig.get('theme', 'key1')
            # Adding a section in the config.ini for storing options in article sorting.
            themeConfig.add_section('articleSorting')
            themeConfig.set('articleSorting', 'key1', 'Newest')
            sortingSelected = themeConfig.get('articleSorting', 'key1')
            # Adding a section in the config.ini for storing options in hubble sorting.
            themeConfig.add_section('hubbleSorting')
            themeConfig.set('hubbleSorting', 'key1', 'Newest')
            HubblesortingSelected = themeConfig.get('hubbleSorting', 'key1')

            with open('config.ini', 'w') as f:
                themeConfig.write(f)
        elif os.path.isfile("config.ini"):
            themeConfig = ConfigParser()
            themeConfig.read("config.ini")
            themeSelected = themeConfig.get('theme', 'key1')
            # Getting the sorting setting last set by the user.
            #global sortingSelected
            sortingSelected = themeConfig.get('articleSorting', 'key1')
            # Getting the sorting setting for hubble images last set by the user.
            HubblesortingSelected = themeConfig.get('hubbleSorting', 'key1')

        #================================================================================================
        # Running the Scrapy spiders that retreives data for the backend modules.
        #================================================================================================
        """
            Must run all spiders together in queue with reactor for them to work. :/
        """
        @defer.inlineCallbacks
        def spiderLauncher():
            process = CrawlerRunner({'ITEM_PIPELINES': { 'astroGraphV85.ItemCollectorPipeline': 2000}})
            yield process.crawl(launchHistory.LaunchhistorySpider)
            process2 = CrawlerRunner({'ITEM_PIPELINES': {'xNewsV85.ItemCollectorPipeline': 2000}})
            yield process2.crawl(news_spider.NewsSpiderSpider)
            process3 = CrawlerRunner({'ITEM_PIPELINES': { 'issPortal.BioCollectorPipeline': 2000}})
            yield process3.crawl(crewSpider.CrewspiderSpider)
            process4 = CrawlerRunner({'ITEM_PIPELINES': { 'astroNinjaV85.ScheduleCollectorPipeline': 2000}})
            yield process4.crawl(scheduleSpider.Schedulespider)
            process5 = CrawlerRunner({'ITEM_PIPELINES': {'xNewsV85.HubbleCollectorPipeline': 2000}})
            yield process5.crawl(hubbleSpider.HubblespiderSpider)
            process6 = CrawlerRunner({'ITEM_PIPELINES': {'xNewsV85.ItemCollectorPipeline': 2000}})
            yield process6.crawl(MoreNews.MorenewsSpider)
            #process.start(stop_after_crawl=False)
            reactor.stop()
            return

        spiderLauncher()
        reactor.run()

        #=================================================================================================
        # Creating tabs in the UI
        #=================================================================================================

        # Initilizing tabs
        self.tabs = QTabWidget()
        self.welcomeTab = QWidget()
        self.scheduleTab = QWidget()
        #self.graphTab = QWidget()
        self.spacexTab = QWidget()
        self.hubbleTab = QWidget()
        self.issTab = QWidget()


        if themeSelected == 'marine':
            astroThemesV85.defaultTabs(self.welcomeTab, self.scheduleTab, self.hubbleTab, self.tabs, self.spacexTab, self.issTab)
        if themeSelected == 'spaceX':
            astroThemesV85.spacexTabs(self.welcomeTab, self.scheduleTab, self.hubbleTab, self.tabs, self.spacexTab, self.issTab)
            self.setStyleSheet("QMainWindow { background-color: White; color: White; }")
        if themeSelected == 'broco':
            astroThemesV85.brocoTabs(self.welcomeTab, self.scheduleTab, self.hubbleTab, self.tabs, self.spacexTab, self.issTab)
            self.setStyleSheet("QMainWindow { background-color: Black; color: Black; }")


        self.tabs.addTab(self.welcomeTab, "Welcome")
        self.tabs.addTab(self.scheduleTab, "Launch Schedule")
        self.tabs.addTab(self.spacexTab, "News")
        self.tabs.addTab(self.hubbleTab, "Hubble Views")
        self.tabs.addTab(self.issTab, "ISS Portal")

        #=========================================================================================================
        # All the functions needed to build a UI for a PyQt5 App
        #=========================================================================================================

        # a function for creating and configuring frame items
        # (a) is the layout that the frame is to be added to
        # (b) is the first position value
        # (c) is the second position value
        # (e) is a toggle for if it is an inner frame

        def frameBuilder(a, b, c,  d, e ):
            self.frame = QFrame()
            """
            if themeSelected == 'marine':
                astroThemesV85.defaultFrame(self.frame)
            if themeSelected == 'spaceX':
                astroThemesV85.spacexFrame(self.frame)

            if themeSelected == 'broco':
                astroThemesV85.brocoFrame(self.frame)"""

            self.frame.setFrameShape(QFrame.Box)
            #self.nextframe.setFixedSize(150, 150)
            self.frame.adjustSize()
            a.addWidget(self.frame, b, c)
            if e == False:
                global frameLayout
            frameLayout = QGridLayout()
            self.frame.setLayout(frameLayout)
            frameLayout.setHorizontalSpacing(25)
            a.setColumnMinimumWidth(1, d)



        # A function that adds verticle margins to layouts
        # Takes the layout it is to be added to as "a"
        # "b" and "c" are the x and y dimensions
        def vert_Spacer(a, b, c):
            verticalSpacer = QSpacerItem(b, c, QSizePolicy.Maximum, QSizePolicy.Expanding)
            a.addItem(verticalSpacer, 3, 0)
            a.addItem(verticalSpacer, 3, 3)


        # A function for creating scroll objects
        # gets the tab/location the scroll is to be inserted as location
        # gets the x and y coordinates as x and y
        global scroll
        def scrollBuilder(location, x, y):
            global scroll
            scroll = QScrollArea(self)

            # Creating the style sheet for the scroll bar colors.


            location.addWidget(scroll, x, y)
            scroll.setWidgetResizable(True)
            #scroll.setMinimumHeight(50)
            scrollContent = QWidget(scroll)
            scroll.layout = QGridLayout(scrollContent)
            scrollContent.setLayout(scroll.layout)

            scroll.setWidget(scrollContent)

        # A function that builds headers
        # (a) is the message string
        # (b) is the first position variable
        # (c) is the second position variable
        # (d) is the layout that the label is to be added to
        # (e) is the amount of height given to the header
        def headerBuild(a, b, c, d, e):

            self.header = QLabel(a, self)
            self.header.setAlignment(QtCore.Qt.AlignCenter)
            self.header.setFixedHeight(e)
            self.header.setWordWrap(True)
            self.header.setFont(fontVar)
            self.header.setStyleSheet('QLabel {background: transparent}')
            d.addWidget(self.header, b, c)



        # A quick Qlabel generator
        # (stringVar) is the string to be displayed
        # (xCord and yCord) are the coordinates the label is to be placed at
        # (layout) is the object the label is to be placed in.
        def genLabel(stringVar,xCord, yCord, layout):
            # Creating the black screen explanation label
            self.label = QLabel(stringVar, self)
            self.label.adjustSize()
            self.label.setWordWrap(True)
            self.label.setMaximumWidth(450)
            self.label.setFont(basicFont)
            frameLayout.addWidget(self.label, xCord, yCord)

        # Adding the most recent Label
        def get_recent():
            astroNinjaV85.armStrong()
            astroNinjaV85.nextFlight.append('Ah')
            global recentMessage
            recentMessage = "{}\n\n{}\n\n{}\n\n{}".format(astroNinjaV85.nextFlight[0], astroNinjaV85.nextFlight[1], astroNinjaV85.nextFlight[2], astroNinjaV85.nextFlight[3])
            self.nextLaunch = QLabel(recentMessage, self)
            self.nextLaunch.setWordWrap(True)
            self.nextLaunch.setMaximumWidth(800)
            self.nextLaunch.setFont(welcomeFont)
            #self.nextLaunch.setAlignment(QtCore.Qt.AlignCenter)
            #self.nextLaunch.resize(30, 30)
            frameLayout.addWidget(self.nextLaunch, 1, 1)
            return recentMessage

        # A function that searches the string in nextFlight[2] for space agency names and displays the agency's logo with the launch data in the next launch.
        # V0.70, added the need for arguement x, which is the item that is to be searched
        def choose_Icon(x):
            global nextLogo
            nextLogo = ''
            if 'SpaceX' in x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/spacex.png")
            elif 'Chinese' in x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/china.png")
            elif 'United Launch Alliance' in x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/ula.png")
            elif 'Arianespace' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/ariane.png")
            elif 'India' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/india.png")
            elif 'Rocket Lab' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/rocketlab.png")
            elif 'Japan' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/Japan.png")
            elif 'Russian' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/russia.png")
            elif 'Pegasus' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/nasa2.png")
            elif 'Eurockot' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/eurockot.png")
            elif 'International Launch Services' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/ILS.png")
            elif 'Northrop Grumman' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/northop.png")
            elif 'Virgin Orbit' in  x:
                nextLogo = os.path.expanduser("~/.AstroNinja/Images/Logos/virginorbit.png")
            else:
                nextLogo = ''
            return nextLogo

        # a function to ad an agency logo to the launch schedule item
        # gets the tab layout it is to be added to as tab
        # a and b are positions for the icon
        # search item is the item choose_Icon() is to search

        def recent_logo(tab, a, b, searchItem):
            choose_Icon(searchItem)
            self.nextLogo = QLabel(self)
            self.nextLogo.setStyleSheet('QLabel {background: transparent}')
            iconPix = QPixmap(nextLogo)
            self.nextLogo.setPixmap(iconPix)
            self.nextLogo.setAlignment(QtCore.Qt.AlignCenter)
            self.nextLogo.setMaximumWidth(400)

            #self.nextLaunch.resize(30, 30)
            tab.addWidget(self.nextLogo, a, b)


        # A function that create graphs from data passed from backend modules.
        # takes the tally data as tallies
        # takes the unique label for the yLabel as ylabelString
        # takes a string as title
        # takes org list as launchers
        # takes the container it is to be placed in as container
        # and takes x, y placement in the container as x,y

        def graph_maker(tallies, ylabelString, title, launchers, container, x, y):

            self.figure = plt.figure(figsize=(11,5))
            ax = self.figure.add_subplot(111)

            self.canvas = FigureCanvas(self.figure)

            container.addWidget(self.canvas, x, y)

            # Changing the graph colors based on which theme is selected:
            global bg_color, fg_color, bar_color

            if themeSelected == 'marine':
                bg_color = 'White'
                fg_color = 'black'
                bar_color = 'Darkslategray'

            if themeSelected == 'spaceX':
                bg_color = 'White'
                fg_color = 'black'
                bar_color = 'Steelblue'

            if themeSelected == 'broco':
                bg_color = 'black'
                fg_color = 'white'
                bar_color = 'DarkTurquoise'

            # x-coordinates
            xItems = 11
            ind = np.arange(xItems)


            p1 = plt.bar(ind, tallies) #setting the plot

            for item in p1:
                item.set_color(bar_color)

            plt.ylabel(ylabelString, color=fg_color)
            plt.xlabel('Organizations/Nations', color=fg_color)
            plt.title(title, fontsize=17, color=fg_color)
            plt.xticks(ind, launchers, color=fg_color)
            if max(tallies) == 0:
                    plt.yticks(np.arange(0, 2), color=fg_color)
            else:
                plt.yticks(np.arange(max(tallies) + 2), color=fg_color)

            #plt.style.use(u'dark_background')
            ax.patch.set_facecolor(bg_color)
            #ax.autoscale(enable=True)
            ax.tick_params(axis='x', labelsize=8)
            self.figure.patch.set_facecolor(bg_color)

            # Adding the totals to the bars
            for index,data in enumerate(tallies):
                plt.text(x=index , y =data-data , s=f"{data}" , fontdict=dict(fontsize=8, ha='center', va='bottom', color=bg_color))
            self.canvas.draw()


        # A function that creates web objects, kind of a way to build a webpage into a widget.

        def web_wrapper(urlItem, maxHeight, container, xPos, yPos):

            self.webView = QtWebEngineWidgets.QWebEngineView()     # creating the webengine object
            self.webView.setUrl(QUrl(urlItem))         # setting the URL
            self.webView.adjustSize()
            self.webView.setMinimumHeight(maxHeight)

            container.addWidget(self.webView, xPos, yPos)

        # A better function to create label widgets in PyQt5.
        # Takes the string to be shown as message.
        # Justification is set with alignment,
        # font size is set with font
        # width sets maximum width of the label.
        # container is where the label is to be placed.
        def label_maker(message, alignment, font, width, container, xpos, ypos):

            self.label = QLabel(message, self)
            self.label.adjustSize()
            self.label.setWordWrap(True)
            self.label.setAlignment(alignment)
            self.label.setMaximumWidth(width)
            self.label.setFont(font)

            container.addWidget(self.label, xpos, ypos)


        #==========================================================================================
        # Creating the first tab. The welcome tab that contains a welcome message, the next launch,
        # and the graph showing launches remaining.
        #==========================================================================================

        # Configuring the tab's layout
        self.welcomeTab.layout =  QGridLayout(self)
        #self.welcomeTab.layout.setRowStretch(1, 5)

        # Building the scrollbars
        firstScroll = scrollBuilder(self.welcomeTab.layout, 1, 1)

        # Creating the Welcome header using headerBuild()
        welcome = "Welcome To AstroNinja!   "
        headerBuild(welcome, 0, 1, self.welcomeTab.layout, 50)

        # Adding a verticle spacer
        vert_Spacer(scroll.layout, 250, 250)

        # Adding Horizontal spacers inbetween frame items
        horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum)          # Top H spacer
        scroll.layout.addItem(horizSpacer, 0, 1)
        horizSpacer = QSpacerItem(20, 20, QSizePolicy.Maximum)          # Resizing for middle spacers
        scroll.layout.addItem(horizSpacer, 2, 1)
        scroll.layout.addItem(horizSpacer, 4, 1)
        scroll.layout.addItem(horizSpacer, 6, 1)
        # Building the frame to put the next launch icon and description
        frameBuilder(scroll.layout, 1, 1, 750, False)
        # Running the function that uses the backend module that scrapes the data needed
        # to display the next launch. Also builds the label object
        headerBuild("Next Launch\n", 0, 1, frameLayout, 50)
        self.header.setAlignment(QtCore.Qt.AlignLeft)

        get_recent()
        # Choosing the right agency logo and placing it in the frame
        recent_logo(frameLayout, 1, 0, recentMessage)


        #================================================================================================
        # Attempting to add a YouTube stream as an object in the first tab
        #================================================================================================

        # Running the backend function that get's the url of the embed version of the newest
        # video by the SpaceX youtube channel.
        # Also will enable the livestreaming of launches.

        # Building the SpaceX Lens object
        frameBuilder(scroll.layout, 3, 1, 750, False)
        frameLayout.addItem(horizSpacer, 1, 1)
        vert_Spacer(frameLayout, 20, 20)

        # Building the webObject using the web_wrapper() function added with V0.85.
        web_wrapper(youtubeTest.fullURL, 700, frameLayout, 2, 1)
        frameLayout.addItem(horizSpacer, 3, 1)

        # building the header frame
        frameBuilder(frameLayout, 0, 1, 650, False)
        self.frame.setLineWidth(5)
        windowMessage = "SpaceX Lens"
        headerBuild(windowMessage, 0, 0, frameLayout, 50)
        # The mission name header
        missionTitle = "%s" % youtubeTest.newestName
        headerBuild(missionTitle, 0, 2, frameLayout, 50)
        """
            Use a smaller font for the mission title if it's
            longer than 25 char. This prevents cutting off of
            parts of the header.
        """
        if len(missionTitle) >= 25:
            self.header.setFont(smallerHeader)

        # Building a Verticle divider Item with QFrame()
        vDivider  = QFrame()
        vDivider.setFrameShape(QFrame.VLine)
        vDivider.setLineWidth(3)
        frameLayout.addWidget(vDivider, 0, 1)

        #============================================================================================================================
        # Adding the Mars Weather service to AstroNinja.
        # A simple embed using QtWebEngineWidgets as a container.
        # Added in Version 0.85
        #============================================================================================================================

        # Building the Mars Meteorologist  Object
        frameBuilder(scroll.layout, 4, 1, 750, False)
        frameLayout.addItem(horizSpacer, 1, 1)
        vert_Spacer(frameLayout, 20, 20)
        web_wrapper("https://mars.nasa.gov/layout/embed/image/insightweather/", 720, frameLayout, 2, 1)
        frameLayout.addItem(horizSpacer, 3, 1)

        # building the header frame
        frameBuilder(frameLayout, 0, 1, 650, False)
        self.frame.setLineWidth(5)

        marsTitle = "Mars Weather Service"
        headerBuild(marsTitle, 0, 0, frameLayout, 50)

        #=============================================================================================================================
        # Creating the graph that shows launches remaining.
        # Moved from own tab in Version 0.70
        #=============================================================================================================================
        # counters for the tallying funtion
        global monthCount
        global missionCount
        monthCount = 0                                   # For iterating over the launchHead2 Items
        missionCount = 3                                 # For iterating over the descriptionMissfin items
        astroGraphV85.tally_ho(monthCount, missionCount)    # the meat and bones of the graph feature

        # the tallies
        remainingTallies = [astroGraphV85.spaceXCount, astroGraphV85.chinaCount, astroGraphV85.japaneseCount, astroGraphV85.ulaCount, astroGraphV85.rocketCount, astroGraphV85.indiaCount, astroGraphV85.arianeCount, astroGraphV85.russiaCount, astroGraphV85.northCount, astroGraphV85.euroCount, astroGraphV85.virginCount]

        # The Organizations
        orgs = ('SpaceX', 'China', 'JAXA', 'ULA', 'Rocket\nLabs', 'India', 'ArianeSpace', 'Russia', 'Northrop', 'Eurockot', 'Virgin\nOrbital')

        graph_maker(remainingTallies, 'Launches Remaining', 'Launches Remaining for This Month by Organization\n', orgs, scroll.layout, 6, 1)
        #=============================================================================================================================
        # Creating the second graph that shows total launches so far for the year
        # added in Version 0.80
        #=============================================================================================================================

        # Running function that scrapes launch history in the backend module
        astroGraphV85.historian('2020')

        # The tallies
        historyTallies = [astroGraphV85.spaceXCount, astroGraphV85.chinaCount, astroGraphV85.ulaCount, astroGraphV85.indiaCount, astroGraphV85.rocketCount, astroGraphV85.japaneseCount, astroGraphV85.arianeCount, astroGraphV85.russiaCount, astroGraphV85.northCount, astroGraphV85.blueOrigin, astroGraphV85.ilsCount]

        # The Organizations
        orgs = ('SpaceX', 'China', 'ULA', 'India', 'Rocket\nLabs', 'Japan', 'Ariane\nSpace', 'Russia', 'Northrop', 'Blue\nOrigin', 'ILS')

        graph_maker(historyTallies, 'Launch Totals', 'Total Launches For 2020 by Organization\n', orgs, scroll.layout, 7, 1)
        #=================================================================================================
        # Creating the third graph, which shows  the total launches for the previous year
        # Added V0.85
        #=================================================================================================

        # Running function that scrapes launch history in the backend module
        astroGraphV85.historian('2019')

        # The tallies
        historyTallies = [astroGraphV85.spaceXCount, astroGraphV85.chinaCount, astroGraphV85.ulaCount, astroGraphV85.indiaCount, astroGraphV85.rocketCount, astroGraphV85.japaneseCount, astroGraphV85.arianeCount, astroGraphV85.russiaCount, astroGraphV85.northCount, astroGraphV85.blueOrigin, astroGraphV85.ilsCount]

        graph_maker(historyTallies, 'Launch Totals', 'Total Launches For 2019 by Organization\n', orgs, scroll.layout, 8, 1)

        self.welcomeTab.setLayout(self.welcomeTab.layout)
        #=================================================================================================
        # The second tab, which contains the complete launch schedule.
        #=================================================================================================

        # Configuring the tab
        self.scheduleTab.layout = QGridLayout()
        # Building the header
        scheduleHeader = "Launch Schedule"
        headerBuild(scheduleHeader, 0, 0, self.scheduleTab.layout, 50)



        # Running the schedule scraping function from the astroNinja module
        astroNinjaV85.getSchedule()
        astroNinjaV85.scheduleList.append('Ah')

        # A function that adds verticle margins to layouts
        # Takes the layout it is to be added to as "a"
        # "b" and "c" are the x and y dimensions
        def vert_Spacer(a, b, c):
            verticalSpacer = QSpacerItem(b, c, QSizePolicy.Maximum, QSizePolicy.Expanding)
            a.addItem(verticalSpacer, 2, 0)
            a.addItem(verticalSpacer, 2, 4)

        # Building the scroll bar for the schedule. scrollBuilder() added V.75
        scrollBuilder(self.scheduleTab.layout, 1, 0)
        # A function to automate the adding of schedule items and their icons to the launch schedule.
        def launch_scheduleBuild(a, b, c, d, e):

            # Building the frame for the item created by launch_scheduleBuild()
            frameBuilder(scroll.layout, e, 1, 300, False)
            # Building the label
            scheduleItem = "{}\n\n{}\n\n{}\n\n{}\n\n".format(astroNinjaV85.scheduleList[a],astroNinjaV85.scheduleList[b],astroNinjaV85.scheduleList[c],astroNinjaV85.scheduleList[d])
            label_maker(scheduleItem, QtCore.Qt.AlignLeft, basicFont, 800, frameLayout, 0, 0)

            #frameLayout.addWidget(self.itemLabel)
            scroll.layout.addWidget(self.frame, e, 2)

            # getting the agency logo for each item
            recent_logo(scroll.layout, e, 1, scheduleItem)



        # calling launch_scheduleBuild() for the schedule entries. the first three arguments correspond with
        # items from the scheduleList in the back end module.
        #
        # The last arguement correspond with the item number in the schedule, and set what position the item
        # appears in.


        # The variables that are to be used to advance launch_scheduleBuild through each schedule item
        # Must be declared as global outside of iterator function and within it
        global firstCount, secondCount, thirdCount, fourthCount, position

        skipCount = 0
        firstCount = 0
        secondCount = 1
        thirdCount = 2
        fourthCount = 3
        position = 1
        # Running the function that updates the date variable of the first shedule item
        astroNinjaV85.update_launch(skipCount)

        """
            Iterate through each schedule item while each date is older than
            todays.
        """
        while astroNinjaV85.comparedList[0] > astroNinjaV85.comparedList[1]:
            skipCount += 1
            firstCount += 4
            secondCount += 4                        # advance by 4 to skip to the next launch in scheduleList
            thirdCount += 4
            fourthCount += 4
            astroNinjaV85.update_launch(skipCount)     # update to the next schedule item
                                                    # after iterating the counter

        # building a function that iterates through schedule items and builds each
        # one into it's own UI item
        def schedule_iterator(a, b, c, d, e):
            launch_scheduleBuild(a, b, c, d, e)
            global firstCount, secondCount, thirdCount, fourthCount, position
            firstCount += 4
            secondCount += 4                        # advance by 4 to skip to the next launch in scheduleList
            thirdCount += 4
            fourthCount += 4
            position += 1
            return

        # run the iterator until it reaches the end of the schedule list provided by the backend
        while fourthCount < len(astroNinjaV85.scheduleList):
            schedule_iterator(firstCount, secondCount, thirdCount, fourthCount, position)

        vert_Spacer(scroll.layout, 250, 250)
        self.scheduleTab.setLayout(self.scheduleTab.layout)

        #============================================================================================================================
        # The News tab, showing news articles scraped by xNews.py
        #============================================================================================================================

        self.spacexTab.layout =  QGridLayout()

        newsRun = xNewsV85.intestellar_News(sortingSelected)

        # Building the scroll bar for the schedule. scrollBuilder() added V.75
        scrollBuilder(self.spacexTab.layout, 0, 0)

        # An function based on launch_scheduleBuild that builds out the list of articles in the GUI
        # a is the position of the item in titleList
        # b is the position of the item in bodyList
        # c is the position of the item in the gui.
        # d is the position of the item in imageList
        # e is the position of the item in listedDate
        def newsListBuilder(a, b, c, d, e):

            # Removing unwanted articles from space.com
            naughtyArticles = ['Pictures from Space!', 'The top space stories of the week!']                        # The list of articles to look for
            if naughtyArticles[0] in xNewsV85.listedTitle[a] or naughtyArticles[1] in xNewsV85.listedTitle[a]:      # if the title matches one of naughtyArticles
                # Ends and moves on to the next article if found.
                return

            else:

                # Building the frame for the item created by launch_scheduleBuild()
                frameBuilder(scroll.layout, c, 1, 1000, False)


                # Building the label
                dateVar = "Date Written: {}\n".format(xNewsV85.listedDate[e])
                titleVar = "{}".format(xNewsV85.listedTitle[a])
                bodyVar = "{}\n\n".format(xNewsV85.listedBody[b])
                # setting the label for the title of the article
                headerBuild(titleVar, 0, 2, frameLayout, 150)

                self.image= QLabel(self)

                """
                    Creating a class that masks the scraper as Mozilla browser.
                    Gets around Admins blocking urllib scrapers on their websites.
                """
                class AppURLopener(urllib.request.FancyURLopener):
                    version = "Mozilla/5.0"

                opener = AppURLopener()



                # FIXED IN VERSION 0.85: fixes inability to load urls that contain
                # non-unicode characters by using the parse module in the urllib library.
                # Uses urllib.parse.quote to correctly quote/escape unicode characters
                picUrl = xNewsV85.listedImg[d]

                if len(picUrl) == 0:

                    horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
                    frameLayout.addItem(horizSpacer, 1, 2)
                    frameLayout.addItem(horizSpacer, 2, 2)

                    # Setting the label for the date of the article.
                    label_maker(dateVar, QtCore.Qt.AlignLeft, basicFont, 900, frameLayout, 3, 2)

                    # setting the label for the body of the article
                    label_maker(bodyVar, QtCore.Qt.AlignLeft, basicFont, 900, frameLayout, 4, 2)


                    # Adding verticle spacing
                    vert_Spacer(scroll.layout, 250, 250)

                else:
                    picUrl = list(urllib.parse.urlsplit(picUrl))
                    picUrl[2] = urllib.parse.quote(picUrl[2])
                    picUrl = urllib.parse.urlunsplit(picUrl)



                    response = urllib.request.urlopen(picUrl)

                    # TO-DO: Test if this is no longer necessary if unicode characters are fixed.
                    if '\u2014' not in xNewsV85.listedImg[d]:
                        data = response.read()

                        artmap = QPixmap()
                        artmap.loadFromData(data)
                        artmap = QPixmap(artmap).scaled(700, 900, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        self.image.setPixmap(artmap)
                        self.image.setAlignment(QtCore.Qt.AlignCenter)
                        self.image.adjustSize()
                        frameLayout.addWidget(self.image, 2, 2)
                        # Adding a space to further seperate the article image and body
                        horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
                        frameLayout.addItem(horizSpacer, 1, 2)
                        frameLayout.addItem(horizSpacer, 3, 2)

                        # Setting the label for the date of the article.
                        label_maker(dateVar, QtCore.Qt.AlignLeft, basicFont, 900, frameLayout, 4, 2)


                        # setting the label for the body of the article
                        label_maker(bodyVar, QtCore.Qt.AlignLeft, basicFont, 900, frameLayout, 5, 2)


                        # Adding verticle spacing
                        vert_Spacer(scroll.layout, 250, 250)
                    else:
                        return

        # Building an iterator for working through items passed by the backend module
        global countKeeper, positionKeeper
        countKeeper = 0
        positionKeeper = 0
        def iterator(a, positionvar):
            global countKeeper
            global positionKeeper

            # Removing unwanted articles from space.com
            naughtyArticles = ['Pictures from space!', 'The top space stories of the week!']                        # The list of articles to look for
            if naughtyArticles[0] in xNewsV85.listedTitle[a] or naughtyArticles[1] in xNewsV85.listedTitle[a]:      # if the title matches one of naughtyArticles
                #newsListBuilder(a, a, positionvar, a)
                countKeeper += 1

            else:
                newsListBuilder(a, a, positionvar, a, a)
                countKeeper += 1
                positionKeeper += 1

            return

        # Build the news list until we reach the end of the data
        while countKeeper < len(xNewsV85.listedTitle):
            iterator(countKeeper, positionKeeper)

        self.spacexTab.setLayout(self.spacexTab.layout)

        #======================================================================================
        # The Hubble Views tab, which shows the shot of the weeks from the Hubble
        # Space Telescope
        #======================================================================================

        self.hubbleTab.layout = QGridLayout()

        # Building the scroll bar. scrollBuilder() added V.75
        scrollBuilder(self.hubbleTab.layout, 0, 0)

        xNewsV85.hubbleViewz(HubblesortingSelected)
        xNewsV85.images.append('Ah')
        xNewsV85.descriptions.append('Ah')
        xNewsV85.headers.append('ah')

        def hubbleViewBuilder(b, c, d):

            # Building the frame for the item created by launch_scheduleBuild()
            frameBuilder(scroll.layout, c, 1, 1000, False)

            # Building the label
            bodyVar = "\n\n\t{}".format(xNewsV85.descriptions[b])
            # setting the label for the title of the article

            self.image= QLabel(self)
            data = urllib.request.urlopen(xNewsV85.images[d]).read()
            artmap = QPixmap()
            artmap.loadFromData(data)
            self.image.setPixmap(artmap)
            self.image.setAlignment(QtCore.Qt.AlignCenter)
            self.image.adjustSize()
            frameLayout.addWidget(self.image, 1, 1)
            # Adding a space to further seperate the article image and body
            horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
            frameLayout.addItem(horizSpacer, 0, 2)
            frameLayout.addItem(horizSpacer, 3, 2)

            #vert_Spacer(frameLayout, 100, 100)
            # setting the label for the body of the article
            frameBuilder(frameLayout, 1, 3, 600, True)

            # Building the header
            headerBuild(xNewsV85.headers[b], 0, 0, frameLayout, 70)

            """
                Use a smaller font for the mission title if it's
                longer than 25 char. This prevents cutting off of
                parts of the header.
            """
            if len(xNewsV85.headers[b]) >= 25:
                self.header.setFont(smallerHeader)

            # Generating the Description label.
            label_maker(bodyVar, QtCore.Qt.AlignLeft, basicFont, 600, frameLayout, 1, 0)





        vert_Spacer(scroll.layout, 250, 250)



        global hubKeeper
        hubKeeper = 0
        def hubIterator(x):
            hubbleViewBuilder(x, x, x)
            global hubKeeper
            hubKeeper += 1
            return

        while hubKeeper < 16:
            hubIterator(hubKeeper)

        self.hubbleTab.setLayout(self.hubbleTab.layout)

        #==========================================================================================
        # Creating the fifth tab. The ISS Portal that contains a livestream from the space station,
        # Experiment info, and crew information. added V0.85
        #==========================================================================================

        # Configuring the tab's layout
        self.issTab.layout =  QGridLayout(self)

        # Building the scrollbars
        scrollBuilder(self.issTab.layout, 0, 0)

        self.issView = QtWebEngineWidgets.QWebEngineView()     # creating the webengine object
        self.issView.setUrl(QUrl("https://www.ustream.tv/embed/17074538?html5ui"))         # setting the URL to the one scraped by testFlight()
        self.issView.setMinimumWidth(900)
        # Building the SpaceX Lens object
        frameBuilder(scroll.layout, 0, 1, 750, False)
        vert_Spacer(scroll.layout, 150, 50)
        frameLayout.addWidget(self.issView, 2, 0)
        horizSpacer = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Expanding)
        frameLayout.addItem(horizSpacer, 3, 0)


        # building the header frame
        windowMessage = "                           ISS Window                        "
        headerBuild(windowMessage, 0, 0, frameLayout, 50)

        frameBuilder(frameLayout, 2, 1, 450, True)              # Creating the inner frame
        self.frame.setLineWidth(5)

        headerMessage = "HDEV Camera Description"
        technicalDescrip = "\tActivated on April 30, 2014, the primary purpose of the High Definition Earth-Viewing System (HDEV) is to monitor the rate at which HD video image quality degrades when exposed to the harsh environment of space, mainly cosmic ray damage. Unfortunatly, the HDEV experiment reached End of Life in 2019, but rejoice space fans! The project maintainers continue to keep previously recorded video available.\n\tThe cameras cycle from one to the next, providing a view looking forward, one straight down on our gorgeous home, and 2 looking back for that rear-facing perspective. You may even spot a docked vehicle or two!\n"
        blackHead = "Why is the window black?\n"
        descrip = "\tDon't fear! The ISS is currently passing over the night side of the Earth. The view usually brightens again a few minutes, and sometimes we're treated with a sunrise!"
        powerHead = "What is this screen?\n"
        screenDesc = "\tIf a screen that looks more like a PowerPoint slide is greeting you, don't fret! The system is only switching cameras or the feed has lost contact with home. The stream is still working, and the view will return."
        headerBuild(headerMessage, 0, 0, frameLayout, 100)


        welcomeFont.setBold(True)
        # Creating the label for the technical description of HDEV
        label_maker(technicalDescrip, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 1, 0 )


        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 2, 0)

        # Creating the label with the black header
        label_maker(blackHead, QtCore.Qt.AlignCenter, welcomeFont, 450, frameLayout, 3, 0)


        # Creating the black screen explanation label
        label_maker(descrip, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 4, 0)


        hDivider  = QFrame()
        hDivider.setFrameShape(QFrame.HLine)
        hDivider.setLineWidth(3)
        frameLayout.addWidget(hDivider, 5, 0)

        # Creating the label with the power point head
        label_maker(powerHead, QtCore.Qt.AlignCenter, welcomeFont, 450, frameLayout, 6, 0)


        # Creating the black screen explanation label
        #self.screenLabel = QLabel(screenDesc, self)
        #self.screenLabel.adjustSize()
        #self.screenLabel.setWordWrap(True)
        #self.screenLabel.setMaximumWidth(450)
        #self.screenLabel.setFont(basicFont)
        #frameLayout.addWidget(self.screenLabel, 7, 0)
        label_maker(screenDesc, QtCore.Qt.AlignLeft, basicFont, 450, frameLayout, 7, 0)
        #horizSpacer = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Expanding)
        #frameLayout.addItem(horizSpacer, 3, 2)

        """
            Building the current residents section

        """
        issPortal.rollCall()

        frameBuilder(scroll.layout, 1, 1, 750, False )

        # the header
        crewHead = "Current ISS Residents                                                         Expedition 63"
        #self.resLabel = QLabel("Current ISS Residents\n\nExpedition 62", self)
        headerBuild(crewHead, 1, 1, frameLayout, 70)


        # Displaying the expidition patch with each bio
        self.expeditionLogoLarge = QLabel(self)
        exPixLarge = QPixmap(os.path.expanduser("~/.AstroNinja/Images/Logos/issLogoLarge.png"))
        self.expeditionLogoLarge.setPixmap(exPixLarge)
        self.expeditionLogoLarge.setAlignment(QtCore.Qt.AlignCenter)
        #self.expeditionLogo.setMaximumWidth(60)
        self.expeditionLogoLarge.setMargin(0)

        frameLayout.addWidget(self.expeditionLogoLarge, 0, 1)

        scrollBuilder(frameLayout, 2, 1)

        vert_Spacer(scroll.layout, 150, 50)         # spacer that goes around profiles.

        scroll.setMinimumHeight(900)
        # This function builds the gui item for each resident's profile
        # takes iteratorY for iterating through each astronaut's data and for setting the Y position in the layout
        # Takes iteratorX as a counter for facilitating the moving on to a new column as needed in the layout.
        def profileBuilder(crewVar, iteratorY):

            # Building the outer frame

            frameBuilder(scroll.layout, iteratorY, 1, 200, True)
            #self.frame.setMaximumWidth(900)
            #building the label for the bio
            smallItems = "Place of Birth: {}\n\nNationality: {} {}".format(issPortal.crewLocation[crewVar], issPortal.crewNat[crewVar], issPortal.shortBio[crewVar])
            genLabel(smallItems, 1, 1, frameLayout)
            self.label.setMargin(0)
            self.label.setMinimumWidth(700)
            genLabel(issPortal.shortBio2[crewVar], 2, 1, frameLayout)
            self.label.setMargin(0)
            self.label.setMinimumWidth(700)

            # Adding spacers to the layout
            horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum, QSizePolicy.Expanding)
            frameLayout.addItem(horizSpacer, 4, 1)
            vert_Spacer(frameLayout, 200, 200)


            # Building the inner frame
            frameBuilder(frameLayout, 0, 1, 200, True)
            self.frame.setMaximumHeight(800)     # setting maximum height
            #self.frame.setAlignment(QtCore.Qt.AlignCenter)
            # building the image object for the portrait
            self.image = QLabel(self)
            image = urllib.request.urlopen(issPortal.crewImg[crewVar]).read()
            artmap = QPixmap()
            artmap.loadFromData(image)
            self.image.setPixmap(artmap)
            self.image.setAlignment(QtCore.Qt.AlignCenter)
            self.image.adjustSize()
            frameLayout.addWidget(self.image, 1, 0)

            # Displaying the expidition patch with each bio
            self.expeditionLogo = QLabel(self)
            exPix = QPixmap(os.path.expanduser("~/.AstroNinja/Images/Logos/issLogo.png")).scaled(60, 60, QtCore.Qt.KeepAspectRatio)
            self.expeditionLogo.setPixmap(exPix)
            #self.expeditionLogo.setAlignment(QtCore.Qt.AlignRight)
            self.expeditionLogo.setMaximumWidth(60)
            self.expeditionLogo.setMargin(0)

            frameLayout.addWidget(self.expeditionLogo, 0, 1)
            # the header that contains the astronaut's name
            headerBuild(issPortal.crewName[crewVar], 0, 0, frameLayout, 70)
            self.label.setMargin(0)
            vert_Spacer(frameLayout, 70, 20)
            return

        global crewIt, xIt
        # crewIt is for iterating through crew members
        crewIt = 0

        # xIt is for iterating through x coordinates
        xIt = 2

        # The function that runs profileBuilder and iterates to the next crew profile.
        # takes the above iterator variables as arguments
        def crewIterator(crew, x):

            profileBuilder(crew, x)
            global crewIt, xIt

            # advancing the variables to advance to the next crew member
            crewIt += 1
            xIt += 1

            return

        while crewIt != len(issPortal.crewName):
            crewIterator(crewIt, xIt)


        # Keep at bottom of tab section. needed for the tab to showup.
        self.issTab.setLayout(self.issTab.layout)


        # Add tabs to widget
        grid_layout.addWidget(self.tabs)
        #=======================================================================
        # Creating the menu bar and its entries.
        #=======================================================================


        iconList = [os.path.expanduser("~/.AstroNinja/Images/Icons/exit.png"), os.path.expanduser("~/.AstroNinja/Images/Icons/about.png"), os.path.expanduser("~/.AstroNinja/Images/Icons/information.png"), os.path.expanduser("~/.AstroNinja/Images/Icons/refresh.png")]


        # The menu item builder
        # takes an image from iconLst as image
        # toggles icons off with iconToggle
        # takes the tool tip as statusTip
        # gets the item's name as menuName
        # method is the function to be run when clicked
        def buildMenuItemAction(image, iconToggle, statusTip, menuName, method):

            if iconToggle is True:
                item = QAction(QIcon(image), menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item
            else:
                item = QAction(menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item


        toggler = True
        exitAct = buildMenuItemAction(iconList[0], toggler, "Exit Application", "&Exit", qApp.quit)                               # Exit option
        aboutAct = buildMenuItemAction(iconList[1], toggler, "Build Information", "&About", clickMethod)                          # About Option
        sourceAct = buildMenuItemAction(iconList[2], toggler, "List of Sources Used By AstroNinja", "&Sources", sourceMethod)     # Sources option
        refreshAct = buildMenuItemAction(iconList[3], toggler, "Refreshes The Window", "&Reload", restart_program)                # Refresh option
        toggler = False                                                                                                           # The rest of the options have no icons
        marineAct = buildMenuItemAction(iconList[0], toggler, "A More Subtle Theme", "&Marine", Marine)                           # Default Theme
        spacexAct = buildMenuItemAction(iconList[0], toggler, "A Theme based On SpaceX and The Default Theme", "&SpaceX", Spacex) # SpaceX Theme
        brocoAct = buildMenuItemAction(iconList[0], toggler, "A Vaporwave Theme For Dark Mode", "&Broco", broco)                  # Broco Theme
        newestAct = buildMenuItemAction(iconList[0], toggler, "Sort News Articles by Newest", "&Newest", newest)
        oldestAct = buildMenuItemAction(iconList[0], toggler, "Sort News Articles by Oldest Date", "&Oldest", oldest)
        newesthubAct = buildMenuItemAction(iconList[0], toggler, "Sort Hubble Images by Newest", "&Newest", newestHubble)
        oldesthubAct = buildMenuItemAction(iconList[0], toggler, "Sort Hubble Images by Oldest Date", "&Oldest", oldestHubble)
        # Adding a menubar.
        menubar = self.menuBar()


        if themeSelected == 'marine':
            astroThemesV85.defaultMenu(menubar)    # TESTING the function for the default menubar theme
        if themeSelected == 'spaceX':
            astroThemesV85.spacexMenu(menubar)
        if themeSelected == 'broco':
            astroThemesV85.brocoMenu(menubar)
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(refreshAct)
        fileMenu.addAction(sourceAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        # Adding a Settings menu to the menu bar.
        settingsMenu = menubar.addMenu('&Settings')
        themeMenu = settingsMenu.addMenu('&Themes')
        themeMenu.addAction(marineAct)
        themeMenu.addAction(spacexAct)
        themeMenu.addAction(brocoAct)

        # Adding an Article Sorting menu to the settings menu.
        sortingMenu = settingsMenu.addMenu('&Article Sorting')
        sortingMenu.addAction(newestAct)
        sortingMenu.addAction(oldestAct)

        hubbleMenu = settingsMenu.addMenu('&Hubble Image Sorting')
        hubbleMenu.addAction(newesthubAct)
        hubbleMenu.addAction(oldesthubAct)

        self.statusBar()
        self.showMaximized()
        #self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    #self.show()
    sys.exit(app.exec_())
