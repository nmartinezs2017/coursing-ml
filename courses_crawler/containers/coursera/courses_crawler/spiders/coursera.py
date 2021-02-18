from time import sleep

import scrapy
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxProfile
from scrapy.loader import *
from ..items import CourseraItem

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# scrapy crawl coursera -o "coursera.csv"
def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


class CourseraSpider(scrapy.Spider):
    name = "coursera"
    start_urls = ['https://www.coursera.org/directory']
    driver = webdriver.Chrome(options=set_chrome_options())

    def parse(self, response):
        self.driver.get(response.url)
        absolute_page = "https://www.coursera.org"
        sections = response.xpath('//*[@class="c-resource-button"]/@href').extract()[1:4]
        for section in sections:
            absolute_next_page_url = absolute_page + section
            yield response.follow(absolute_next_page_url, self.parse_directory)

    def parse_directory(self, response):
        pages = response.xpath('//*[@class="c-directory-link"]/@href').extract()

        for page in pages:
            yield response.follow(page, self.parse_page)
            sleep(4)

    def parse_page(self, response):
        # initialization
        l = ItemLoader(item=CourseraItem(), response=response)
        self.driver.get(response.url)
        sleep(2)
        sel = Selector(text=self.driver.page_source)
        duration = None
        language = None
        difficulty = None
        n_reviews_spe = None
        # url
        url = response.url
        # section
        section = url.split("/")[3]
        # category
        category = sel.xpath('//*[@class="_1ruggxy"]/a/text()').extract()
        # number of students enrolled
        enrolled = sel.xpath('.//strong/span/text()').extract_first()
        # title
        title = sel.xpath('.//h1/text()').extract_first()
        # RATING
        rating = sel.xpath('//*[@data-test="number-star-rating"]/text()').extract_first()
        n_ratings = sel.xpath('//*[@class="_wmgtrl9 m-r-1s color-white"]/span/text()').extract_first()
        n_reviews = sel.xpath('//*[@class="_bd90rg"]/*//span/text()').extract_first()
        if section == 'specializations':
            n_reviews_spe = sel.xpath('//*[@class="_bd90rg"]/*//span/text()').extract_first()
        n_ratings_spe = sel.xpath('//*[@class="_wmgtrl9 color-white ratings-count-expertise-style"]/span/text()').extract_first()
        # skills
        skills = sel.xpath('//*[@class="_t6niqc3"]/span/@title').extract()
        # description
        description_spe = sel.xpath('//*[@class="description"]/*//p/text()').extract()
        description_cou = sel.xpath('//*[@class="m-t-1 description"]/*//p/text()').extract()
        description_pro = sel.xpath('//*[@class="_g61i7y"]/*//p/text()').extract()
        # CHARACTERISTICS
        # characteristics_cou = sel.xpath('//*[@class="_g61i7y"]/text()').extract()
        # spetialization
        characteristics_spe = sel.xpath('//*[@class="_16ni8zai m-b-0"]/text()').extract()
        duration_week = sel.xpath('//*[@class="font-sm text-secondary"]/span/text()').extract_first()
        if len(characteristics_spe) != 0:
            difficulty = characteristics_spe[3]
            duration = sel.xpath('//*[@class="_16ni8zai m-b-0"]/span/text()').extract_first()
            language = characteristics_spe[-1]
        # courses
        if section == 'learn':
            difficulty = sel.xpath('//*[@class="_16ni8zai m-b-0 m-t-1s"]/text()').extract_first()
            duration = sel.xpath('//*[@class="_16ni8zai m-b-0 m-t-1s"]/span/text()').extract_first()
        # LANGUAGE
        # language_cou = sel.xpath('//*[@class="_16ni8zai m-b-0 m-t-1s"]/text()').extract()
        # COLLABORATION
        # professional-certificates
        instructor = sel.xpath('//*[@class="_1qfi0x77"]/span/text()').extract_first()
        if section == 'specializations':
            instructor = sel.xpath('//*[@class="_1qfi0x77 instructor-count-display"]/span/text()').extract_first()
        institution = sel.xpath('//*[@class="_1g3eaodg"]/@title').extract_first()

        # add values
        l.add_value('id_course', url.split("/")[4])
        l.add_value('title', title)
        l.add_value('difficulty', difficulty)
        l.add_value('category', category)
        l.add_value('duration', duration)
        l.add_value('duration_week', duration_week)
        # l.add_value('school', school)
        l.add_value('rating', rating)
        l.add_value('language', language)
        l.add_value('description', description_spe)
        l.add_value('description', description_cou)
        l.add_value('description', description_pro)
        l.add_value('url', response.url)
        l.add_value('skills', skills)
        l.add_value('enrolled', enrolled)
        l.add_value('section', section)
        l.add_value('n_ratings', n_ratings)
        l.add_value('n_reviews', n_reviews)
        l.add_value('n_reviews', n_reviews_spe)
        l.add_value('n_ratings', n_ratings_spe)
        l.add_value('instructor', instructor)
        l.add_value('institution', institution)
        l.add_value('characteristics', characteristics_spe)

        return l.load_item()