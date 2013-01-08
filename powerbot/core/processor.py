'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
import time, threading, datetime, logging
from powerbot.core.sensor import get_status, init_sensor
from powerbot.database.models import StateChange, Tweet
from powerbot.database import access 
from Queue import Queue
from powerbot.core.tweet import get_wait_time, send_tweet, internet_on
from powerbot.core.report import sleep_till_midnight, generate_reports
from powerbot.database.access import init_database

old_status = True
state_change_queue = Queue()
tweet_ready = threading.Event()
tweet_ready.set()

def get_message_with_ts(stateChange):
    message = access.get_message(stateChange)
    flag = getStatusName(stateChange.new_state)
    sign = datetime.datetime.fromtimestamp(stateChange.timestamp).strftime("  ~ %H:%M " + flag)
    return message.message + sign

def getStatusName(state):
    return 'ON' if state else 'OFF'

def do_sensing():
    global old_status, state_change_queue
    while True:
        new_status = get_status()
        if(new_status != old_status):
            logging.info('Status changed from ' + getStatusName(old_status) + ' to ' + getStatusName(new_status))
            old_status = new_status
            state_change = StateChange(1 if new_status else 0, int(time.time()))
            state_change_queue.put(state_change)
        time.sleep(1)

def process_change():
    global state_change_queue, tweet_ready
    while True:
        stateChange = state_change_queue.get()
        access.new_state_change(stateChange)
        tweet = Tweet(stateChange.timestamp, get_message_with_ts(stateChange) , None, stateChange.timestamp + 600)
        access.new_tweet(tweet)
        tweet_ready.set()

def process_tweets():
    global tweet_ready
    while tweet_ready.wait():
        if internet_on():
            while True:
                tweet = access.next_tweet()
                if tweet is None:
                    break
                elif send_tweet(tweet):
                    access.update_posted_tweet(tweet)
        else:
            sleep_time = get_wait_time()
            logging.info('Apparently Internet connection is down now. Sleeping time : ' + str(sleep_time))
            time.sleep(sleep_time)
            tweet_ready.set()

def process_reports():
    global tweet_ready
    while True:
        sleep_till_midnight()
        generate_reports()
        tweet_ready.set()

def init_logging():
    logging.basicConfig(#filename='powerbot.log', 
                        format='%(asctime)s [%(threadName)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S",
                         level=logging.INFO)
    logging.info('### Running POWER BOT service ###')

def main():    
    
    init_logging()
    init_database()
    init_sensor()
    
    global old_status 
    lastStateChange = access.get_last_state_change()
    if not lastStateChange is None:
        logging.info('Last ' + str(lastStateChange))
        old_status = True if lastStateChange.new_state else False
    
    senseThread = threading.Thread(target=do_sensing)    
    senseThread.setName('SenseThread')

    processThread = threading.Thread(target=process_change)
    processThread.setName('ProcessThread')
    
    tweetThread = threading.Thread(target=process_tweets)
    tweetThread.setName('TweetThread')
    
    reportThread = threading.Thread(target=process_reports)
    reportThread.setName('ReportThread')
    
    senseThread.start()
    processThread.start()
    tweetThread.start()
    reportThread.start()
    
if __name__ == "__main__":
    main()
