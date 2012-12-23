'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
import config
from twython import Twython
import time

twitter = Twython(
    twitter_token = config.twitter_token,
    twitter_secret = config.twitter_secret,
    oauth_token = config.oauth_token,
    oauth_token_secret = config.oauth_token_secret
)

def post_tweet(text):
    global twitter
    twitter.updateStatus(status=text)
    
def post_tweet_with_image(text, image):
    global twitter
    twitter.updateStatusWithMedia(image, status=text)

def send_tweet(tweet):
    if(tweet.expires < int(time.time())):
        return
    try:
        if(tweet.picture):
            post_tweet_with_image(tweet.message, tweet.picture)
        else:
            post_tweet(tweet.message)
        return True
    except Exception:
        return False
#tweet_with_image(auth, 'Testing image attachment now', '/home/sakthipriyan/Desktop/index.jpeg')
