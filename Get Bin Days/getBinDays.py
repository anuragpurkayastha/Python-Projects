'''
    This is a script that scrapes the council website to find the bin days.

    It makes use of the selenium package to automate browser activities.

    NOTE: Only works for Firefox. Adjust driver settings for other browsers.
'''
#!python3

#   Import modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

print("Gathering bin collection information...\n")

#   Implement the WebDriver for Firefox

#   Headless - no GUI
driverOpts = Options()
driverOpts.add_argument('-headless')
driver = webdriver.Firefox(options = driverOpts)
wait = WebDriverWait(driver,10) #   Wait 10 seconds for page elements to load.

#   Search for the residential address and wait for the response
try:
    #   Go to the council's rubbish collection website.
    driver.get('https://www.melton.vic.gov.au/Near-Me')

    #   Wait until the search input bar is loaded.
    wait.until(EC((By.ID,'intramaps-full-text-search')))

    #   Search for the address
    search = driver.find_element_by_id('intramaps-full-text-search')    #   Search bar
    search.send_keys("14 Fellows St")   #   Address to search for
    search.send_keys(Keys.ENTER)    #   Press ENTER

    #   Wait for the 'Waste days' element to load
    wait.until(EC((By.CLASS_NAME,'intramaps-waste__day')))

    #   Get the elements that contain info about all the collection days
    collectionDaysList = driver.find_elements_by_class_name('intramaps-waste__day')

    # The first 3 elements of collection days elements are the 'Garbage', 'Recycling', 'Green Waste' dates. Create a dictionary with the waste type as the key and the HTML elements as the values.
    collectionDays = {'Garbage': collectionDaysList[0],
        'Recycling': collectionDaysList[1],
        'Green Waste': collectionDaysList[2]}

except Exception as exc:
    print("Error: " + str(exc))

#   For each collectionDay item, create 'caption' and 'value' dictionaries, which contain the text for the caption and value, respectively.
#   e.g collectionDay_caption = {'Garbage':['Collection Day','Waste Area'],...}
collectionDay_captions = {}
collectionDay_values = {}

#   For each element in the 'collectionDays' dictionary, get the HTML code of the values, parse them through BeautifulSoup, and then save the content of the HTML code to corresponding lists.
for key in collectionDays.keys():

        soup = BeautifulSoup(collectionDays[key].get_attribute('outerHTML'),
            'html.parser')

        #   Get the element captions
        captions = soup.find_all(class_='intramaps-waste__caption')
        values = soup.find_all(class_='intramaps-waste__value')

        collectionDay_captions[key] = []
        collectionDay_values[key] = []

        for i in range(len(captions)):
            collectionDay_captions[key].append(captions[i].string)
            collectionDay_values[key].append(values[i].string)

for key in collectionDay_captions.keys():
    print(key.upper())

    for i in range(len(collectionDay_captions[key])):
        print('%s:\t%s' % (collectionDay_captions[key][i],collectionDay_values[key][i]))
    print('=' * 80)
