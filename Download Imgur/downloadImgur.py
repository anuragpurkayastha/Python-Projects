'''
    A script that downloads the top item in the "Funny" gallery.

    The images are downloaded to a folder named 'imgur' under a subfolder with the date of the post as the name in the current working directory from which the
    script is called.

    This script makes use of the Imgur API.
'''
#!python3

#   Import modules
import os, requests, json
import pprint
from pathlib import Path
import time
from ezgmail import send

'''
    Name:   sendNotification
    Arguments:
        -   Link to the image or album
    Returns:
        -   None => sends email notification of downloaded image
'''
def sendNotification(link):
    message = r'''A new post has been downloaded!
The post can be found at:

{}
            '''.format(link)

    send('anuragpurkayastha@gmail.com',
        'Imgur - Top Post of the Day',
        message)
'''
    Name:   getTopPost
    Arguments:
        -   None
    Returns:
        The top post of the day from 'Funny' on Imgur, formatted as JSON data
'''
def getTopPost():
    #   URL to query - sort by top by day
    url = "https://api.imgur.com/3/gallery/t/funny/top/day"

    response = requests.request("GET", url, headers=headers, data = payload, files = files)
    response.raise_for_status()

    #   The response - JSON data format
    galleryData = json.loads(response.text)

    return galleryData['data']['items'][0]

'''
    Name:   getImageURLS
    Arguments:
        -   itemInfo:   JSON data of the item
    Returns:
        List of image urls for all of the images in the item
'''
def getImageURLs(itemInfo):

    #   Get the item ID which is used to query the Imgur API.
    itemID = itemInfo['id']
    imageURLs = []  #   List to contain the image URLs of all the images in the item

    #   Get the image URL(s)
    if itemInfo['is_album']:

        #   Get the albumURL - takes album ID as parameter (this is the itemID)
        mediaURL = 'https://api.imgur.com/3/album/{}'.format(itemID)

        response = requests.request('GET', mediaURL, headers=headers, data = payload, files = files)
        response.raise_for_status()

        #   Process the response to get all the image links of the images in the album
        album = json.loads(response.text)
        albumImages = album['data']['images']   #   A list of all the images in the album

        #   Loop through the list of images in the album
        for image in albumImages:
            imageURLs.append(image['link'])
    else:
        mediaURL = 'https://api.imgur.com/3/gallery/image/{}'.format(itemID)

        response = requests.request('GET', mediaURL, headers=headers, data = payload, files = files)
        response.raise_for_status()

        image = json.loads(response.text)

        #   Image link
        imageURLs.append(image['data']['link'])

    return imageURLs

#   MAIN
if __name__ == '__main__':

    #   Authorization creds to use IMGUR_API - obtain from environment variables
    CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
    CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET')

    payload = {}
    files = {}
    headers = {
      'Authorization': 'Client-ID %s' % CLIENT_ID
    }

    #   Grab the top post
    print('\nGetting top post from "Funny" on Imgur...')
    topPost = getTopPost()
    topPostDate = topPost['datetime']   #   The datetime of the album in EPOCH time

    #   Make directory to store the images for today. format: <post_year>_<post_month>_<post_day>
    folderName = time.strftime('%Y_%m_%d',time.localtime(topPostDate))
    IMGUR_DIR = Path.cwd()/'imgur'/folderName
    os.makedirs(IMGUR_DIR,exist_ok='true')

    #   Get a list of the image URLs.
    imageURLs = getImageURLs(topPost)

    #   Iterate over each image URL and download each file to the folder.
    for i,imageURL in enumerate(imageURLs):
        #   Download the image
        if (i+1) != len(imageURLs):
            print("Downloading post %s of %s..." % (i+1, len(imageURLs)),end='\r')
        else:
            print("Downloading image %s of %s..." % (i+1,len(imageURLs)),end='')

        #   Download the image/media file to the directory.
        #   Filename format is '<Year>_<month>_<day>_<i>.<ext>'
        filename = '%s_%s%s' % (time.strftime('%Y_%m_%d',time.localtime(topPostDate)),i+1,os.path.splitext(imageURL)[1])
        pathToFile = Path(IMGUR_DIR)/filename

        #   Download the image and save it to the file
        res = requests.get(imageURL)
        res.raise_for_status()

        with open(pathToFile,'wb') as file:
            for chunk in res.iter_content(100000):
                file.write(chunk)

    print('done.')
    print("Creating info text file...",end='')
    #   Create a text file with some details of the image
    filename = '%s_imageInfo.txt' % (time.strftime('%Y%m%d',time.localtime(topPostDate)))

    with open(Path(IMGUR_DIR)/filename,'w') as file:
        file.write('TITLE: %s\n' % (topPost['title']))
        file.write('POST DATE: %s\n\n' % (time.strftime('%d/%m/%Y',time.localtime(topPostDate))))
        file.write('DESCRIPTION:\n%s\n' % (topPost['description']))

    print('done.')
    print('Sending email notification...',end='')
    sendNotification(topPost['link'])
    print('done.')
