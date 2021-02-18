from time import sleep

import requests
import pandas as pd
import logging

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


# FUNCTIONS #

# MAIN #

#response = requests.get(ENDPOINT, auth=AUTH, params=PARAMS)
# json_response = response.json()  # dict con 'count', 'next', 'previous', 'results', 'aggregations', 'seach_tracking_id'
# courses_list = json_response['results']

# '_class', 'id', 'title', 'url', 'is_paid', 'price', 'price_detail', 'price_serve_tracking_id', 'visible_instructors', 'image_125_H', 'image_240x135', 'is_practice_test_course', 'image_480x270', 'published_title', 'tracking_id', 'predictive_score', 'relevancy_score', 'input_features', 'lecture_search_result', 'curriculum_lectures', 'order_in_results', 'curriculum_items', 'headline', 'instructor_name'

#response = requests.get(ENDPOINT, auth=AUTH, params={'page':214, 'page_size':12, 'subcategory':'Graphic Design & Illustration'})
#print(response.json())
id_list = []
title_list = []
url_list = []
for subcategory in SUBCATEGORIES:
    try:
        param = {'ordering': 'highest-rated', 'subcategory': subcategory, 'ordering': 'highest-rated'}
        response = requests.get(ENDPOINT, auth=AUTH, params=param)
        json_response = response.json()
        while json_response['next'] != None:
            response = requests.get(json_response['next'], auth=AUTH)
            while response.status_code == 504:
                sleep(10)
                response = requests.get(json_response['next'], auth=AUTH)
            try:
                json_response = response.json()
            except Exception:
                break
            print(json_response)
            try:
                courses = json_response['results']
                if len(courses) == 0:
                    logging.info("Empty results.")
            except Exception:
                logging.exception("Exception raised.")
            for course in courses:
                id_list.append(course['id'])
                title_list.append(course['title'])
                url_list.append(course['url'])
        print("\n{} free courses were found in the subcategory {}\n".format(json_response['count'], subcategory))
    except Exception:
        logging.critical("Error grave de conexión")
        sleep(50)

dct = {'title': title_list, 'id': id_list, 'url': url_list}
df = pd.DataFrame(dct)
print(df)