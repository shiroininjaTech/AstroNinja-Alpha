"""
   * A Module for AstroNinja that receives data passed by crew_spider and
   * processes it before passing it to the front end module.
"""

"""
   * Written By : Tom Mullins
   * Created:  06/29/19
   * Modified: 06/09/2020
"""


"""
    Creating a pipeline class that collects dictionary objects passed by
    scrapy into a single list for easier processing.
"""
global biosList
biosList = []    # list to be filled with scrapy objects

class BioCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        biosList.append(item)

"""
    Creating the pipeline class to collect objects from scienceSpider
"""
global labList
labList = []

class LabCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        labList.append(item)

# The function that processes the data from crew_spider
def rollCall():


    # Creating the empty global lists that the keys of each dictionary are dumped into
    global crewName, crewLocation, crewNat, crewImg, shortBio, shortBio2

    crewName = []
    crewLocation = []
    crewNat = []
    crewImg = []
    shortBio = []
    shortBio2 = []

    # A string with the rest of the img url
    httpify = "https:"
    # sorting all the dict keys into their rightful lists
    for i in biosList:

        bioDict = dict(i)

        crewName.append(bioDict['name'])
        crewLocation.append(bioDict['birthplace'])
        crewNat.append(bioDict['nationality'])

        # Temporary fix for if there is no image found for a crew member.
        # Replaces missing image with expedition logo.
        if bioDict['photo'] != "":
            crewImg.append(httpify + bioDict['photo'])
        else:
            crewImg.append("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ISS_Expedition_63_Patch.png/180px-ISS_Expedition_63_Patch.png")

        shortBio.append(bioDict['short'])
        shortBio2.append(bioDict['short2'])
    #print(crewImg)
    #print(crewNat)

    return

# The function that processes the data from scienceSpider
def labNotes():

    # Creating the empty global lists that the keys of each dictionary are dumped into.
    global scienceTitle, scienceBody

    scienceTitle = []
    scienceBody = []

    def spiderLauncher(className):
        process = CrawlerProcess({'ITEM_PIPELINES': { '__main__.LabCollectorPipeline': 2000}})
        process.crawl(className)
        process.start()

        return
    spiderLauncher(scienceSpider.SciencespiderSpider)
    for i in labList:
        labDict = dict(i)

        scienceTitle.append(labDict['title'])

    print(scienceTitle)
    return

#rollCall()
#labNotes()
