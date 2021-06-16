# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseraItem(scrapy.Item):
    id_course = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    n_ratings = scrapy.Field()
    views = scrapy.Field()
    url = scrapy.Field()
    duration = scrapy.Field()
    difficulty = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    instructor = scrapy.Field()
    institution = scrapy.Field()
    duration_week = scrapy.Field()
    enrolled = scrapy.Field()
    language = scrapy.Field()
    category = scrapy.Field()
    section = scrapy.Field()
    characteristics = scrapy.Field()
