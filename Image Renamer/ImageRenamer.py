'''
    This script renames all the images in a particular directory to a particular format.
'''
#!python3

#   Import modules
import os
from pathlib import Path
from PIL import Image
from pprint import pprint
import re

'''
    Function that returns a new filename given a given image PATH (absolute)
'''
def getNewFilename(imagePath):
    #   Get the filebasename and extension
    fileBasename = os.path.split(imageFilePath)[1]
    extension = os.path.splitext(fileBasename)[1]
    
    try:
        image = Image.open(imageFilePath)      #   Open the image to extract the EXIF data
        image_date = image._getexif()[36867]    #   Get the datetime field in the EXIF data - returns 'yyyy:mm:dd hh:mm:ss' string

        #   Create a regex to extract the year, month and day from the image_date
        imageDateRegex = re.compile(r'''(
            ^(\d{4})    #   Year - Group 2
            :           #   Seperator
            (\d{2})     #   Month - Group 3
            :           #   Seperator
            (\d{2})     #   Day - Group 4
            \s+         #   Ends with space
            )''',re.VERBOSE)

        #   Search for the data in the EXIF data of the current image.
        image_date_re = imageDateRegex.search(image_date)

        #   Extract the year, month and day
        imageYear = image_date_re.group(2)
        imageMonth = image_date_re.group(3)
        imageDay = image_date_re.group(4)

        newFilename = f'Aneeka_First Week_{imageYear}_{imageMonth}_{imageDay}{extension}'
    except KeyError:
        print(f'{fileBasename} - No EXIF data found.')
        newFilename = f'Aneeka_First Week{extension}'
    finally:
        return newFilename

#   TODO - Loop through all the images in a directory
IMAGE_DIR = Path("D:/Pictures/2020/March/Aneeka's Album/First Month/1 week photo shoot")

image_files = IMAGE_DIR.glob('*.jpg')

#   Get the image date - Must get it from the EXIF data.
for i, imageFilePath in enumerate(image_files):
    print(f'{i+1} - ',end=' ')
    newFilename = getNewFilename(imageFilePath)
    fileBasename = os.path.split(imageFilePath)[1]
    fileDirectory = os.path.dirname(imageFilePath)
    
    #   Calculate the new file path for the new file name
    newFilePath = Path(os.path.join(fileDirectory,newFilename))
    
    if newFilePath.exists():
       newFilename_base = os.path.splitext(os.path.split(newFilePath)[1])[0]
       newFilename_ext = os.path.splitext(os.path.split(newFilePath)[1])[1]
       
       newFilename = f'{newFilename_base}_{i}{newFilename_ext}'
       
       newFilePath = os.path.join(os.path.dirname(imageFilePath),newFilename)
       
    print(f'Renaming {fileBasename} to {newFilename}...')
    imageFilePath.rename(newFilePath)

#   TODO - Rename the image to 'Aneeka_First Week_<YYYY_MM_DD>.jpg'