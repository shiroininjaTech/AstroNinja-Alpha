from __future__ import unicode_literals

"""
   This the Library file for the backend modules for AstroNinja, a space launch tracker and space news app for the
   Linux desktop. It scrapes data from spacelaunchnow.com and displays it in an interactive GUI using beautiful soup
   and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.50
   * Date Created: 10/03/17
   * Date Modified: 05/22/19
"""
"""
   * Changelog:
   * Version 0.10: Added iteration to armStrong and getSchedule function to fix formatting.
   * Version 0.50: Added Space agency logos to the next launch data on welcome tab
"""

import re
import requests, bs4
import time, os
from datetime import date
import calendar
from dateutil import parser
#import threading
#from queue import Queue
my_date = date.today()

#====================================================================================================================
# The next Launch scheduled Functions
#====================================================================================================================

def armStrong():

    # Getting the website and making sure we've made contact :P
    spaceFlight = requests.get('https://spaceflightnow.com/launch-schedule/')
    spaceFlight.raise_for_status()

    # Now that we have the website loaded, let's parse it with Beautiful Soup (why not Ugly soup??)
    global flyingSoup
    flyingSoup = bs4.BeautifulSoup(spaceFlight.text, "lxml")

    def update_launch(counter):
        # Getting the Date and Mission name
        dateName = flyingSoup.find_all(class_="launchdate")

        global dateName2
        dateName2 = dateName[counter].getText()
        #print(dateName2)

        if 'NET' in dateName2 and '/' in dateName2:
            noNet = dateName2[4:]

            fixer = re.sub(r'/.*', '', noNet)
            print(fixer)
            dateChange = parser.parse(fixer)
            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)

        elif '/' in dateName2:
            fixer = re.sub(r'/.*', '', dateName2)
            #print(fixer)
            dateChange = parser.parse(fixer)

            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)

        elif 'TBD' in dateName2 or 'First Quarter' in dateName2:
            dateFake = 'January'
            dateChange = parser.parse(dateFake)
            changedateStr = str(dateChange)

        elif 'NET' in dateName2:
            noNet = dateName2[4:]

            dateChange = parser.parse(noNet)
            changedateStr = str(dateChange)

        elif 'Early' in dateName2:
            notEarly = dateName2[6:]
            changedateStr = str(parser.parse(notEarly))

        elif 'Late' in dateName2:
            notLate = dateName2[5:]
            dateChange = parser.parse(notLate)
            changedateStr = str(dateChange)

        elif 'Mid' in dateName2:
            noMids = dateName2[4:]
            dateChange = parser.parse(noMids)
            changedateStr = str(dateChange)
        else:
            #print(dateName2)
            dateChange = parser.parse(dateName2)
            #print(dateChange)
            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)

        global todaydateStr
        global changedSlice
        changedSlice = changedateStr[0:10]
        todaydateStr = str(my_date)
        #print(todaydateStr)
        #print(changedSlice)
        # Temporary fix for parsed date showing the current year instead of the next
        # year
        if int(todaydateStr[5:7]) == 12 and int(changedateStr[5:7]) < 12:
            changedSlice = changedateStr.replace('2018', '2019')
            changedSlice = changedSlice[0:10]

    # a function that compares the launch date to the current date so
    # that AstroNinja shows the proper launch on the welcome screen
    def chooseLaunch(b):

        global nextFlight                    # declare global variables here



        dateName = flyingSoup.find_all(class_="launchdate")
        dateName2 = dateName[b].getText()

        spaceName = flyingSoup.find_all(class_="mission")
        spaceName2 = spaceName[b].getText()

        spaceMission = flyingSoup.find_all(class_="missiondata")
        spaceMission2 = spaceMission[b].getText()

        missDescrip = flyingSoup.find_all(class_="missdescrip")
        missDescrip1 = missDescrip[b].getText()
        #missDescripFixed = missDescrip1.replace('. ', '. \n')
        missDescripFixed2 = re.sub(r'\n*Delayed.*', '', missDescrip1)
        missDescripFixed3 = re.sub(r'\[.*\]', '', missDescripFixed2)
        missDescripFixed4 = "\t" + missDescripFixed3
        missDescripFixed5 = re.sub(r'\s*]', '', missDescripFixed4)
        missDescripFixed6 = re.sub(r'\s*Moved.*', '', missDescripFixed5)


        nextFlight = [dateName2, spaceName2, spaceMission2, missDescripFixed6]
        #print(nextFlight)
        return


    def monthFixer(dateObject):

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        dates = [dateObject]
        monthFind = any(String in months for String in dates)
        if monthFind:
            return True
        else:
            return False


    global recentCounter
    recentCounter = 0
    update_launch(recentCounter)
    monthCheck = monthFixer(dateName2)
    #print(monthCheck)
    # if the launch date has passed, advance to the next launch
    # CHANGED V.80 : made the ability to skip multiple old launches by advancing
    # the same counter as the launch chooser
    switchVar = True
    # If the schedule item has passed, switchVar becomes false
    if todaydateStr > changedSlice:
        switchVar = False
        # Keep skipping schedule items until one is found that hasn't passed.
        # switchVar stays False while checked launch date hasn't passed
        # switchVar turns True and recentCounter is advanced only when launch date has passed
        while switchVar == False:
            if todaydateStr <= changedSlice and 'TBD' not in dateName2 and monthCheck == False:
                switchVar = True
                update_launch(recentCounter)
                monthCheck = monthFixer(dateName2)
            elif todaydateStr >= changedSlice or 'TBD' in dateName2 or monthCheck == True:            # Also skips launch if date isn't determined
                switchVar = False
                recentCounter += 1                    # recentCounter MUST be updated first on
                update_launch(recentCounter)          # the final iteration or it will display
                monthCheck = monthFixer(dateName2)    # the incorrect launch


    chooseLaunch(recentCounter)
    #print(nextFlight)
    return

# A function for skipping old schedule Items

def update_launch(counter):



    # Getting the Date and Mission name
    dateName = flyingSoup.find_all(class_="launchdate")
    dateName2 = dateName[counter].getText()

    if 'NET' in dateName2 and '/' in dateName2:
        noNet = dateName2[4:]

        fixer = re.sub(r'/.*', '', noNet)
        print(fixer)
        dateChange = parser.parse(fixer)
        # Changing the date objects to strings because computers are stupid.
        changedateStr = str(dateChange)
    elif '/' in dateName2:
        fixer = re.sub(r'/.*', '', dateName2)
        #print(fixer)
        dateChange = parser.parse(fixer)

        # Changing the date objects to strings because computers are stupid.
        changedateStr = str(dateChange)

    elif 'TBD' in dateName2 or 'First Quarter' in dateName2:
        dateName2 = 'January'
        dateChange = parser.parse(dateName2)
        changedateStr = str(dateChange)

    elif 'Early' in dateName2:
        notEarly = dateName2[6:]
        changedateStr = str(parser.parse(notEarly))

    elif 'Late' in dateName2:
        notLate = dateName2[5:]
        dateChange = parser.parse(notLate)
        changedateStr = str(dateChange)

    elif 'NET' in dateName2:
        noNet = dateName2[4:]

        dateChange = parser.parse(noNet)

        # Changing the date objects to strings because computers are stupid.
        changedateStr = str(dateChange)

    elif 'Mid' in dateName2:
        noMids = dateName2[4:]
        dateChange = parser.parse(noMids)
        changedateStr = str(dateChange)

    else:
        dateChange = parser.parse(dateName2)

        # Changing the date objects to strings because computers are stupid.
        changedateStr = str(dateChange)

    #global changedSlice, todaydateStr
    changedSlice = changedateStr[0:10]
    todaydateStr = str(my_date)

    #print(int(todaydateStr[5:7]))
    #print(int(changedSlice[5:7]))
    # Temporary fix for parsed date showing the current year instead of the next
    # year
    if int(todaydateStr[5:7]) == 12 and int(changedateStr[5:7]) < 12:
        changedSlice = changedateStr.replace('2018', '2019')
        changedSlice = changedSlice[0:10]

    global comparedList
    comparedList = [todaydateStr, changedSlice]
    return

# Getting the launch schedule.

def getSchedule():

    # Getting the website
    scheduleSite = requests.get('https://spaceflightnow.com/launch-schedule/')
    scheduleSite.raise_for_status()

    # Parsing.
    scheduleSoup = bs4.BeautifulSoup(scheduleSite.text, "lxml")
    goodHtml = scheduleSoup.prettify()

    scheduleContent = scheduleSoup.find_all(class_="entry-content clearfix")

    # getting the launch headers
    launchHead = scheduleSoup.find_all(class_="launchdate")
    global launchHead2
    launchHead2 = []
    # placing the text matches in a list.
    for i in launchHead:
        launchHead2.append(i.text)

    # Getting the Mission
    mission = scheduleSoup.find_all(class_="mission")

    mission2 = []

    for i in mission:
        mission2.append(i.text)

    # Getting mission data.
    missionData = scheduleSoup.find_all(class_="missiondata")
    missionData2 = []

    for i in missionData:
        missionData2.append(i.text)

    # Getting mission descriptions.
    descriptionMiss = scheduleSoup.find_all(class_="missdescrip")




    descriptionMiss3 = []
    for i in descriptionMiss:
        """ fixing overflow between schedule items
            There is an issue with the source Html where a closing </div>
            has been left out and it causes all the following schedule Items
            to be included in the missDescrip of a launch.

            This is a Hacky solution to the problem, it checks if the missDescrip
            is longer than normal and removes the erronous information after the
            paragraph break.
        """
        if len(i.text) > 5000:
            descriptionMiss3.append(re.sub(r'\n.*', '', i.text))
        else:
            descriptionMiss3.append(i.text)


    # Adding some new lines.

    descriptionMiss8 = [re.sub(r'\[.*\]', '', i) for i in descriptionMiss3]
    descriptionMiss9 = ["\t" + i for i in descriptionMiss8]
    #descriptionMissfin = [re.sub(r'\s*Moved.*', '', i) for i in descriptionMiss9]

    #print(len(launchHead))
    #print(len(mission2))
    #print(len(missionData2))
    #print(len(descriptionMissfin))

    # The global list where the data is merged.
    global scheduleList
    scheduleList = []
    # A function to populate the scheduleList list with items scraped from the launch scedule on spaceflightnow.com
    # takes a counter variable as an arguement
    def populate_List(counter):

        global scheduleList

        scheduleList.append(launchHead2[counter])
        scheduleList.append(mission2[counter])
        scheduleList.append(missionData2[counter])
        scheduleList.append(descriptionMiss9[counter])

    global scheduleCounter
    scheduleCounter = 0


    # A function that enables the ability to iterate through populating scheduleList
    # takes a counter as x
    def iterator(x):
        populate_List(x)
        global scheduleCounter
        scheduleCounter += 1
        return

    while scheduleCounter < len(descriptionMiss9):
        iterator(scheduleCounter)

    #for i in scheduleList:     # for testing.
        #print(i)

    #return












#armStrong()
#getSchedule()
