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
    duration_hours = scrapy.Field()
    difficulty = scrapy.Field()
    description = scrapy.Field()
    free = scrapy.Field()
    skills = scrapy.Field()
    collaboration = scrapy.Field()
    duration_weeks = scrapy.Field()
    # idioma


class CourseraItem(scrapy.Item):
    id_course = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    n_ratings = scrapy.Field()
    n_reviews = scrapy.Field()
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
