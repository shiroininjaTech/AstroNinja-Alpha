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
        yield videos
#/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[1]/div[1]/div[1]/div[1]/h3/a
