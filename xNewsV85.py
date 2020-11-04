"""
   * A Module for AstroNinja that pulls news articles from multiple sources
   * and wraps them in a global list for iterating over and passing over to the
   * front end for displaying to the user via the SpaceX news tab.
"""

"""
   * Written By : Tom Mullins
   * Created:  04/30/18
   * Modified: 11/04/20
"""
import re
from dateutil import parser


"""
    Creating pipeline classes that collects dictionary objects passed by
    scrapy into a single list for easier processing.
"""
global spiderLoot
spiderLoot = []    # list to be filled with scrapy objects

class ItemCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        spiderLoot.append(item)

# For hubble views
global hubbleData
hubbleData = []

# pipeline to fill the items list
class HubbleCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        hubbleData.append(item)



# A function that runs the news_spider and processes the scraped data
# for use by the front end module.
def intestellar_News(sorter):

    # a fix for missing dates. temporary.
    for i in spiderLoot:
        if i['date'] == '':
            i['date'] = '2020-01-01'

    # sorting the list of dictionaries passed by scrapy by date.
    if sorter == 'Newest':
        sortedResults = sorted(spiderLoot, key = lambda i: parser.parse(i['date']), reverse=True)
    if sorter == "Oldest":
        sortedResults = sorted(spiderLoot, key = lambda i: parser.parse(i['date']), reverse=False)

    # Creating some empty lists to dump the contents of each dictionary into.
    global listedTitle, listedBody, listedImg, listedDate
    listedDate = []
    listedTitle = []
    listedBody = []
    listedImg = []
    fixedBody = []
    # Iterating through each dict item in the sorted list of dicts
    for i in sortedResults:
        # picking out the single dictionary as it's own variable
        linkDict = dict(i)
        listedDate.append(linkDict['date'])
        listedTitle.append(linkDict['title'])                                                     # Adding the article's title
        listedBody.append(re.sub('(:?[a-zA-Z0-9\,\:\"\'\)\*\(\-\-\]\[_])\n\n\t', r'\1 ', linkDict['body']))           # Adding the article's body/if there is a letter or number before newlines, remove them
        listedImg.append(linkDict['image'])



        # If there is no image provided with the article, use a generic one (prevents crashes)
        # No longer needed, found a better fix that displays articles even if there is no image.
        """
        if len(linkDict['image']) == 0:
            listedImg.append('https://image.flaticon.com/icons/svg/117/117992.svg')
        else:
            listedImg.append(linkDict['image'])
        """

    return


"""
    * A function that scapes Images from the Hubble space telescope from spacetelescope.org
    * using a function that scrapes links from the site and passes it to another Function
    * that retreives the image and description.
"""

def hubbleViewz(sorter):

    # Sorting the Pictures of the week from hubble by newest.

    if sorter == 'Newest':
        sortedResults = sorted(hubbleData, key = lambda i: parser.parse(i['hubbleDate']), reverse=True)
    if sorter == 'Oldest':
        sortedResults = sorted(hubbleData, key = lambda i: parser.parse(i['hubbleDate']), reverse=False)

    # Creating some empty lists to dump the contents of each dictionary into.
    global images, descriptions, headers
    images = []
    descriptions = []
    headers = []

    # Iterating through each dict item in the sorted list of dicts
    for i in sortedResults:
        hubbleDict = dict(i)
        for i in hubbleDict['hubbleImage']:
            images.append(i)
        for i in hubbleDict['hubbleDescrip']:
            descriptions.append(i)
        for i in hubbleDict['header']:
            headers.append(i)


#phoneHome()
#hubbleViewz()
