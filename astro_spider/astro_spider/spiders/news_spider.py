# -*- coding: utf-8 -*-
import scrapy


class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['spacenews.com']
    start_urls = ['http://spacenews.com/section/commercial/', 'http://spacenews.com/section/launch/', 'https://spacenews.com/section/civil/']
    custom_settings = {'LOG_ENABLED': False,
    }

    def parse(self, response):
        for article_url in response.xpath("//h2[contains(@class, 'launch-title')]/a/@href").extract():
            yield response.follow(article_url, callback=self.parse_article)


    def parse_article(self, response):
        article = {
            'title' : response.xpath("//h1[contains(@class, 'post-title')]//text()").extract()[0],
            'date'  : response.xpath("//time//text()").extract()[0],
            'body'  : "\n\n\t".join([i.strip() for i in response.xpath("//p//text()").getall()]),
            'image'   : "".join(response.xpath("//figure[contains(@class, 'featured wp-caption')]//img/@src").extract())

        }


        #concatenate_list(article['body'])
        yield article
