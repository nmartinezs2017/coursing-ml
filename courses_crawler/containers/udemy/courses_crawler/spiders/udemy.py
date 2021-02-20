
import scrapy
from scrapy import Selector, http
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.loader import *
from ..items import UdemyItem
import logging
import requests
from time import sleep
# scrapy crawl udemy -o "udemy.csv"

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

# CONFIGURATION #

CLIENT_ID = 'mSqqJGFCxs2UYF0RGMwtT1ilAvzETsxiIKufRlGq'
CLIENT_SECRET = 'AYaYDfCFFmB2GuIjTsyIZOBFr09ykiVkwQQNZMNq6yAlprFUXh4eWWzxOo5iRYuaTIaPwOLq8YyqSAhloelGbUntsgzTtY1PTNo4qqnuwsj1Pz5xDqNupMAbtdWkEfvu'
ENDPOINT = 'https://www.udemy.com/api-2.0/courses/'
CATEGORIES_DICT = ['Business', 'Lifestyle', 'Marketing', 'Udemy Free Resource Center', 'Photography & Video',
                   'Personal Development', 'Teaching & Academics', 'Development', 'Music', 'IT & Software',
                   'Office Productivity', 'Finance & Accounting', 'Health & Fitness']
SUBCATEGORIES = ['3D & Animation', 'Advertising', 'Affiliate Marketing', 'Apple',
'Architectural Design', 'Arts & Crafts', 'Beauty & Makeup', 'Branding', 'Business Law',
'Career Development', 'Commercial Photography', 'Communications', 'Content Marketing', 'Creativity',
'Dance', 'Data Science', 'Database Design & Development', 'Design Thinking', 'Design Tools', 'Development Tools',
'Dieting', 'Digital Marketing', 'Digital Photography', 'E-Commerce', 'Economics', 'Engineering', 'Entrepreneurship',
'Fashion Design', 'Finance', 'Finance Cert & Exam Prep', 'Financial Modeling & Analysis', 'Fitness', 'Food & Beverage',
'Game Design', 'Game Development', 'Gaming', 'General Health', 'Google', 'Graphic Design & Illustration', 'Growth Hacking', 'Happiness',
'Hardware', 'Home Improvement', 'Human Resources', 'Humanities', 'Industry', 'Influence', 'Instruments', 'Investing & Trading',
'Interior Design', 'IT Certification', 'Language', 'Leadership', 'Management', 'Marketing Fundamentals', 'Marketing Analytics & Automation',
'Marketing Fundamentals', 'Math', 'Media', 'Meditation', 'Memory & Study Skills', 'Mental Health', 'Microsoft', 'Mobile Development',
'Money Management Tools', 'Motivation', 'Music Fundamentals', 'Music Production', 'Music Software', 'Music Techniques', 'Network & Security',
'Nutrition', 'No-Code Development', 'Online Education', 'Operating Systems', 'Operations', 'Oracle', 'Other Business',
'Other Design', 'Other Finance & Accounting', 'Other Health & Fitness', 'Other IT & Software', 'Other Lifestyle', 'Other Marketing',
'Other Music', 'Other Office Productivity', 'Other Personal Development', 'Other Photography & Video',
'Other Teaching & Academics', 'Parenting & Relationships', 'Personal Brand Building',
'Personal Growth & Wellness', 'Personal Productivity', 'Personal Transformation', 'Pet Care & Training',
'Photography', 'Photography Tools', 'Portrait Photography', 'Product Marketing', 'Productivity & Professional Skills',
'Programming Languages', 'Project Management', 'Public Relations', 'Real Estate',
'Religion & Spirituality', 'Safety & First Aid', 'Sales', 'SAP', 'Science', 'Search Engine Optimization',
'Self Defense', 'Self Esteem & Confidence', 'Social Media Marketing', 'Social Science', 'Software Engineering',
'Software Testing', 'Sports', 'Stress Management', 'Teacher Training', 'Test Prep', 'Taxes',
'Travel', 'User Experience Design', 'Video & Mobile Marketing', 'Video Design', 'Vocal', 'Vodafone', 'Web Design',
'Web Development', 'Yoga']
AUTH = ('mSqqJGFCxs2UYF0RGMwtT1ilAvzETsxiIKufRlGq',
        'AYaYDfCFFmB2GuIjTsyIZOBFr09ykiVkwQQNZMNq6yAlprFUXh4eWWzxOo5iRYuaTIaPwOLq8YyqSAhloelGbUntsgzTtY1PTNo4qqnuwsj1Pz5xDqNupMAbtdWkEfvu')


# SPIDER #

class UdemySpider(scrapy.Spider):
    name = "udemy"
    start_urls = ['https://www.udemy.com/']
    absolute_page = "https://www.udemy.com"

    def parse(self, response):
        for subcategory in SUBCATEGORIES:
                param = {'ordering': 'highest-rated', 'subcategory': subcategory, 'ordering': 'highest-rated'}
                response_courses = requests.get(ENDPOINT, auth=AUTH, params=param)
                json_response = response_courses.json()
                while json_response['next'] != None:
                    response_courses = requests.get(json_response['next'], auth=AUTH)
                    while response_courses.status_code == 504:
                        sleep(10)
                        response_courses = requests.get(json_response['next'], auth=AUTH)
                    try:
                        json_response = response_courses.json()
                    except Exception:
                        break
                    try:
                        courses = json_response['results']
                        if len(courses) == 0:
                            logging.info("Empty results.")
                    except Exception:
                        logging.exception("Exception raised.")
                    for course in courses:
                        link = course['url']
                        absolute_next_page_url = self.absolute_page + link
                        yield http.Request(absolute_next_page_url, self.parse_course,
                                              cb_kwargs=dict(title=course['title'], cost=course['price'], subcategory=subcategory,
                                                             is_free=not course['is_paid'], id_course=course['id'],
                                                             instructor=course['visible_instructors'][0]['title'],
                                                             instructor_url=course['visible_instructors'][0]['url'],
                                                             description=course['headline']))
                print(
                    "\n{} free courses were found in the subcategory {}\n".format(json_response['count'], subcategory))
            #except Exception:
            #    logging.critical("Error grave de conexión")
             #   sleep(50)

    def parse_course(self, response, title, cost, subcategory, is_free, description, id_course, instructor, instructor_url):
        self.driver = webdriver.Chrome(options=set_chrome_options())
        self.driver.get(response.url)
        self.driver.maximize_window()
        sel = Selector(text=self.driver.page_source)

        rating = sel.xpath('.//*[@data-purpose="rating-number"]/text()').extract_first()
        n_students = sel.xpath('.//*[@data-purpose="enrollment"]/text()').extract_first()
        duration = sel.xpath('.//*[@data-purpose="curriculum-stats"]/span/span/span/text()').extract()
        sessions = sel.xpath('.//*[@data-purpose="curriculum-stats"]/span/text()').extract()
        category = sel.xpath('.//*[@class="udlite-heading-sm"]/text()').extract_first()
        language = sel.xpath('.//*[@data-purpose="lead-course-locale"]/text()').extract()
        description_extend = sel.xpath('.//*[@data-purpose="safely-set-inner-html:description:description"]/descendant-or-self::*/text()').extract()
        l = ItemLoader(item=UdemyItem(), response=response)

        l.add_value('id_course', id_course)
        l.add_value('title', title)
        l.add_value('rating', rating)
        l.add_value('n_students', n_students)
        l.add_value('url', response.url)
        l.add_value('duration', duration)
        l.add_value('description', description)
        l.add_value('description_extend', description_extend)
        l.add_value('instructor', instructor)
        l.add_value('language', language)
        l.add_value('category', category)
        l.add_value('subcategory', subcategory)
        l.add_value('sessions', sessions)
        l.add_value('cost', cost)
        l.add_value('free', is_free)

        return l.load_item()