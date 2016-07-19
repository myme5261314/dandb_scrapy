# -*- coding: utf-8 -*-
import scrapy


class DandbdunsSpider(scrapy.Spider):
    name = "DandbDuns"
    allowed_domains = ["dandb.com"]
    start_urls = (
        'http://www.dandb.com/',
    )

    def parse(self, response):
        pass
