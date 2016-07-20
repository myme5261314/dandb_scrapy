# -*- coding: utf-8 -*-
import scrapy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup as bs
from dandb_scrapy.items import DandbScrapyItem

from company import Company
import utils

header = {
    "Host": "www.dandb.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
}
distribute_proxy = "http://localhost:8888"


class DandbdunsSpider(scrapy.Spider):
    name = "DandbDuns"
    allowed_domains = ["dandb.com"]
    # start_urls = (
    #     'http://www.dandb.com/',
    # )
    start_urls = ['http://www.dandb.com/', ]

    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     db_str = "mysql+pymysql://%s:%s@%s:%s/%s" % (
    #         settings.get("MYSQL_USER"), settings.get("MYSQL_PASSWD"),
    #         settings.get("MYSQL_HOST"), settings.get("MYSQL_PORT"),
    #         settings.get("MYSQL_DBNAME"))
    #     return db_str

    # def __init__(self, db_str, *args, **kwargs):
    #     super(DandbdunsSpider, self).__init__(*args, **kwargs)
        # self.url_t = "https://www.dandb.com/search/?search_type=duns&country=&duns="
        # engine = create_engine(
        #     # 'mysql+pymysql://root:inmotion@localhost:3306/duns2company'
        #     db_str)
        # DBSession = sessionmaker(bind=engine)
        # self.db_session = DBSession()
        # self.resume_duns = utils.get_largest_duns_stored(db_session)

    def start_requests(self):
        db_str = "mysql+pymysql://%s:%s@%s:%s/%s" % (
            self.settings.get("MYSQL_USER"), self.settings.get("MYSQL_PASSWD"),
            self.settings.get("MYSQL_HOST"), self.settings.get("MYSQL_PORT"),
            self.settings.get("MYSQL_DBNAME"))
        url_t = "https://www.dandb.com/search/?search_type=duns&country=&duns="
        engine = create_engine(db_str)
        DBSession = sessionmaker(bind=engine)
        db_session = DBSession()
        # resume_duns = utils.get_largest_duns_stored(db_session)
        resume_duns = 239147510
        # for num in xrange(resume_duns, int(1e9)):
        for num in xrange(resume_duns, resume_duns+1):
            s_num = str(num)
            fill_zero = 9 - len(s_num)
            url = url_t + "0" * fill_zero + s_num
            yield scrapy.http.FormRequest(url,
                                          headers=header,
                                          meta={"proxy": distribute_proxy},
                                          callback=self.parse)

    def parse(self, response):
        duns = int(response.url[-9:])
        form = response.selector.xpath("//form[@name='FormProd']")
        if form and len(form) == 1:
            form = form[0]
            cname = form.xpath("//input[@name='companyName']/@value").extract(
            )[0]
            city = form.xpath("//input[@name='city']/@value").extract()[0]
            address = form.xpath(
                "//input[@name='streetAddress']/@value").extract()[0]
            # countryCode = form.xpath(
            #     "//input[@name='countryCode']/@value").extract()[0]
            # countryName = form.xpath(
            #     "//input[@name='countryName']/@value").extract()[0]
            # This two parameters are interpreted from the request url.
            countryCode, countryName = None, None
            postal_code = form.xpath("//input[@name='zip']/@value").extract()[
                0]
            postal_code = None if postal_code == '' else postal_code
        else:
            cname, city, address, countryCode, countryName, postal_code = [None] * 6
        item = DandbScrapyItem(duns=duns,
                               cname=cname,
                               city=city,
                               address=address,
                               countryCode=countryCode,
                               countryName=countryName,
                               postal_code=postal_code)
        return item
