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

	api.update_status(r"Today's top post: %s" % link)

def getTopPostURL():
	'''
		Return the link to the top 'Funny' post off Imgur
	'''
	#   Authorization creds to use IMGUR_API - obtain from environment variables
	CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
	CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET')

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

#   MAIN
if __name__ == '__main__':

	#   Grab the top post
	print('\nGetting top post URL from "Funny" on Imgur...',end='')
	topPostURL = getTopPostURL()
	print('done.')

	#print(f'The link is: {topPostLink}')
	sendNotification(topPostURL)
