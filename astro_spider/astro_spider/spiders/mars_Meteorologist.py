# -*- coding: utf-8 -*-
import scrapy


class MarsMeteorologistSpider(scrapy.Spider):
    name = 'mars_Meteorologist'
    allowed_domains = ['mars.nasa.gov']
    start_urls = ['https://mars.nasa.gov/insight/weather/']

    custom_settings = {'LOG_ENABLED': True,
    }


    def parse(self, response):



        weatherData = {
            'marsDate'     : response.xpath("//div[contains(@class, wysiwyg_content)]//text()").extract(),
            'tempMax'      : '',
            'tempMin'      : '',
        }

        yield weatherData

#/html/body/div[3]/div/div[3]/section[1]/div/article/div/div/div/div[1]/div/div[1]/div/div/div[1]/span[1]
