# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapypivixItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    tags=scrapy.Field()
    user_id=scrapy.Field()
    user_name=scrapy.Field()
    url=scrapy.Field()
    illust_id=scrapy.Field()