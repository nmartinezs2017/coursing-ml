
import scrapy
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from scrapy.loader import *
from ..items import UdemyItem

# scrapy crawl udemy -o "udemy.csv"


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

    def parse(self, response):


    def parse_course(self, response):
        self.driver = Firefox(executable_path='geckodriver.exe')
        self.driver.get(response.url)
        self.driver.maximize_window()
        sel = Selector(text=self.driver.page_source)

        rating = sel.xpath('.//*[@data-purpose="rating-number"]/text()').extract_first()
        n_students = sel.xpath('.//*[@data-purpose="enrollment"]/text()').extract_first()
        duration = sel.xpath('.//*[@data-purpose="video-content-length"]/text()').extract_first()
        sessions = sel.xpath('.//*[@data-purpose="curriculum-stats"]/span/text()').extract_first()
        description_extend = sel.xpath('.//*[@data-purpose="safely-set-inner-html:description:description"]/descendant-or-self::*/text()').extract()

        l = ItemLoader(item=UdemyItem(), response=response)

        l.add_value('id_course', id_course)
        l.add_value('title', title)
        l.add_value('rating', rating)
        l.add_value('n_students', n_students)
        l.add_value('url', url)
        l.add_value('duration', duration)
        l.add_value('description', description)
        l.add_value('description_extend', description_extend)
        l.add_value('instructor', instructor)
        l.add_value('language', language)
        l.add_value('category', category)
        l.add_value('sessions', sessions)
        l.add_value('cost', cost)
        l.add_value('free', free)

        return l.load_item()