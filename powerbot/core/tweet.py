'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
import config
from twython import Twython

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
    
#tweet(auth, 'hello from eclipse')
#tweet_with_image(auth, 'Testing image attachment now', '/home/sakthipriyan/Desktop/index.jpeg')
