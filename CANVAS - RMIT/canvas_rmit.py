'''
    This is a script to query the Canvas API. It gets all of the course details for the current semester and creates folders for each course.
'''
#   Import modules
import os, requests, json
import pprint
from pathlib import Path

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
courses={}

#   For each course, add the course code - course name into the dictionary only if the enrollment_term_id is 289 (current semester)
for course in courses_JSON:
    if course['enrollment_term_id'] != 289:
        continue
    courses[course['course_code']] = course['name']

#   Create a folder to store the course folders in
uni_folder = Path.cwd()/'2020 Semester 1'
os.makedirs(uni_folder,exist_ok='true')

#   For each course, create 'Lecture', 'Assignments' and 'Labs' folders
print('Creating course folders...')
for key in courses.keys():
    #   Course Code - Course Name folder
    folder_name = '{} - {}'.format(key,courses[key])
    os.makedirs(uni_folder/folder_name/'Lectures',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Assignments',exist_ok='true')
    os.makedirs(uni_folder/folder_name/'Labs',exist_ok='true')

#pprint.pprint(courses)
