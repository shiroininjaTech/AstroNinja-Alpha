# -*- coding: utf-8 -*-
import scrapy

from scrapy.http.request import Request

class LaunchhistorySpider(scrapy.Spider):
    name = 'launchHistory'
    allowed_domains = ['rocketlaunch.live']
    start_urls = ['https://www.rocketlaunch.live/?pastOnly=1&page=1', 'https://www.rocketlaunch.live/?pastOnly=1&page=2','https://www.rocketlaunch.live/?pastOnly=1&page=3', 'https://www.rocketlaunch.live/?pastOnly=1&page=4', 'https://www.rocketlaunch.live/?pastOnly=1&page=5', 'https://www.rocketlaunch.live/?pastOnly=1&page=6', 'https://www.rocketlaunch.live/?pastOnly=1&page=7', 'https://www.rocketlaunch.live/?pastOnly=1&page=8']

    custom_settings = {'LOG_ENABLED': False,
    }




    def parse(self, response):
        launches = {
            'spacexDate' : response.xpath(".//div[contains(@class, 'company-spacex')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'chinaDate' : response.xpath(".//div[contains(@class, 'company-china')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'ulaDate' : response.xpath(".//div[contains(@class, 'company-united-launch-alliance-ula')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'indiaDate' : response.xpath(".//div[contains(@class, 'company-isro')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'rocketDate' : response.xpath(".//div[contains(@class, 'company-rocket-lab')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'japanDate' : response.xpath(".//div[contains(@class, 'company-jaxa')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'arianeDate' : response.xpath(".//div[contains(@class, 'company-arianespace')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'russiaDate' : response.xpath(".//div[contains(@class, 'company-roscosmos')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'northropDate' : response.xpath(".//div[contains(@class, 'company-northrop-grumman')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'blueDate' : response.xpath(".//div[contains(@class, 'company-blue-origin')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'ilsDate' : response.xpath(".//div[contains(@class, 'company-international-launch-services-ils')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'rusMil' : response.xpath(".//div[contains(@class, 'company-russian-military')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),
            'expace' : response.xpath(".//div[contains(@class, 'company-expace-china')]/div[@class='large-2 medium-2 small-3 columns']/div[@data-sortdate]/@title").extract(),


        }
        yield launches
