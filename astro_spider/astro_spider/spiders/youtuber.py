# -*- coding: utf-8 -*-
import scrapy


class YoutuberSpider(scrapy.Spider):
    name = 'youtuber'
    allowed_domains = ['www.spacex.com']
    start_urls = ['https://www.spacex.com/launches/']

    def parse(self, response):

        videos = {
            'link' : response.xpath('//a[contains(@class, "btn animate")]//@href').extract()[0],
            'mission' : response.xpath('//h2[contains(@class, "animate")]//text()').extract()[0]

        }
        #print(videos['link'])

        # TO-DO: Find a correct way to fix broken videos if there is a launch delay
        """
        firstLink = response.xpath('//div[contains(@class, "inner-right-bottom")]/a[contains(@class, "btn ")]//@href').extract()[0]
        missionName = response.xpath('//div[contains(@class, "inner-right-bottom")]/h1/text()').extract()[0]
        print(firstLink)
        #print(firstLink)
        if '/launches/' in firstLink:
            firstLink = response.xpath('//div[contains(@class, "inner-left-bottom")]/a[contains(@class, "btn ")]//@href').extract()[0]

        videos = {
            'link' : firstLink,
            'mission' : response.xpath('//h2[contains(@class, "animate")]//text()').extract()[0]

        }
        """
        yield videos
