"""
   * A practice script for scraping data from article pages using scrapy instead
   * of bs4
"""

"""
   * Written By : Tom Mullins
   * Created:  07/24/20
   * Modified: 11/11/20
"""

global spacexDump
spacexDump = []



# pipeline to fill the items list
class MoreCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        spacexDump.append(item)


def liftOff():
    # lists to be filled with items from spacexDump
    global link, missionTitle
    link = []
    missionTitle = []

    for i in spacexDump:
        spacexDict = dict(i)
        link.append(spacexDict['link'])
        missionTitle.append(spacexDict['mission'])

    # Turning the link into an embed link.
    global fixedLink

    if len(link) == 0:
        fixedLink = 'https://www.spacex.com/launches/#update'
        missionTitle.append("Upcoming Mission")
    elif '#update' in link[0]:
        fixedLink = 'https://www.spacex.com/launches/#update'

    else:
        fixedLink = link[0].replace('https://youtu.be/', 'https://www.youtube.com/embed/')
    #print(fixedLink)

    return
