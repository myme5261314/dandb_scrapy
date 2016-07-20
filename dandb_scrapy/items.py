# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DandbScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    duns = scrapy.Field()
    cname = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    countryCode = scrapy.Field()
    countryName = scrapy.Field()
    postal_code = scrapy.Field()
