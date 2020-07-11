"""
	This script gets the Picture of the Day from the NASA website.
"""
import json, requests, os, tweepy
from pprint import pprint

def getNasaPOTD():
	"""
		This function queries the NASA API and downloads the POTD
	"""

	#	Get the API key
	api_key = os.getenv('NASA_API_KEY')

	params = {
		'api_key': str(api_key),
		'hd': 'true'
	}

	url = 'https://api.nasa.gov/planetary/apod'

	res = requests.request('GET', url, params=params)
	res.raise_for_status()

	resData = json.loads(res.text)

	imageTitle = resData['title']
	imageURL = resData['url']
	imageFilename = os.path.basename(imageURL)

	res = requests.request('GET', imageURL)
	res.raise_for_status()

	with open(imageFilename,'wb') as file:
		for chunk in res.iter_content(100000):
			file.write(chunk)

	#	Return info about the image
	return {'filename':imageFilename, 'title': imageTitle}

def postToTwitter(filename, status):
	"""
		Function that posts the picture to Twitter with the given 'status'
	"""

	#	Create a Tweepy object - Get the credentials from environment variables.
	api_key = os.getenv("TWITTER_API_KEY")
	api_secret = os.getenv("TWITTER_API_SECRET")
	access_token = os.getenv("TWITTER_ACCESS_TOKEN")
	access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

	auth = tweepy.OAuthHandler(api_key, api_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,
	    wait_on_rate_limit_notify=True)

	api.update_with_media(filename, status)

if __name__ == '__main__':

	#	Grab the link and download the POTD from NASA
	potd = getNasaPOTD()

	#	Post the image to twitter with a status.
	postToTwitter(potd['filename'],
		f"Check out today's Picture of the Day from NASA!\n\n{potd['title']}:")

	#	Remove the downloaded image
	os.remove(potd['filename'])
