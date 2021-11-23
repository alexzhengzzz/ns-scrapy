# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PicItem(scrapy.Item):
    link = scrapy.Field()


class AllPicCount(scrapy.Item):
    numOfPic = scrapy.Field()


