# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UdacityItem(scrapy.Item):
    id_course = scrapy.Field()
    title = scrapy.Field()
    school = scrapy.Field() # -> Categoría
    rating = scrapy.Field()
    n_reviews = scrapy.Field()
    url = scrapy.Field()
    difficulty = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    collaboration = scrapy.Field()
    duration = scrapy.Field()
    free = scrapy.Field()
    # idioma