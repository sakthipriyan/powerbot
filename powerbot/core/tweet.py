'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
from twython import Twython
import config
import logging
import urllib2 
import os
from powerbot.core.config import tweet_file

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
    
    if(not os.path.isfile(tweet_file)):    
        logging.info('Tweeting is not enabled. To enable, touch ' + tweet_file)
        return
    
    try:
        logging.info('Sending...' + str(tweet))
        if(tweet.picture):            
            post_tweet_with_image(tweet.message, tweet.picture)
        else:
            post_tweet(tweet.message)
        return True
    except Exception, e:
        logging.error('Failed to send ' + str(tweet) + str(e))
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
        urllib2.urlopen('http://www.google.com',timeout=10)
        return True
    except Exception: 
        pass    
    return False
#tweet_with_image(auth, 'Testing image attachment now', '/home/sakthipriyan/Desktop/index.jpeg')
