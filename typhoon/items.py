# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TyphoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    located = scrapy.Field()
    thistime=scrapy.Field()
    nexttime=scrapy.Field()
    name=scrapy.Field()
    country=scrapy.Field()
    time=scrapy.Field()
    place=scrapy.Field()
    pressure=scrapy.Field()
    speed=scrapy.Field()
    power=scrapy.Field()
    movespeed=scrapy.Field()
