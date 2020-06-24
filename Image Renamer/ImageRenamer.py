'''
    This script renames all the images in a particular directory to a particular format.
'''
#!python3

#   Import modules
import os
from pathlib import Path, PureWindowsPath
from PIL import Image
import re

def getNewFilename(absImagePath, seqNo):
    '''
        Function that returns a new filename.
        Arguments:
            -   absImagePath:  Absolute path to the image as a Path object.
            -   seqNo:   The sequence number
        Returns:
            -   A string containing the new filename in the format <suffix>_<yyyy_mm_dd>_<seqNo>.<ext>
            If the 'Date Taken' attribute is not able to be found, then a default renaming scheme is applied.
    '''
    #   Get the basename of the file and the extension
    basename = os.path.basename(absImagePath)
    fileExt = os.path.splitext(basename)[1]
    
    #   Leading filename text - CHANGE ACCORDING TO NEEDS
    leadingText = 'CHANGE LEADING TEXT OF FILE'
    
    try:
        #   Open the image to extract the EXIF data and get the date the picture was taken
        image = Image.open(absImagePath)
        image_date_taken = image._getexif()[36867]    #   Get the datetime field in the EXIF data - returns 'yyyy:mm:dd hh:mm:ss' string

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
        image_date_re = imageDateRegex.search(image_date_taken)

        #   Extract the year, month and day
        imageYear = image_date_re.group(2)
        imageMonth = image_date_re.group(3)
        imageDay = image_date_re.group(4)

        #   Construct the new filename appending the date to the end of it.
        newFilename = f'{leadingText}_{imageYear}_{imageMonth}_{imageDay}_{seqNo}{fileExt}'
        
    except Exception as error:
        '''
            If an exception occurs apply a default name to the filename.
        '''
        print(f'Error opening file: {str(error)}. Applying default renaming...')
        newFilename = f'{leadingText}_{seqNo}{fileExt}'
    finally:
        #   Return the new filename.
        return newFilename

#   MAIN
if __name__ == '__main__':
    
    #   Directory containing the images to rename - CHANGE AS REQUIRED
    windowsPath = PureWindowsPath(r"/path/to/directory/")   #   Required on Windows platforms.
    IMAGE_DIR = Path(windowsPath.as_posix())

    #   Loop through each item in the directory and rename the item if it is a file.
    for i, imageFile in enumerate(os.listdir(IMAGE_DIR)):
        imageFilePath = IMAGE_DIR/imageFile
        
        #   If the current item is a directory then pass.
        if (imageFilePath).is_dir():
            continue
            
        print(f'Image {i+1} - ',end=' ')
        
        #   Get a new filename for the current image
        newFilename = getNewFilename(imageFilePath,i+1)
        
        #   Calculate the new file path for the new file name
        newFilePath = IMAGE_DIR/newFilename
           
        print(f'Renaming {imageFile} to {newFilename}...')
        imageFilePath.rename(newFilePath)