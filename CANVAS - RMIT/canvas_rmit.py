'''
    This is a script to query the Canvas API. It gets all of the course details for the current semester and creates folders for each course.

    TODO:   Access the module item HTML_URL with login page.
'''
#   Import modules
import os, requests, json
from pprint import pprint
from pathlib import Path

#   SELENIUM
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from pprint import pprint

#   Credentials
CANVAS_SECRET = os.getenv('CANVAS_SECRET')

headers = {
  'Authorization': 'Bearer %s' % CANVAS_SECRET
}

print('Getting a list of courses...')
res = requests.request('GET',"https://rmit.instructure.com/api/v1/courses",headers=headers)
res.raise_for_status()

courses_JSON = json.loads(res.text)

#   Print the raw JSON response data
#pprint(courses_JSON)

#   Compile a dictionary of {course_code: course_name}
courses = {}

#   Compile a dictionary of {course_id: course_name}
course_ids = {}

#   For each course, add the course code - course name into the dictionary only if the enrollment_term_id is 289 (current semester - Sem 1 2020)
for course in courses_JSON:
    if course['enrollment_term_id'] != 311:
        continue
    courses[course['course_code']] = course['name']
    course_ids[course['id']] = course['name']

#   Create folders for each course
print('Creating course folders...')
#   Create a folder to store the course folders in
uni_folder = Path.cwd()/'2020 Semester 2'
os.makedirs(uni_folder,exist_ok='true')

#   For each course, create 'Lecture', 'Assignments' and 'Labs' folders
for courseCode in courses.keys():
    #   Course Code - Course Name folder
    folder_name = '{} - {}'.format(courseCode,courses[courseCode])
    os.makedirs(uni_folder/folder_name/'Lectures',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Assignments',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Labs',exist_ok='true')
