# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ImgsItem(scrapy.Item):
    image_urls = Field()
    images = Field()
    image_paths = Field()



