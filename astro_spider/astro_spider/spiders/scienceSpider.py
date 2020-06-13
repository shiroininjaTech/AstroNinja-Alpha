# -*- coding: utf-8 -*-
import scrapy


class SciencespiderSpider(scrapy.Spider):
    name = 'scienceSpider'
    allowed_domains = ['nasa.gov', 'google.com']
    start_urls = ['https://www.google.com/search?client=ubuntu&channel=fs&q=space+station+science+highlights&ie=utf-8&oe=utf-8']
    custom_settings = {'LOG_ENABLED': True,
    }
    def parse(self, response):
        for highlight_url in response.xpath("/html/body/div[6]//a/@href").extract():
            #if "SSSH_" in highlight_url:
            yield response.follow(highlight_url, callback=self.parse_highlight)


    def parse_highlight(self, response):
        highlights = {

            'title' : response.xpath("//h1[contains(@class, 'title')]//text()").extract()[0],
            'text'  : "\n\n\t".join([i.strip() for i in response.xpath("//div[contains(@class, 'text')]//p//text()").getall()])

        }
        yield highlights
#/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/a/h3/div
