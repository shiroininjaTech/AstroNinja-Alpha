# -*- coding: utf-8 -*-
import scrapy
import re

class CrewspiderSpider(scrapy.Spider):

    name = 'crew_spider'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Expedition_63']
    custom_settings = {'LOG_ENABLED': True,
    }

    def parse(self, response):
        for bio_url in response.xpath("//table[contains(@class, 'infobox')]//div[contains(@class, 'plainlist')]//a/@href").extract():
            yield response.follow(bio_url, callback=self.parse_bio)


    def parse_bio(self, response):

        fixedBio = []
        fixedBio2 = []
        for r in response.xpath("//div[contains(@class, 'mw-body-content')]//p"):
            fullBio = [p.strip() for p in r.xpath('.//text()').extract() if p.strip()]

            fixedBio.append(" ".join(fullBio))

        # Getting rid of those pesky wikipedia citation brackets
        finishedBrackets = []
        pattern = r'(\[[?:0-9]*\])'     # The pattern to be found, the * is crucial to finding every instance

        for i in fixedBio:
            s = i
            finishedBrackets.append(re.sub(pattern, '', s))

        """
            TO-DO:
                see if we can combine these if statements.
        """
        for i in finishedBrackets:
            fixedBio2.append("\n\n\t" + i)

        if len(fixedBio2) < 4:
            shortBio = fixedBio2[0]+fixedBio2[1]
        if len(fixedBio) > 4:
            shortBio   = fixedBio2[0]+fixedBio2[1]
            fixedBio2.pop(0)
            fixedBio2.pop(0)
            secondHalf = "".join(fixedBio2)

        bio = {
            'name' : "".join(response.xpath("//table[contains(@class, 'infobox biography vcard')]//div[contains(@class, 'fn')]").extract()),
            'short'  : shortBio,
            'short2'  : secondHalf,
            'birthplace'  : "".join(response.xpath("//table[contains(@class, 'infobox biography vcard')]//div[contains(@class, 'birthplace')]//text()").extract()),
            'nationality'   : "".join(response.xpath("//table[contains(@class, 'infobox biography vcard')]//tr/td[contains(@class, 'category')]/text()").extract()),
            'photo'       : "".join(response.xpath("//table[contains(@class, 'infobox biography vcard')]//td[contains(@colspan, '2')]//a[contains(@class, 'image')]//img/@src").extract())

        }

        yield bio
