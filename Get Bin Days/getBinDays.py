'''
    This is a script that scrapes the Melton and Point Cook council websites to find the bin collection days.

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
from pprint import pprint

#================================ END IMPORTS ==============================================

''' MELTON ADDRESS '''
MELTON_ADDR = "13 Borrowdale Rd"

print('Gathering bin collection information for %s...\n' % MELTON_ADDR.upper())

#   Implement the WebDriver for Firefox

#   Headless - no GUI
driverOpts = Options()
driverOpts.add_argument('-headless')
driver = webdriver.Firefox(options = driverOpts)
wait = WebDriverWait(driver,10) #   Wait 10 seconds for page elements to load.


#       MELTON
#   Search for the residential address and wait for the response
try:
    #   Go to the Melton council's rubbish collection website.
    driver.get('https://www.melton.vic.gov.au/Near-Me')

    #   Wait until the search input bar is loaded.
    wait.until(EC((By.ID,'intramaps-full-text-search')))

    #   Search for the address
    search = driver.find_element_by_id('intramaps-full-text-search')    #   Search bar
    search.send_keys(MELTON_ADDR)   #   Address to search for
    search.send_keys(Keys.ENTER)    #   Press ENTER

    #   Wait for the 'Waste days' element to load
    wait.until(EC((By.CLASS_NAME,'intramaps-waste__day')))

    #   Get the elements that contain info about all the collection days
    wasteDayElements = driver.find_elements_by_class_name('intramaps-waste__day')

    # The first 3 elements of collection days elements are the 'Garbage', 'Recycling', 'Green Waste' dates. Create a dictionary with the waste type as the key and the HTML elements as the values.
    wasteDays_MEL_HTML = {'Garbage': wasteDayElements[0].get_attribute('outerHTML'),
        'Recycling': wasteDayElements[1].get_attribute('outerHTML'),
        'Green Waste': wasteDayElements[2].get_attribute('outerHTML')}

except Exception as exc:
    print("Error: " + str(exc))

#   Create a waste info dictionary for Melton. This has 'waste type' as the key, and the information related to that waste type as a value which is also a dictionary.
#   e.g {'Garbage':{'Next date':'22 June 2020', 'Waste Area': 'A'}}
wasteDayInfo_MEL = {}

#   For each HTML element, get the 'caption' and 'value' and store them in the dictionary
for wasteType in wasteDays_MEL_HTML.keys():

        soup = BeautifulSoup(wasteDays_MEL_HTML[wasteType],
            'html.parser')

        #   Get the caption and value elements from the current HTML element
        captions = soup.find_all(class_='intramaps-waste__caption')
        values = soup.find_all(class_='intramaps-waste__value')

        #   Temp dictionary to store in the main dictionary. {key: 'caption', value: 'value'}
        wasteDayInfo_values = {}

        #   For each caption-value pair, save it into the dictionary 'wasteDayInfo_values'
        for i in range(len(captions)):
            wasteDayInfo_values[captions[i].string] = values[i].string

        wasteDayInfo_MEL[wasteType] = wasteDayInfo_values

#       POINT COOK
#   Get the dates for Point Cook
driver.get('https://digital.wyndham.vic.gov.au/myWyndham/?propnum=187817&radius=3000&mapfeatures=')

try:
    wait.until(EC((By.CLASS_NAME,'waste')))

    #   Get all the 'waste info elements'
    waste_info_elements = driver.find_elements_by_class_name('waste')

    wasteDayInfo_PC = {}

    #   The first 3 elements contain the appropriate info
    for elem in waste_info_elements[:3]:
        soup = BeautifulSoup(elem.get_attribute('outerHTML'),'html.parser')

        #   Get the string
        splitString = soup.string.split(':')
        wasteDayInfo_PC[splitString[0]] = splitString[1]

except Exception as exc:
    print('Error: %s' % exc)

#           Print the results for melton
print('MELTON'.center(80))
for wasteType in wasteDayInfo_MEL.keys():
    print('\t'+wasteType.upper())

    for wasteInfoVal in wasteDayInfo_MEL[wasteType]:
        print('\t%s:\t%s' % (wasteInfoVal, wasteDayInfo_MEL[wasteType][wasteInfoVal]))
    print('\t'+'=' * 80)

print('\t'+'#' * 80)

print('\n'+'POINT COOK'.center(80)+'\n')
for garbageType in wasteDayInfo_PC.keys():
    print('\t%s:\t%s' % (garbageType, wasteDayInfo_PC[garbageType]))
    print('\t'+'=' * 80)
