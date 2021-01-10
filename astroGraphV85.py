
"""
   This the Library file for the backend graph module for AstroNinja, a space launch tracker and space news app for the
   Linux desktop. It scrapes data from spacelaunchnow.com and displays it in an interactive GUI using beautiful soup
   and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.85
   * Date Created: 01/11/18
   * Date Modified: 01/10/21
"""

import AstroNinjaMain
import astroNinjaV85
import time, os
import calendar
from dateutil import parser
from datetime import date
import re

#missionCount = 3
my_date = date.today()

"""
    Creating a pipeline class for scrapy to funnel results into.
    Must be placed outside of function that it is to be used in
"""
global links
links = []  # the list to catch everything from the scrapy pipeline

# pipeline to fill the items list
class ItemCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        links.append(item)
# A function to tally how many launches each agency has in a given month.
# Takes monthCount as x and missionCount as y
def tally_ho(x, y):

    # tally_ho uses functions from astroNinja to tally the launch counts.
    astroNinjaV85.getSchedule()
    astroNinjaV85.scheduleList.append('Ah')
    astroNinjaV85.launchHead2.append('Ah')
    #print(astroNinja.launchHead2)
    # The variables that keep count of the agency Tallies
    global spaceXCount
    global chinaCount
    global ulaCount
    global indiaCount
    global rocketCount
    global japaneseCount
    global arianeCount
    global russiaCount
    global northCount
    global euroCount
    global virginCount

    spaceXCount = 0
    chinaCount = 0
    ulaCount = 0
    indiaCount = 0
    rocketCount = 0
    japaneseCount = 0
    arianeCount = 0
    russiaCount = 0
    northCount = 0
    euroCount = 0
    virginCount = 0

    global changedSlice, changedSlice2, todaySlice, todaydateStr
    # A function to properly clean the data for tallying.
    # Takes launch date variable as launchDate
    # Takes today's date as currentDay
    def the_cleaner(launchDate, currentDay):
        global changedSlice, changedSlice2, todaySlice, todaydateStr

        # converting the launch date so that it can be compared to the current month.

        if 'NET' in launchDate and '/' in launchDate:
            noNet = launchDate[4:]

            fixer = re.sub(r'/.*', '', noNet)
            #print(fixer)
            dateChange = parser.parse(fixer)
            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)
        elif '/' in launchDate:
            fixer = re.sub(r'/.*', '', launchDate)
            dateChange = parser.parse(fixer)

            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)

        elif '1st Quarter' in launchDate:
            launchDate = 'January'
            dateChange = parser.parse(launchDate)
            changedateStr = str(dateChange)

        elif 'TBD' in launchDate or 'First Quarter' in launchDate:
            launchDate= 'January'
            dateChange = parser.parse(launchDate)
            changedateStr = str(dateChange)

        elif 'Early' in launchDate:
            notEarly = launchDate[6:]
            changedateStr = str(parser.parse(notEarly))

        elif 'NET' in launchDate:
            noNet = launchDate[4:]

            if 'Late' in noNet:
                noNet = noNet[5:]

            dateChange = parser.parse(noNet)
            changedateStr = str(dateChange)


        elif 'Late' in launchDate:
            notLate = launchDate[5:]
            dateChange = parser.parse(notLate)
            changedateStr = str(dateChange)


        elif 'Mid' in launchDate:
            noMids = launchDate[4:]
            dateChange = parser.parse(noMids)
            changedateStr = str(dateChange)

        else:
            dateChange = parser.parse(launchDate)

            # Changing the date objects to strings because computers are stupid.
            changedateStr = str(dateChange)


        parsedDate = str(parser.parse(changedateStr))
        changedSlice = parsedDate[0:10]

        # Converting today's date so it can be compared to the launch month.
        todaydateStr = str(currentDay)
        todaySlice = todaydateStr[5:7]
        changedSlice2 = changedSlice[5:7]



    # A function to that tallies launches based on orginization
    # Takes changedSlice2 as an arguement
    def countDracula(a):

        global spaceXCount
        global chinaCount
        global ulaCount
        global indiaCount
        global rocketCount
        global japaneseCount
        global arianeCount
        global russiaCount
        global northCount
        global euroCount
        global virginCount

        # If launch is in the current month and matches with keywords, then add to the tally variable for that agency.
        # Then increment both month count and mission count by 4.
        if todaySlice == a and changedSlice >= todaydateStr :
             if 'SpaceX' in astroNinjaV85.scheduleList[y]:
                 spaceXCount += 1
             elif 'Chinese' in astroNinjaV85.scheduleList[y]:
                 chinaCount += 1
             elif 'Arianespace' in astroNinjaV85.scheduleList[y]:
                 arianeCount += 1
             elif 'India' in astroNinjaV85.scheduleList[y]:
                 indiaCount += 1
             elif 'United Launch Alliance' in astroNinjaV85.scheduleList[y]:
                 ulaCount += 1
             elif 'Rocket Lab' in astroNinjaV85.scheduleList[y]:
                 rocketCount += 1
             elif 'Japan' in astroNinjaV85.scheduleList[y]:
                 japaneseCount += 1
             elif 'Russian' in astroNinjaV85.scheduleList[y]:
                 russiaCount += 1
             elif 'Eurockot' in astroNinjaV85.scheduleList[y]:
                 euroCount += 1
             elif 'Virgin Orbit' in astroNinjaV85.scheduleList[y]:
                 virginCount += 1
             elif 'Northrop Grumman' and 'International Launch Services' not in astroNinjaV85.scheduleList[y]:
                 northCount += 1



    # Haven't found fixes for these, so they're skipped for now.
    brokenDates = ['Early', 'Quarter', 'First Half', 'TBD', 'Spring', 'Mid-2019']


    # Iterate over scheduleList until finished
    while x != 60 and y != 67:

        # First we start with some conditionals that check for breaking characters in the launch month and correct them before continuing
        if 'Approx.' in astroNinjaV85.scheduleList[x] :
            later = astroNinjaV85.scheduleList[x].replace('Approx. ', '') # removing breaking characters
            slicy = later[0:3]

            the_cleaner(slicy, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'Mid-' in astroNinjaV85.scheduleList[x] and 'Mid-2019' not in astroNinjaV85.scheduleList[x]:
            later = astroNinjaV85.scheduleList[x].replace('Mid-', '') # removing breaking characters
            slicy = later[0:3]

            the_cleaner(slicy, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'Late' in str(astroNinjaV85.scheduleList[x]):
            later = astroNinjaV85.scheduleList[x].replace('Late ', '') # removing breaking characters

            the_cleaner(later, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4

        elif 'Mid/Late' in astroNinjaV85.scheduleList[x] :
            later = astroNinjaV85.scheduleList[x].replace('Mid/Late ', '') # removing breaking characters

            the_cleaner(later, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4

        elif '/' and 'NET' in astroNinjaV85.scheduleList[x]:
            monthString = astroNinjaV85.scheduleList[x]
            noNet = monthString[4:]
            noSlash = noNet[0:3]               # Removing breaking characters

            the_cleaner(noSlash, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4

        elif '/' in astroNinjaV85.scheduleList[x]:
            monthString = astroNinjaV85.scheduleList[x]
            noSlash = re.sub('/.*', '', monthString)

            the_cleaner(noSlash, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4


        elif 'NET' in astroNinjaV85.scheduleList[x]:
            netMonth = astroNinjaV85.scheduleList[x]
            noNet = netMonth[4:]      # cutting out characters that cause a crash and miscount.

            the_cleaner(noNet, my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4

        # checking for any of the vague launch dates that cause breakage.
        elif any(word in astroNinjaV85.scheduleList[x] for word in brokenDates) :
            x += 4
            y += 4

        else:

            the_cleaner(astroNinjaV85.scheduleList[x], my_date)

            if todaySlice != changedSlice2 and changedSlice <= todaydateStr:
                x += 4
                y += 4
            # countDracula checks which agency the launch is with and increments
            # the correct variable
            else:
                countDracula(changedSlice2)

                # increment to the next launch
                x += 4
                y += 4
    #print(spaceXCount)
    #print(chinaCount)   # testing
    #print(japaneseCount)
    #print(ulaCount)
    #print(rocketCount)
    #print(arianeCount)
    #print(indiaCount)
    #print(commieCount)

    return

"""
    A Function that scrapes launch history from rocketlaunch.live and tallies it.
    It then passes the counts to AstroNinjaMain to build a graph of previous launch
    Counts in the GUI.

    Takes a year in string form as year
"""
def historian(year):


    #print(links)
    # a simple function to fix and sort items in each orginization date list.
    def datlistFix(key):
        listedDates = []
        for i in links:
            linkDict = dict(i)
            for i in linkDict[key]:
                listedDates.append(i)

        cutList = []
        for i in listedDates:
            cutList.append(i[0:10])
        return sorted(cutList, reverse=True)

    # Getting all the dates for each Organization
    sortedAriane = datlistFix('arianeDate')
    sortedSpacex = datlistFix('spacexDate')
    sortedChina  = datlistFix('chinaDate')
    sortedUla    = datlistFix('ulaDate')
    sortedIndia  = datlistFix('indiaDate')
    sortedRocket = datlistFix('rocketDate')
    sortedJapan  = datlistFix('japanDate')
    sortedRussia = datlistFix('russiaDate')
    sortedNorthrop = datlistFix('northropDate')
    sortedBlue   = datlistFix('blueDate')
    sortedIls    = datlistFix('ilsDate')
    sortedRusMil = datlistFix('rusMil')
    sortedRussia = sortedRussia + sortedRusMil          # Adding Russian Military launches to the Russian list.
    sortedRussia = list(dict.fromkeys(sortedRussia))    # Removing duplicates.
    sortedXpace = datlistFix('expace')
    sortedChina = sortedChina + sortedXpace
    sortedChina = list(dict.fromkeys(sortedChina))
    #print(sortedSpacex)
    #print(sortedChina)
    # The global variables to be passed to the front end to build graphs
    # TO-DO: put them in a dictionary
    global spaceXCount
    global chinaCount
    global ulaCount
    global indiaCount
    global rocketCount
    global japaneseCount
    global arianeCount
    global russiaCount
    global northCount
    global blueOrigin, ilsCount

    spaceXCount = 0
    chinaCount = 0
    ulaCount = 0
    indiaCount = 0
    rocketCount = 0
    japaneseCount = 0
    arianeCount = 0
    russiaCount = 0
    northCount = 0
    blueOrigin = 0
    ilsCount = 0
    #milCount = 0
    #yearVar = '2019'

    """
        The function that actually does the tallying.
        takes the sorted list object of an org, it's counter,
        and the year passed to the parent funtion as yearArg.
    """
    def pastTally(sortedOb, orgCounter, yearArg):

        for i in sortedOb:              # for each object in the sorted list
            if yearArg in i:            # If the year is in the string
                orgCounter += 1         # Increment the org's counter by 1
        return orgCounter               # instead of using another global Var, just return the counter itself.

    # running the pastTally() function as the org counter itself saves on global varibles.
    spaceXCount = pastTally(sortedSpacex, spaceXCount, year)
    chinaCount  = pastTally(sortedChina, chinaCount, year)
    ulaCount    = pastTally(sortedUla, ulaCount, year)
    indiaCount  = pastTally(sortedIndia, indiaCount, year)
    rocketCount = pastTally(sortedRocket, rocketCount, year)
    japaneseCount = pastTally(sortedJapan, japaneseCount, year)
    arianeCount = pastTally(sortedAriane, arianeCount, year)
    russiaCount = pastTally(sortedRussia, russiaCount, year)
    northCount  = pastTally(sortedNorthrop, northCount, year)
    blueOrigin  = pastTally(sortedBlue, blueOrigin, year)
    ilsCount    = pastTally(sortedIls, ilsCount, year)
    #milCount    = pastTally(sortedRusMil, milCount, year)
    #russiaCount = russiaCount + milCount
    """
    print("SpaceX %s" % spaceXCount)
    print("China %s" % chinaCount)
    print("Russia %s " % russiaCount)
    print("Ariane %s" % arianeCount)
    print("India %s" % indiaCount)
    print("Rocket labs %s" % rocketCount)
    print("Northrop %s" % northCount)
    print("Japan %s" % japaneseCount)
    print("United %s" % ulaCount)
    print("Blue Origin %s" % blueOrigin)
    print("ILS %s" % ilsCount)
    """
    return

#tally_ho(monthCount, missionCount)
#build_Graph()
#historian('2019')
