# -*- coding: utf-8 -*-
import scrapy


class Schedulespider(scrapy.Spider):
    name = 'scheduleSpider'
    allowed_domains = ['spaceflightnow.com']
    start_urls = ['https://spaceflightnow.com/launch-schedule/']

    custom_settings = {'LOG_ENABLED': True,
    }




    def parse(self, response):

        # Creating a new way to get schedule items. get the items first as list,
        # then get the individual parts of the item.
        schedItems = []


        # This gets ALL the child items from the div class 'missionData' and
        # merges all of the children into one beast and adds them to a library.
        missDat = []
        for r in response.xpath("//div[contains(@class, 'missiondata')]"):
            date = [p.strip() for p in r.xpath('.//text()').extract() if p.strip()]
            date2 = []
            for i in date:
                date2.append(i.replace('Launch site:', '\nLaunch site: '))
            # fixing spacing
            finalDate = []
            for i in date2:
                finalDate.append(i.replace('Launch time:', 'Launch time: '))
            missDat.append("".join(finalDate))

        # Doing the same for the mission description.
        dissDat = []
        for r in response.xpath("//div[contains(@class, 'missdescrip')]"):
            missingDate = r.xpath(".//text()").extract()
            #print(missingDate)
            crip = [p.strip() for p in r.xpath('.//text()').extract() if p.strip()]
            dissDat.append("".join(crip))



        scheduleData = {
            'launchDates' : response.xpath("//div[contains(@class, 'datename')]/span[contains(@class, 'launchdate')]//text()").extract(),
            'missionTitle' : response.xpath("//div[contains(@class, 'datename')]/span[contains(@class, 'mission')]//text()").extract(),
            'missionInfo' : missDat,
            'description' : dissDat,
        }

        yield scheduleData
