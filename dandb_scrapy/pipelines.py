# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from spiders.DandbDuns import DandbdunsSpider
from items import DandbScrapyItem
from spiders.company import Company


def Item2Company(item):
    return Company(duns_id=item["duns"],
                   company_name=item["cname"],
                   city=item["city"],
                   address=item["address"],
                   country_code=item["countryCode"],
                   postal_code=item["postal_code"])


class DandbScrapyPipeline(object):
    def __init__(self, db_session):
        self.db_session = db_session

    @classmethod
    def from_settings(cls, settings):
        db_str = "mysql+pymysql://%s:%s@%s:%s/%s" % (
            settings.get("MYSQL_USER"), settings.get("MYSQL_PASSWD"),
            settings.get("MYSQL_HOST"), settings.get("MYSQL_PORT"),
            settings.get("MYSQL_DBNAME"))
        engine = create_engine(
            # 'mysql+pymysql://root:inmotion@localhost:3306/duns2company'
            db_str)
        DBSession = sessionmaker(bind=engine)
        return cls(DBSession())

    def process_item(self, item, spider):
        if isinstance(spider, DandbdunsSpider) and isinstance(item,
                                                              DandbScrapyItem):
            if "cname" in item.keys() and item["cname"]:
                # self.db_session.add(Company(dict(DandbScrapyItem)))
                self.db_session.add(Item2Company(item))
                self.db_session.commit()
        return item
