'''
    This is a script to query the Canvas API. It gets all of the course details for the current semester and creates folders for each course.

    TODO:   Access the module item HTML_URL with login page.
'''
#   Import modules
import os, requests, json
from pprint import pprint
from pathlib import Path, PureWindowsPath
from pprint import pprint

#   Credentials
CANVAS_SECRET = # Insert Bearer Token here

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

#pprint(courses)
#pprint(course_ids)

#   Create folders for each course
print('Creating course folders...')
#   Create a folder to store the course folders in
windowsPath = PureWindowsPath(r"D:/OneDrive - RMIT University/2020 Semester 2")
UNI_DIR = Path(windowsPath.as_posix())
os.makedirs(UNI_DIR,exist_ok='true')

#   For each course, create 'Lecture', 'Assignments' and 'Labs' folders
for courseCode in courses.keys():
    #   Course Code - Course Name folder
    folder_name = '{} - {}'.format(courseCode,courses[courseCode])
    os.makedirs(UNI_DIR/folder_name/'Lectures',exist_ok='true')
    os.makedirs(UNI_DIR/folder_name/'Assignments',exist_ok='true')
    os.makedirs(UNI_DIR/folder_name/'Labs',exist_ok='true')
