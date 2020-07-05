'''
    This is a script that retrieves the top 'Funny' post from Imgur and tweets it to a twitter account.
'''
#!python3

#   Import modules
import os, requests, json
import tweepy

def sendNotification(link):
	'''
	    Function that tweets a link.
	'''

	#	Create a Tweepy object - Get the credentials from environment variables.
	api_key = os.getenv("TWITTER_API_KEY")
	api_secret = os.getenv("TWITTER_API_SECRET")
	access_token = os.getenv("TWITTER_ACCESS_TOKEN")
	access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

	auth = tweepy.OAuthHandler(api_key, api_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,
	    wait_on_rate_limit_notify=True)

	try:
		api.update_status(r"Today's top post from Imgur: %s" % link)
	except tweepy.error.TweepError as err:
		pass
		#print("Could not post to Twitter. Error: %s" % str(err))


def getTopPostURL():
	'''
		Return the link to the top 'Funny' post off Imgur
	'''
	#   Authorization creds to use IMGUR_API - obtain from environment variables
	CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

	headers = {
	  'Authorization': 'Client-ID %s' % CLIENT_ID
	}

	#   URL to query - sort by top by day
	url = "https://api.imgur.com/3/gallery/t/funny/top/day"

	response = requests.request("GET", url, headers=headers)
	response.raise_for_status()

	#   The response - JSON data format
	galleryData = json.loads(response.text)

	#	Return the link to the post
	return galleryData['data']['items'][0]['link']

def shortenURL(url):
	"""
		Shorten the url
	"""
	headers = {
	  'Authorization': 'Bearer %s' % os.getenv('BITLY_ACCESS_TOKEN'),
	  'Content-Type': 'application/json'
	}

	payload = {
		'long_url': url
	}

	res = requests.request('POST','https://api-ssl.bitly.com/v4/shorten',headers=headers,json=payload)
	res.raise_for_status()
	resData = json.loads(res.text)

	return resData['link']

#   MAIN
if __name__ == '__main__':

	#   Grab the top post
	#print('\nGetting top post URL from "Funny" on Imgur...',end='')
	topPostURL = getTopPostURL()
	#print('done.')

	sendNotification(shortenURL(topPostURL))
