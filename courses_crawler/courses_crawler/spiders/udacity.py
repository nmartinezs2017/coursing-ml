from time import sleep

import scrapy
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from scrapy.loader import *
from courses_crawler.items import UdacityItem
# from scraper_api import ScraperAPIClient

# scrapy crawl udacity -o "salida.csv"
# scrapy crawl uda -o salida.csv

class UdacitySpider(scrapy.Spider):
    # client = ScraperAPIClient('b168278f17fd1cdc7040bcbdeed7c80a')
    name = "udacity"
    start_urls = ['https://www.udacity.com/courses/all']

    def parse(self, response):
        self.driver = Firefox(executable_path='geckodriver.exe')
        self.driver = webdriver.Chrome(options=set_chrome_options())
        self.driver.get(response.url)
        self.driver.maximize_window()
        sleep(5)
        self.driver.find_element_by_xpath('//*[@class="modal-close light"]').click()
        sleep(5)
        self.driver.find_element_by_xpath('//*[@class="button button--white acceptButton__6yUXUq"]').click()

        while True:
            sleep(5)
            try:
                program_details = self.driver.find_element_by_xpath('.//*[@class="card__bottom__button"]')
                program_details.click()
            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                break

        sel = Selector(text=self.driver.page_source)
        cards = sel.xpath('//*[@class="catalog-cards__list__item"]') # extract

        for card in cards:
            link = card.xpath('./a/@href').extract_first() #
            difficulty = card.xpath('//*[@data-level="beginner"]/text()').extract_first() #
            school = card.xpath('.//h3/text()').extract() #
            skills = card.xpath('.//*[@class="overview__5MOH/R"]/section[1]/p/text()').extract() #
            collaboration = card.xpath('.//*[@class="actionButtonsContainer__5MOH/R"]/div/p/text()').extract() #
            n_reviews = card.xpath('.//*[@class="reviews__5MOH/R"]/small/text()').extract() #
            active_stars = card.xpath('.//*[@class="active-stars"]/@style').extract() #

            self.logger.info(link)
            self.logger.info(difficulty)
            self.logger.info(school)
            self.logger.info(skills)
            self.logger.info(collaboration)
            self.logger.info(n_reviews)
            self.logger.info(active_stars)

            absolute_page = "https://www.udacity.com"

            absolute_next_page_url = absolute_page + link
            yield response.follow(absolute_next_page_url, self.parse_card, cb_kwargs=dict(difficulty=difficulty, school=school, skills=skills, collaboration=collaboration, n_reviews=n_reviews, active_stars=active_stars))

    def parse_card(self, response, difficulty, school, skills, collaboration, n_reviews, active_stars):
        l = ItemLoader(item=UdacityItem(), response=response)

        # self.driver = Firefox(executable_path='geckodriver.exe')
        # self.driver.get(response.url)
        # sel = Selector(text=self.driver.page_source)
        self.logger.info(response.url)

        description = response.xpath('//*[@class="small hidden-md-down"]/text()').extract_first()
        description_old = response.xpath('//*[@class="details__description"]/div/p/p/text()').extract_first()
        description_old2 = response.xpath('//*[@class="ng-star-inserted"]/following-sibling::p/text()').extract_first()
        duration_weeks = response.xpath('//*[@class="column-list "]/li/div/h5/text()').extract_first()
        duration_weeks_old = response.xpath('//*[@class="details__stats"]/div/div[2]/h5/text()').extract()
        duration_weeks_old2 = response.xpath('//*[@class="details__overview__item ng-star-inserted"]/text()').extract()
        duration_hours = response.xpath('//*[@class="column-list "]/li/div/p/text()').extract_first()
        # title = response.xpath('//*[@class="nd-syllabus-term__header__content"]/h2/text()').extract_first()
        title = response.xpath('//h1/text()').extract_first()
        # rating = sel.xpath('//*[@class="stats__average__rating"]/text()').extract_first()
        # n_valorations = sel.xpath('//*[@class="x-small gray mb-0"]/text()').extract()
        url:str = response.url
        id_course = url.split('--')[1]
        if id_course == 'ud803':
            self.logger.info("ud803")
            self.logger.info(duration_weeks)
            self.logger.info(duration_weeks_old)
            self.logger.info(duration_weeks_old2)
            self.logger.info(description_old)

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
        l.add_value('collaboration', collaboration)
        l.add_value('duration_weeks', duration_weeks)
        l.add_value('duration_weeks', duration_weeks_old)
        l.add_value('duration_weeks', duration_weeks_old2)
        l.add_value('duration_hours', duration_hours)

        return l.load_item()
