# -*- coding: utf-8 -*-
import scrapy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup as bs
from html.parser.HTMLParser import HTMLParserError

from company import Company
import utils

header = {
    "Host": "www.dandb.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
}
distribute_proxy = "http://localhost:8888"


class DandbdunsSpider(scrapy.Spider):
    name = "DandbDuns"
    allowed_domains = ["dandb.com"]
    # start_urls = (
    #     'http://www.dandb.com/',
    # )
    start_urls = self.generate_urls()

    def __init__(self, *args, **kwargs):
        super(DandbdunsSpider, self).__init__(*args, **kwargs)
        self.url_t = "https://www.dandb.com/search/?search_type=duns&country=&duns="
        engine = create_engine('mysql+pymysql://root:inmotion@localhost:3306/duns2company')
        DBSession = sessionmaker(bind=engine)
        self.db_session = DBSession()
        self.resume_duns = utils.get_largest_duns_stored(db_session)

    def generate_urls(self):
        for num in range(self.resume_duns, int(1e9)):
            s_num = str(num)
            fill_zero = 9 - len(s_num)
            yield self.url_t + "0" * fill_zero + s_num


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.http.Request(url, headers=header, meta={"proxy": distribute_proxy})

    def parse(self, response):
        duns = int(response.url[-9:])
        form = response.selector.xpath("//form[@name='FormProd']/")
        if form and len(form) == 1:
            form = form[0]
        else:
            return None
