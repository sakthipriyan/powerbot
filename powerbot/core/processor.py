'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

from powerbot.core.sensor import get_status
import time
import threading
from powerbot.database.models import StateChange, Tweet
from powerbot.database import access
import datetime
from Queue import Queue

old_status = True
state_change_queue = Queue()

def get_message_with_ts(stateChange):
    message = access.get_message(stateChange)
    flag =  'ON' if stateChange.new_state else 'OFF'
    sign =  datetime.datetime.fromtimestamp(stateChange.timestamp).strftime("  ~ %H:%M "+flag)
    return message.message + sign

def do_sensing():
    while True:
        new_status = get_status()
        global old_status, state_change_queue
        if(new_status != old_status):
            print str(time.asctime()) + ' Status changed from ' + str(old_status) + ' to '  + str(new_status)
            old_status = new_status
            state_change = StateChange(1 if new_status else 0, int(time.time()))
            state_change_queue.put(state_change)
            print 'Change put into queue ' + str(state_change_queue.qsize())        
        time.sleep(1)

def process_change():
    global state_change_queue
    while True:
        stateChange = state_change_queue.get()
        access.new_state_change(stateChange)
        tweet = Tweet(stateChange.timestamp, get_message_with_ts(stateChange) , None, stateChange.timestamp + 600)
        access.new_tweet(tweet)

def process_tweets():
    while True:
        print 'Trying to send tweet'
        time.sleep(2)

def process_reports():
    while True:
        print "Generates reports"
        time.sleep(5)

def main():    
    print 'Starting POWER BOT service'
    senseThread = threading.Thread(target = do_sensing)    
    processThread = threading.Thread(target = process_change)
    tweetThread = threading.Thread(target = process_tweets)
    reportThread = threading.Thread(target = process_reports)
    
    senseThread.start()
    processThread.start()
    tweetThread.start()
    reportThread.start()
    
if __name__ == "__main__":
    main()

