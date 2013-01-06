'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

from powerbot.core.sensor import get_status, init_sensor
import time
import threading
from powerbot.database.models import StateChange, Tweet
from powerbot.database import access
import datetime
from Queue import Queue
import logging
from threading import Lock
from powerbot.database.access import init_database

old_status = True
state_change_queue = Queue()
tweet_ready_lock = Lock()

def get_message_with_ts(stateChange):
    message = access.get_message(stateChange)
    flag =  getStatusName(stateChange.new_state)
    sign =  datetime.datetime.fromtimestamp(stateChange.timestamp).strftime("  ~ %H:%M "+flag)
    return message.message + sign

def getStatusName(state):
    return 'ON' if state else 'OFF'

def do_sensing():
    while True:
        new_status = get_status()
        global old_status, state_change_queue
        if(new_status != old_status):
            logging.info('Status changed from ' + getStatusName(old_status) + ' to '  + getStatusName(new_status))
            old_status = new_status
            state_change = StateChange(1 if new_status else 0, int(time.time()))
            state_change_queue.put(state_change)
        time.sleep(1)

def process_change():
    global state_change_queue
    while True:
        stateChange = state_change_queue.get()
        access.new_state_change(stateChange)
        tweet = Tweet(stateChange.timestamp, get_message_with_ts(stateChange) , None, stateChange.timestamp + 600)
        access.new_tweet(tweet)

def process_tweets():
    global tweet_ready_lock
    while True:
        logging.info('Supposed to send tweets')
        time.sleep(200)

def process_reports():
    while True:
        logging.info('Supposed to generate reports')
        time.sleep(500)

def main():    
    logging.basicConfig(#filename='powerbot.log', 
                        format='%(asctime)s [%(threadName)s] %(message)s', datefmt= "%Y-%m-%d %H:%M:%S",
                         level=logging.INFO)
    logging.info('### Running POWER BOT service ###')
    init_database()
    init_sensor()
    
    senseThread = threading.Thread(target = do_sensing)    
    senseThread.setName('SenseThread')
    
    processThread = threading.Thread(target = process_change)
    processThread.setName('ProcessThread')
    
    tweetThread = threading.Thread(target = process_tweets)
    tweetThread.setName('TweetThread')
    
    reportThread = threading.Thread(target = process_reports)
    reportThread.setName('ReportThread')
    
    senseThread.start()
    processThread.start()
    tweetThread.start()
    reportThread.start()
    
if __name__ == "__main__":
    main()
