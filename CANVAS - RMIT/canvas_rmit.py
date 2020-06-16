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
#pprint.pprint(courses)

#   Compile a dictionary of {course_code: course_name}
courses = {}

#   Compile a dictionary of {course_id: course_name}
course_ids = {}

#   For each course, add the course code - course name into the dictionary only if the enrollment_term_id is 289 (current semester - Sem 1 2020)
for course in courses_JSON:
    if course['enrollment_term_id'] != 289:
        continue
    courses[course['course_code']] = course['name']
    course_ids[course['id']] = course['name']

#   Write the course_ids to JSON file for later use and reference.
with open('courseInfo.json', 'w') as file:
    json.dump(course_ids,file)

#   Create folders for each course
print('Creating course folders...')
#   Create a folder to store the course folders in
uni_folder = Path.cwd()/'2020 Semester 1'
os.makedirs(uni_folder,exist_ok='true')

#   For each course, create 'Lecture', 'Assignments' and 'Labs' folders
for courseCode in courses.keys():
    #   Course Code - Course Name folder
    folder_name = '{} - {}'.format(courseCode,courses[courseCode])
    os.makedirs(uni_folder/folder_name/'Lectures',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Assignments',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Labs',exist_ok='true')

#   Get a list of modules and create dictionary for them

#   Load the JSON info to extract the course IDs
JSON_DIR = Path.cwd()/'JSON'
with open(JSON_DIR/'courseInfo.json','r') as file:
    courseIDs = json.load(file)

print('Getting a list of modules for each course and writing it to file...')
course_modules = {} #   Module dictionary {course_id: [{course_modules}]}

for id in courseIDs.keys():
    #   Query the URL
    res = requests.request('GET',"https://rmit.instructure.com:443/api/v1/courses/{}/modules".format(id),headers=headers)
    res.raise_for_status()
    course_modules[id] = json.loads(res.text)

    #   Write the course_modules data for the current course to file.
    with open(JSON_DIR/'course_modules_{}.json'.format(id),'w') as file:
        json.dump(course_modules[id], file)

#       TEST
#   For the 'Week 4 - Intro to Programming (64796)' get all the items
with open(JSON_DIR/'course_modules_64796.json') as file:
    course_module = json.load(file)


#   Grab the week 4 module item
week4_module = course_module[4]

#   Get the 'items_url' from week 4
week4_items_url = week4_module['items_url']

#   Get the 'module items'
res = requests.request('GET',week4_items_url,headers=headers)
res.raise_for_status()
# Print the HTML url of the response
HTML_URL = json.loads(res.text)[1]['html_url']
print("HTML URL: %s" % HTML_URL)

driver = webdriver.Firefox()
wait = WebDriverWait(driver,10) #   Wait 10 seconds for page elements to load.

driver.get(HTML_URL)
wait.until(EC((By.ID,'Ecom_User_ID')))
username = driver.find_element_by_id('Ecom_User_ID')
username.send_keys('s3805894')
password = driver.find_element_by_id('Ecom_Password')
password.send_keys('S3pt3mb3r90')
password.send_keys(Keys.RETURN)
try:
    #   Find the element with attribute 'data-api-returntype="File"'
    wait.until(EC((By.CLASS_NAME,'instructure_file_link')))
    fileLink = driver.find_element_by_class_name('instructure_file_link')
    print(fileLink.get_attribute('href'))
except Exception as exc:
    print('Error! Message: %s' % exc)
