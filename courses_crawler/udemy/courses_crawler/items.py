# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UdemyItem(scrapy.Item):
    id_course = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    n_students = scrapy.Field()
    url = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    description_extend = scrapy.Field()
    instructor = scrapy.Field()
    language = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    sessions = scrapy.Field()
    characteristics = scrapy.Field()
    cost = scrapy.Field()
    free = scrapy.Field()
