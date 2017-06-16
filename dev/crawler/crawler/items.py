# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacultyItem(scrapy.Item):
    # define the fields for your item here like:
    university = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    interests = scrapy.Field()
    photo = scrapy.Field()
