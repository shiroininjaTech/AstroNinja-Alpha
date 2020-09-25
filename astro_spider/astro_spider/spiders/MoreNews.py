# -*- coding: utf-8 -*-
import scrapy


class MorenewsSpider(scrapy.Spider):
    name = 'MoreNews_spider'
    allowed_domains = ['space.com']
    start_urls = ['https://www.space.com/tech-robots', 'https://www.space.com/science-astronomy']
    #custom_settings = {'LOG_ENABLED': False,
    #}

    def parse(self, response):
        for article_url in response.xpath("//a[contains(@class, 'article-link')]//@href").extract():
            yield response.follow(article_url, callback=self.parse_article)


    def parse_article(self, response):

        # Fixing the found items in the xpath of the photo's metadata.
        # This ensures we only get the date of the image so they can be sorted.
        date =  "".join(response.xpath("//p[contains(@class, 'byline')]//time//text()").extract())                 # Just get the first item found, which will be the date.
        head, sep, tail = date.partition('T')                                          # use partition() to seperate the item on the comma
        fixedDate = head                                                                # Getting the head, which is everything in front of the partition (the actual date)

        # Removing the Related: inserts from the articles.
        bodyItems = [i.strip() for i in response.xpath("//div[contains(@class, 'text-copy bodyCopy auto')]//p//text()").getall()]

        """
            Iterating through body items, looking for descriptions of related articles,
            and removing them when found.
        """
        for i in bodyItems:
            if "Related:" in i:
                current = bodyItems.index(i) + 1        # The actual description, this is the index number
                bodyItems.pop(current)                  # of the related tag + 1. Must be popped first.
                bodyItems.pop(bodyItems.index(i))       # Then we pop the Related: tag.

            elif "Complete coverage:" in i:
                current = bodyItems.index(i) + 1        # The actual description, this is the index number
                bodyItems.pop(current)                  # of the related tag + 1. Must be popped first.
                bodyItems.pop(bodyItems.index(i))       # Then we pop the Related: tag.

            elif "Video:" in i:
                current = bodyItems.index(i) + 1        # The actual description, this is the index number
                bodyItems.pop(current)                  # of the related tag + 1. Must be popped first.
                bodyItems.pop(bodyItems.index(i))       # Then we pop the Related: tag.

            elif "Additional resources:" in i:
                current = bodyItems.index(i) + 1        # The actual description, this is the index number
                bodyItems.pop(current)                  # of the related tag + 1. Must be popped first.
                bodyItems.pop(bodyItems.index(i))       # Then we pop the Related: tag.

            elif "OFFER:" in i:
                current = bodyItems.index(i) + 1        # The actual description, this is the index number
                current2 = current + 1
                current3 = current2 + 1
                current4 = current3 + 1
                bodyItems.pop(current4)
                bodyItems.pop(current3)
                bodyItems.pop(current2)
                bodyItems.pop(current)                  # of the related tag + 1. Must be popped first.
                bodyItems.pop(bodyItems.index(i))       # Then we pop the Related: tag.

        # Getting the different types of possible images
        mainImage = "".join(response.xpath("//div[contains(@class, 'box')]//img/@src").extract())
        altImage  = response.xpath("//p[contains(@class, 'vanilla-image-block')]//img/@data-original-mos").extract()[0]


        # Fixing the spacing of the items, so smaller items don't get indented.
        betterSpaced = []
        for i in bodyItems:
            # Only newline and indent if over 25 characters
            if len(i) > 25:
                betterSpaced.append("\n\n\t" + i)
            else:
                betterSpaced.append(" " + i)

        if len(mainImage) == 0:
            imageUsed = altImage
        else:
            imageUsed = mainImage
        article = {
            'title' : "".join(response.xpath("//h1//text()").extract()),
            'date'  : fixedDate,
            'body'  : "".join(betterSpaced),
            'image'   : imageUsed,

        }




        yield article
