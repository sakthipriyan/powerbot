'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
from twython import Twython
import config
import logging
import urllib2

twitter = Twython(
    twitter_token = config.twitter_token,
    twitter_secret = config.twitter_secret,
    oauth_token = config.oauth_token,
    oauth_token_secret = config.oauth_token_secret
)

wait_time_index = -1;

def post_tweet(text):
    global twitter
    twitter.updateStatus(status=text)
    
def post_tweet_with_image(text, image):
    global twitter
    twitter.updateStatusWithMedia(image, status=text)

def send_tweet(tweet):
    try:
        if(tweet.picture):
            post_tweet_with_image(tweet.message, tweet.picture)
        else:
            post_tweet(tweet.message)
        logging.info('Sending ' + str(tweet))
        return True
    except Exception:
        logging.error('Failed to send ' + str(tweet))
        return False
    
def get_wait_time():
    wait_time = (1,2,4,8,16,32)
    length = len(wait_time)
    global wait_time_index
    wait_time_index = wait_time_index + 1
    if wait_time_index == length:
        wait_time_index = 0
    return wait_time[wait_time_index]

def internet_on():
    try:
        urllib2.urlopen('http://74.125.113.99',timeout=5)
        return True
    except urllib2.URLError: 
        pass    
    return False
#tweet_with_image(auth, 'Testing image attachment now', '/home/sakthipriyan/Desktop/index.jpeg')
