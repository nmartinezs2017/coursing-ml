from time import sleep

import scrapy
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from scrapy.loader import *
from ..items import UdacityItem

# scrapy crawl udacity -o "udacity_scrapped.csv"

class UdacitySpider(scrapy.Spider):
    name = "udacity"
    start_urls = ['https://www.udacity.com/courses/all']

    def parse(self, response):
        self.driver = Firefox(executable_path='geckodriver.exe')
        self.driver.get(response.url)
        self.driver.maximize_window()
        sleep(5)
        try:
            self.driver.find_element_by_xpath('//*[@class="modal-close light"]').click()
        except NoSuchElementException:
            ...
        try:
            self.driver.find_element_by_xpath('//*[@class="modal-close light"]').click()
        except NoSuchElementException:
            ...
        sleep(5)
        try:
            self.driver.find_element_by_xpath('//*[@class="button button--white acceptButton__6yUXUq"]').click()
        except NoSuchElementException:
            self.driver.find_element_by_xpath('//*[@class="button button--white cookie-consent_acceptButton__33VaL"]').click()

        sel = Selector(text=self.driver.page_source)
        cards = sel.xpath('//*[@class="catalog-cards__list__item"]')

        for card in cards:
            link = card.xpath('./a/@href').extract_first()
            difficulty = card.xpath('.//*[@class="stats__5MOH/R"]/li[1]/@data-level').extract_first()
            duration = card.xpath('.//*[@class="stats__5MOH/R"]/li[2]/text()').extract_first()
            free = card.xpath('.//*[@data-type="free"]/small/text()').extract_first()
            school = card.xpath('.//h3/text()').extract()
            skills = card.xpath('.//*[@class="overview__5MOH/R"]/section[1]/p/text()').extract()
            collaboration = card.xpath('.//*[@class="actionButtonsContainer__5MOH/R"]/div/p/text()').extract()
            n_reviews = card.xpath('.//*[@class="reviews__5MOH/R"]/small/text()').extract()
            active_stars = card.xpath('.//*[@class="active-stars"]/@style').extract()

            if (free == 'Free'):
                is_free = True
            else:
                is_free = False

            absolute_page = "https://www.udacity.com"

            absolute_next_page_url = absolute_page + link
            yield response.follow(absolute_next_page_url, self.parse_card, cb_kwargs=dict(difficulty=difficulty, school=school, skills=skills, is_free=is_free, collaboration=collaboration, n_reviews=n_reviews, active_stars=active_stars, duration=duration))

    def parse_card(self, response, difficulty, school, skills, collaboration, n_reviews, active_stars, is_free, duration):
        l = ItemLoader(item=UdacityItem(), response=response)

        description = response.xpath('//*[@class="small hidden-md-down"]/text()').extract_first()
        description_old = response.xpath('//*[@class="summary-text"]/p/text()').extract()
        description_old2 = response.xpath('//*[@class="ng-star-inserted"]/following-sibling::p/text()').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        url:str = response.url
        id_course = url.split('--')[1]

        l.add_value('id_course', id_course)
        l.add_value('title', title)
        l.add_value('difficulty', difficulty)
        l.add_value('school', school)
        l.add_value('rating', active_stars)
        l.add_value('n_reviews', n_reviews)
        l.add_value('description', description)
        l.add_value('description', description_old)
        l.add_value('description', description_old2)
        l.add_value('url', response.url)
        l.add_value('skills', skills)
        l.add_value('free', is_free)
        l.add_value('collaboration', collaboration)
        l.add_value('duration', duration)

        return l.load_item()
